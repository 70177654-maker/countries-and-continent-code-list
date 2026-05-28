import pandas as pd
import unittest

from filters import get_country_counts_by_continent


class FiltersTests(unittest.TestCase):
    def test_get_country_counts_by_continent_returns_expected_frame(self):
        df = pd.DataFrame(
            {
                "Country": ["Algeria", "Egypt", "France", "Germany"],
                "Continent": ["Africa", "Africa", "Europe", "Europe"],
            }
        )

        result = get_country_counts_by_continent(df)

        self.assertEqual(list(result.columns), ["Continent", "Count"])
        self.assertEqual(result.to_dict("records"), [
            {"Continent": "Africa", "Count": 2},
            {"Continent": "Europe", "Count": 2},
        ])


if __name__ == "__main__":
    unittest.main()
