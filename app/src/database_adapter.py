from typing import TypedDict, List, NotRequired

import pandas as pd
from pandas import DataFrame

def _get_data() -> pd.DataFrame:
  base_data = pd.read_csv("../../data/air-pollution.csv", header = 0, sep = ",")

  # Rename columns to be more speaking
  base_data.rename(columns = {"Nitrogen oxide (NOx)": "Nitrogen oxide"}, inplace = True)
  base_data.rename(columns = {"Sulphur dioxide (SO₂) emissions": "Sulphur dioxide"}, inplace = True)
  base_data.rename(columns = {"Carbon monoxide (CO) emissions": "Carbon monoxide"}, inplace = True)
  base_data.rename(columns = {"Organic carbon (OC) emissions": "Organic carbon"}, inplace = True)
  base_data.rename(columns = {"Non-methane volatile organic compounds (NMVOC) emissions": "Non-methane volatile organic compounds"}, inplace = True)
  base_data.rename(columns = {"Black carbon (BC) emissions": "Black carbon"}, inplace = True)
  base_data.rename(columns = {"Ammonia (NH₃) emissions": "Ammonia"}, inplace = True)

  return base_data

class Filter(TypedDict):
  """
      TypedDict class to have good typing support for filters.
  """
  Year: NotRequired[List[int]] | None
  Entity: NotRequired[List[str]] | None


def get_filtered_data(filter: Filter | None = None) -> DataFrame:
  """
    This function will filter down data.
    When given a year the data get filtered down by that year.
    When given a entity the data get filtered down by that entity.
    So the more filters, the smaller the dataset
    :param filter: The Filter to filter the data by
    :return: dict of data
  """

  global base_data

  data:pd.DataFrame = _get_data()

  if filter:  # is not None and bool(filter):
    for f in filter:
      data = data[data[f].isin(filter[f])]

  grouped_result = data.groupby(lambda x: True)

  measurement_fields = [
    "Nitrogen oxide",
    "Sulphur dioxide",
    "Carbon monoxide",
    "Organic carbon",
    "Non-methane volatile organic compounds",
    "Black carbon",
    "Ammonia"
  ]

  mean: pd.DataFrame = grouped_result[measurement_fields].mean()
  mean.insert(0, "Type", "Mean", True)

  median: pd.DataFrame = grouped_result[measurement_fields].median()
  median.insert(0, "Type", "Median", True)

  std: pd.DataFrame = grouped_result[measurement_fields].std()
  std.insert(0, "Type", "Standard Deviation", True)

  temp = pd.concat([mean, median])
  merged = pd.concat([temp, std])
  merged.replace({float('nan'): None}, inplace = True)

  merged.reset_index(drop = True, inplace = True)

  return merged
