import os
from enum import Enum
from typing import Literal, TypedDict, List, NotRequired

import pandas as pd
from pandas import DataFrame


class Filter(TypedDict):
    """
    TypedDict class to have good typing support for filters.
    """

    Year: NotRequired[List[int]] | None
    Entity: NotRequired[List[str]] | None


class GroupByParameter(str, Enum):
    """
   Fast API Group By Parameter
   """
    entity = "entity"
    year = "year"


def _get_base_data() -> pd.DataFrame:
    base_data = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + "/../../data/air-pollution.csv", header=0, sep=",")

    # Rename columns to be more speaking
    base_data.rename(
        columns={"Nitrogen oxide (NOx)": "Nitrogen oxide"},
        inplace=True
    )
    base_data.rename(
        columns={"Sulphur dioxide (SO₂) emissions": "Sulphur dioxide"},
        inplace=True
    )
    base_data.rename(
        columns={"Carbon monoxide (CO) emissions": "Carbon monoxide"},
        inplace=True
    )
    base_data.rename(
        columns={"Organic carbon (OC) emissions": "Organic carbon"},
        inplace=True
    )
    base_data.rename(
        columns={
            "Non-methane volatile organic compounds (NMVOC) emissions": "Non-methane volatile organic compounds"
        },
        inplace=True,
    )
    base_data.rename(
        columns={"Black carbon (BC) emissions": "Black carbon"},
        inplace=True
    )
    base_data.rename(
        columns={"Ammonia (NH₃) emissions": "Ammonia"},
        inplace=True
    )

    return base_data


def get_filtered_data(
    filter: Filter | None = None, 
    group_by: GroupByParameter | None = None
) -> DataFrame:
    """
    This function will filter down data.
    When given a year the data get filtered down by that year.
    When given an entity the data get filtered down by that entity.
    So the more filters, the smaller the dataset
    :param filter: The Filter to filter the data by
    :param group_by: The type for group the data by
    :return: dict of data
    """

    base_data: pd.DataFrame = _get_base_data()

    if filter is not None:
        # parameter filter shadows build in, so we have to do 'old school' :)
        f: Literal["Entity", "Year"]
        for f in [f for f in filter if filter[f] is not None]:
            base_data = base_data[base_data[f].isin(filter[f])]

    group_by_str: str | None = None

    if group_by:
        group_by_str = group_by.title()
        grouped_result = base_data.groupby(group_by_str)
    else:
        grouped_result = base_data.groupby(lambda x: True)

    measurement_fields = [
        "Nitrogen oxide",
        "Sulphur dioxide",
        "Carbon monoxide",
        "Organic carbon",
        "Non-methane volatile organic compounds",
        "Black carbon",
        "Ammonia",
    ]

    mean: pd.DataFrame = grouped_result[measurement_fields].mean()
    mean.insert(0, "Type", "Mean", True)

    median: pd.DataFrame = grouped_result[measurement_fields].median()
    median.insert(0, "Type", "Median", True)

    std: pd.DataFrame = grouped_result[measurement_fields].std()
    std.insert(0, "Type", "Standard Deviation", True)

    temp = pd.concat([mean, median])
    merged = pd.concat([temp, std])

    if group_by is not None:
        merged.index.names = ["index"]
        merged[group_by_str] = merged.index
        # ignore error cause we already check for group by
        merged.sort_values(by=[group_by_str], ascending=True, inplace=True)  # type: ignore

    merged.replace({float("nan"): None}, inplace=True)
    merged.reset_index(drop=True, inplace=True)

    return merged
