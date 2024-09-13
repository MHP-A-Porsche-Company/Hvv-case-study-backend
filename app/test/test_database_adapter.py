import unittest
from unittest.mock import patch

import pandas as pd

from src.database_adapter import get_filtered_data, Filter


class TestDatabaseAdapter(unittest.TestCase):

  @patch('src.database_adapter._get_data')
  def test_get_filtered_data_without_filter(self, _get_data_mock):
    data = {
      "Entity": ["A", "B"],
      "Year": [2024, 2024],
      "Nitrogen oxide": [1, 2],
      "Sulphur dioxide": [1, 2],
      "Carbon monoxide": [1, 2],
      "Organic carbon": [1, 2],
      "Non-methane volatile organic compounds": [1, 2],
      "Black carbon": [1, 2],
      "Ammonia": [1, 2]
    }
    _get_data_mock.return_value = pd.DataFrame(data = data)

    filter: Filter = None

    actual = get_filtered_data(filter)

    row = actual.iloc[1].values.flatten().tolist()
    self.assertEqual(row, ["Median", 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5])

    row = actual.iloc[2].values.flatten().tolist()
    self.assertEqual(row, ["Standard Deviation", 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476])


  @patch('src.database_adapter._get_data')
  def test_get_filtered_data_with_entity_filter(self, _get_data_mock):
    data = {
      "Entity": ["A", "B"],
      "Year": [2024, 2024],
      "Nitrogen oxide": [1, 2],
      "Sulphur dioxide": [1, 2],
      "Carbon monoxide": [1, 2],
      "Organic carbon": [1, 2],
      "Non-methane volatile organic compounds": [1, 2],
      "Black carbon": [1, 2],
      "Ammonia": [1, 2]
    }
    _get_data_mock.return_value = pd.DataFrame(data = data)

    filter: Filter = {
      "Entity": ["A"]
    }

    actual = get_filtered_data(filter)

    row = actual.iloc[1].values.flatten().tolist()
    self.assertEqual(row, ["Median", 1, 1, 1, 1, 1, 1, 1])

    row = actual.iloc[2].values.flatten().tolist()
    self.assertEqual(row, ["Standard Deviation", None, None, None, None, None, None, None])


  @patch('src.database_adapter._get_data')
  def test_get_filtered_data_with_year_filter(self, _get_data_mock):
    data = {
      "Entity": ["A", "B"],
      "Year": [2024, 2024],
      "Nitrogen oxide": [1, 2],
      "Sulphur dioxide": [1, 2],
      "Carbon monoxide": [1, 2],
      "Organic carbon": [1, 2],
      "Non-methane volatile organic compounds": [1, 2],
      "Black carbon": [1, 2],
      "Ammonia": [1, 2]
    }
    _get_data_mock.return_value = pd.DataFrame(data = data)

    filter: Filter = {
      "Year": [2024]
    }

    actual = get_filtered_data(filter)

    row = actual.iloc[1].values.flatten().tolist()
    self.assertEqual(row, ["Median", 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5])

    row = actual.iloc[2].values.flatten().tolist()
    self.assertEqual(row, ["Standard Deviation", 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476])


if __name__ == "__main__":
    unittest.main()