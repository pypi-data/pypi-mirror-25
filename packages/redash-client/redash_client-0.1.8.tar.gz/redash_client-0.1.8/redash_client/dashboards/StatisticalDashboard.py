import math
import statistics
from scipy import stats
import statsmodels.stats.power as smp

from redash_client.utils import upload_as_json
from redash_client.constants import TTableSchema, VizWidth
from redash_client.dashboards.ActivityStreamExperimentDashboard import (
    ActivityStreamExperimentDashboard)


class StatisticalDashboard(ActivityStreamExperimentDashboard):
  TTABLE_DESCRIPTION = (
    "Smaller p-values (e.g. <= 0.05) indicate a high "
    "probability that the variants have different distributions. Alpha "
    "error indicates the probability a difference is observed when one "
    "does not exists. Larger power (e.g. >= 0.7) indicates a high "
    "probability that an observed difference is correct. Beta error "
    "(1 - power) indicates the probability that no difference is observed "
    "when indeed one exists.")

  def _compute_pooled_stddev(self, control_std, exp_std,
                             control_vals, exp_vals):

    control_len_sub_1 = len(control_vals) - 1
    exp_len_sub_1 = len(exp_vals) - 1

    pooled_stddev_num = (pow(control_std, 2) * control_len_sub_1 +
                         pow(exp_std, 2) * exp_len_sub_1)
    pooled_stddev_denom = control_len_sub_1 + exp_len_sub_1

    pooled_stddev = math.sqrt(pooled_stddev_num / float(pooled_stddev_denom))
    return pooled_stddev

  def _power_and_ttest(self, control_vals, exp_vals):
    control_mean = statistics.mean(control_vals)
    control_std = statistics.stdev(control_vals)
    exp_mean = statistics.mean(exp_vals)
    exp_std = statistics.stdev(exp_vals)

    pooled_stddev = self._compute_pooled_stddev(
        control_std, exp_std, control_vals, exp_vals)

    power = 0
    if control_mean != 0 and pooled_stddev != 0:
      percent_diff = abs(control_mean - exp_mean) / control_mean
      effect_size = (percent_diff * float(control_mean)) / float(pooled_stddev)
      power = smp.TTestIndPower().solve_power(
          effect_size,
          nobs1=len(control_vals),
          ratio=len(exp_vals) / float(len(control_vals)),
          alpha=self.ALPHA_ERROR, alternative='two-sided')

    ttest_result = stats.ttest_ind(control_vals, exp_vals, equal_var=False)
    p_val = ""
    if len(ttest_result) >= 2 and not math.isnan(ttest_result[1]):
      p_val = ttest_result[1]

    mean_diff = exp_mean - control_mean

    if p_val <= 0.05 and mean_diff < 0:
      significance = "Negative"
    elif p_val <= 0.05 and mean_diff > 0:
      significance = "Positive"
    else:
      significance = "Neutral"

    return {
        "power": power,
        "p_val": p_val,
        "mean_diff": mean_diff,
        "significance": significance
    }

  def _get_ttable_data_for_query(self, label, query_string,
                                 column_name, data_source_id):
    data = self.redash.get_query_results(
        query_string, data_source_id)

    if data is None or len(data) <= 3 or (column_name not in data[0]):
      return {}

    control_vals = []
    exp_vals = []
    for row in data:
      if "type" in row and row["type"] == "experiment":
        exp_vals.append(row[column_name])
      elif "type" in row and row["type"] == "control":
        control_vals.append(row[column_name])
      else:
        return {}

    results = self._power_and_ttest(control_vals, exp_vals)
    return {
        "Metric": label,
        "Alpha Error": self.ALPHA_ERROR,
        "Power": results["power"],
        "Two-Tailed P-value (ttest)": results["p_val"],
        "Significance": results["significance"],
        "Experiment Mean - Control Mean": results["mean_diff"]
    }

  def _apply_ttable_event_template(self, template, chart_data, events_list,
                                   events_table, values):
    self._params["events_table"] = events_table
    for event in events_list:
      event_data = self._get_event_title_description(template, event)
      options = self._create_options()

      adjusted_string = template["query"].replace(
          "{{{", "{").replace("}}}", "}")
      query_string = adjusted_string.format(**self._params)

      self.redash.update_query(
          template["id"],
          template["name"],
          template["query"],
          template["data_source_id"],
          event_data["description"],
          options
      )
      ttable_row = self._get_ttable_data_for_query(
          event_data["title"],
          query_string,
          "count",
          template["data_source_id"])

      if len(ttable_row) == 0:
        self._logger.info((
            "StatisticalTester: "
            "Query '{name}' has no relevant data and will not be "
            "included in T-Table.".format(name=event_data["title"])))
        continue

      values["rows"].append(ttable_row)

  def add_ttable(self, template_keyword, events_list=None, events_table=None):
    self._logger.info(
        "StatisticalTester: Creating a T-Table")

    if events_list is None:
      events_list = self.DEFAULT_EVENTS
      events_table = self._events_table

    chart_data = self.get_query_ids_and_names()
    values = {"columns": TTableSchema, "rows": []}

    # Remove a table if it already exists
    if self.T_TABLE_TITLE in chart_data:
      self._logger.info((
          "StatisticalTester: "
          "Stale T-Table exists and will be removed"))
      query_id = chart_data[self.T_TABLE_TITLE]["query_id"]
      widget_id = chart_data[self.T_TABLE_TITLE]["widget_id"]
      self.remove_graph_from_dashboard(widget_id, query_id)

    # Create the t-table
    self._apply_functions_to_templates(
        template_keyword,
        events_list,
        events_table,
        self._apply_ttable_event_template,
        None,
        values)

    query_string = upload_as_json("experiments", self._experiment_id, values)
    query_id, table_id = self.redash.create_new_query(
        self.T_TABLE_TITLE,
        query_string,
        self.URL_FETCHER_DATA_SOURCE_ID,
        self.TTABLE_DESCRIPTION,
    )
    self.redash.add_visualization_to_dashboard(
        self._dash_id, table_id, VizWidth.WIDE)
