import datetime
import os
import unittest

import app.prepare_data as pd
from app.charts import description as charts_description
from locations import Location, LOCATIONS

# Set up path to test data once.
data_path = os.path.dirname(os.path.abspath(__file__)) + "/data"


class TestLoadDayResults(unittest.TestCase):
    def test_file_1(self):
        # The data in this file are:
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # 08:16,0.0,0.0
        # Time,Temperature,Humidity
        # 08:18,21.3,73.9
        # Time,Temperature,Humidity
        # 08:21,20.6,73.8
        location = Location("", "downstairs-back-room", "", "")
        file_date = datetime.date(2020, 9, 3)
        day_results = pd.load_day_results(data_path, location, file_date)
        # Verify location.
        self.assertEqual(day_results.location, location, "Location wrong")
        # Verify SensorHeader contents.
        # print("HEADER", day_results.header, day_results.header.columns)
        header_columns = day_results.header.columns
        self.assertEqual(header_columns[0], "DateTime", "Header 0 wrong")
        self.assertEqual(header_columns[1], "Temperature", "Header 1 wrong")
        self.assertEqual(header_columns[2], "Humidity", "Header 2 wrong")
        # Verify readings.
        # print("ENTRIES", day_results.entries)
        # Verify no header rows are in contents.
        for entry in day_results.entries:
            self.assertFalse(type(entry) == type(datetime.datetime), "Header in contents")
        # Verify number of rows.
        self.assertEqual(len(day_results.entries), 3, "Should be 3 rows")
        # Verify the entry for 08:18 contains 21.3,73.9.
        time = datetime.time(8, 18)
        expected_datetime = datetime.datetime.combine(file_date, time)
        entry = day_results.get(expected_datetime)
        self.assertTrue(entry, "Entry not found")
        self.assertEqual(entry.temperature, 21.3, "Temperature wrong")
        self.assertEqual(entry.humidity, 73.9, "Humidity wrong")

    def test_file_2(self):
        # The data in this file are:
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # 08:21,20.2,68.1
        location = Location("", "upstairs-landing", "", "")
        file_date = datetime.date(2020, 9, 3)
        day_results = pd.load_day_results(data_path, location, file_date)
        # Verify readings.
        # Verify no header rows are in contents.
        for entry in day_results.entries:
            self.assertFalse(type(entry) == type(datetime.datetime), "Header in contents")
        # Verify number of rows.
        self.assertEqual(len(day_results.entries), 1, "Should be 1 row")
        # Verify the entry for 08:21 contains 20.2,68.1.
        time = datetime.time(8, 21)
        expected_datetime = datetime.datetime.combine(file_date, time)
        entry = day_results.get(expected_datetime)
        self.assertTrue(entry, "Entry not found")
        self.assertEqual(entry.temperature, 20.2, "Temperature wrong")
        self.assertEqual(entry.humidity, 68.1, "Humidity wrong")

    def test_file_3(self):
        # Test different header row and no results.
        # The data in this file are:
        # Time,Temperature C,Humidity %,Wind m/s,Gust m/s
        location = Location("", "external", "", "")
        file_date = datetime.date(2020, 9, 3)
        # print(file_name)
        day_results = pd.load_day_results(data_path, location, file_date)
        # Verify entries are empty.
        self.assertEqual(len(day_results.entries), 0, "Should be 0 rows")


class TestLoadResultsForLocation(unittest.TestCase):
    def setUp(self):
        self.location = Location("", "external", "", "")

    def test_load_single_day(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 11)
        location_results = pd.load_results_for_location(
            data_path, self.location, date_from, date_to
        )
        # print(location_results)
        # Verify that single day from given location has been loaded.
        self.assertEqual(
            len(location_results.entries), 288, "Incorrect number of entries"
        )

    def test_load_two_days(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 12)
        location_results = pd.load_results_for_location(
            data_path, self.location, date_from, date_to
        )
        # print(location_results)
        # Verify that single day from given location has been loaded.
        self.assertEqual(
            len(location_results.entries), 576, "Incorrect number of entries"
        )

    def test_load_seven_days(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 17)
        location_results = pd.load_results_for_location(
            data_path, self.location, date_from, date_to
        )
        # print(location_results)
        # Verify that single day from given location has been loaded.
        self.assertEqual(
            len(location_results.entries), 2014, "Incorrect number of entries"
        )


class TestLoadResults(unittest.TestCase):
    """ Test load_results().
    Verify that all locations are loaded for the specifed date range.
    Only need to test that all locations are loaded.
    Date range and contents of the entries have been tested elsewhere.
    """

    def test_load_results(self):
        # Use a range of dates for fun!
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 14)
        location_results_list = pd.load_results(data_path, date_from, date_to)
        # print(location_results_list)
        # Check that there are the correct number of locations.
        self.assertEqual(
            len(location_results_list), len(LOCATIONS), "Incorrect number of locations"
        )
        # Verify that each location is in the master list.
        for location_results in location_results_list:
            found = False
            for location in LOCATIONS:
                if location.file_name == location_results.location:
                    found = True
                    break
            self.assertFalse(found, "Location not found")


class TestWriteResults(unittest.TestCase):
    def todo():
        pass


class TestMergeResults(unittest.TestCase):
    """ Test the function merge_results. """

    def test_merge_one_day_full(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 11)
        raw_results = pd.load_results(data_path, date_from, date_to)
        # Merge results using 15 minute intervals.
        (humidity, temperature) = pd.merge_results(raw_results, 60)
        print("DESCRIPTION", charts_description)
        print("Humidity")
        for k, v in humidity.items():
            print(k, v)
        print("Temperature")
        for k, v in temperature.items():
            print(k, v)
        # # Output format has to be.
        # # description = {
        # #     "time_of_day": ("timeofday", "Time"),
        # #     "external": ("number", "External"),
        # #     "sensor1": ("number", "Upstairs"),
        # #     "sensor2": ("number", "Downstairs"),
        # # }
        # # data = [
        # #     {
        # #         "time_of_day": datetime.time(hour=10, minute=30),
        # #         "external": 25.4,
        # #         "sensor1": 57.0,
        # #         "sensor2": 25.7,
        # #     },
        # #     {
        # #         "time_of_day": datetime.time(hour=11, minute=30),
        # #         "external": 11.7,
        # #         "sensor1": 18.8,
        # #         "sensor2": 10.5,
        # #     },
        # # ]
        # self.assertEqual(
        #     len(description), 4, "Incorrect number of entries in description"
        # )

    # def test_merge_seven_days(self):
    #     date_from = datetime.date(2020, 8, 11)
    #     date_to = datetime.date(2020, 8, 17)
    #     raw_results = load_results(data_path, date_from, date_to)
    #     # Merge results using default.
    #     results = merge_results(raw_results)

    # def test_merge_one_day_part(self):
    #     date_from = datetime.date(2020, 9, 3)
    #     date_to = datetime.date(2020, 9, 3)
    #     raw_results = load_results(data_path, date_from, date_to)
    #     # Merge results using default.
    #     results = merge_results(raw_results)
