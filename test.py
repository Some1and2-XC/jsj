import unittest
import jsj


class TestFlattenWithPandasCases(unittest.TestCase):
    """
    Tests the flatten functionality using some of the test cases provided by pandas.json_normalize().
    """

    def test_initial(self):

        data = [
            {"id": 1, "name": {"first": "Coleen", "last": "Volk"}},
            {"name": {"given": "Mark", "family": "Regner"}},
            {"id": 2, "name": "Faye Raker"},
        ]

        jsj_data = jsj.JSON(data)
        res, keys = jsj_data.flatten()

        self.assertEqual(len(res), 3, "Incorrect amount of values!")
        self.assertEqual(len(keys), 6, "Incorrect amount of keys!")


    def test_second(self):

        data = [
            {
                "id": 1,
                "name": "Cole Volk",
                "fitness": {"height": 130, "weight": 60},
            },
            {"name": "Mark Reg", "fitness": {"height": 130, "weight": 60}},
            {
                "id": 2,
                "name": "Faye Raker",
                "fitness": {"height": 130, "weight": 60},
            },
        ]

        jsj_data = jsj.JSON(data)
        res, keys = jsj_data.flatten()

        self.assertEqual(len(res), 3, "Incorrect amount of values!")
        self.assertEqual(len(keys), 4, "Incorrect amount of keys!")


    def test_third(self):

        data = [
            {
                "state": "Florida",
                "shortname": "FL",
                "info": {"governor": "Rick Scott"},
                "counties": [
                    {"name": "Dade", "population": 12345},
                    {"name": "Broward", "population": 40000},
                    {"name": "Palm Beach", "population": 60000},
                ],
            },
            {
                "state": "Ohio",
                "shortname": "OH",
                "info": {"governor": "John Kasich"},
                "counties": [
                    {"name": "Summit", "population": 1234},
                    {"name": "Cuyahoga", "population": 1337},
                ],
            },
        ]

        jsj_data = jsj.JSON(data)
        res, keys = jsj_data.flatten()

        self.assertEqual(len(res), 2, "Incorrect amount of values!")
        self.assertEqual(len(keys), 5, "Incorrect amount of keys!")


class TestDotNotation(unittest.TestCase):
    """
    Test Module for testing dot notation indexing and network requests.
    """

    def test_weather(self):
        """Testing a weather API for getting a timezone"""

        url = "https://api.weather.gov/points/39.7632,-101.6483"

        data = jsj.fetch(url) \
            .json() \
            .get_data()

        self.assertEqual(data.properties.timeZone, "America/Chicago", "Incorrect time zone!")


    def test_music(self):
        """MusicBrainz API test"""

        url = "https://musicbrainz.org/ws/2/release?artist=b1e26560-60e5-4236-bbdb-9aa5a8d5ee19&type=album|ep&fmt=json"

        albums = jsj.fetch(url) \
            .json() \
            .then(lambda data: data.flatten(base=["releases"])[0]) \
            .then(lambda data: [item.title for item in data]) \
            .get_data()

        condition: bool = {"Stoney", "Hollywood’s Bleeding", "beerbongs & bentleys"}.issubset(albums)
        self.assertTrue(condition, "The provided values aren't a subset of the collected albums!")


if __name__ == "__main__":
    get_title = lambda txt, spacing: "{}\033[1;3;4;36m{}\033[m".format(" " * spacing, txt)

    print(get_title("Starting Test Suite!", spacing=2))
    unittest.main()