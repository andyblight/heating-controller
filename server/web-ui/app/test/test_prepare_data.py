import datetime
import os
import unittest

import app.prepare_data as pd
import app.charts as charts
from locations import Location, LOCATIONS

# Set up path to test data once.
this_dir = os.path.dirname(os.path.abspath(__file__))
data_path = this_dir + "/data"
temp_path = this_dir + "/temp"


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
            self.assertFalse(isinstance(entry, datetime.datetime), "Header in contents")
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
            self.assertFalse(isinstance(entry, datetime.datetime), "Header in contents")
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


class TestMergeResults(unittest.TestCase):
    """ Test the function merge_results. """

    def test_merge_one_day_full(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 11)
        raw_results = pd.load_results(data_path, date_from, date_to)
        # Merge results using 60 minute intervals.
        (humidity, temperature) = pd.merge_results(raw_results, 60)
        # print("DESCRIPTION", charts_description)
        # print("Humidity")
        # for entry in humidity.items():
        #     print(entry)
        # print("Temperature")
        # for entry in temperature.items():
        #     print(entry)
        # Expect 24 results in humidity and temperature.
        self.assertEqual(len(humidity), 24, "Incorrect number of entries in humidity")
        self.assertEqual(
            len(temperature), 24, "Incorrect number of entries in temperature"
        )
        # Expect the format to be a list.
        # Verify the 3rd humdity entry.
        # [2020-08-11 02:00:00, 85.0, 66.3, 65.3]
        entry = humidity[2]
        self.assertEqual(
            entry[0],
            datetime.datetime(year=2020, month=8, day=11, hour=2, minute=0, second=0),
            "Humidity datetime did not match.",
        )
        self.assertEqual(entry[1], 85.0, "Humidity external did not match.")
        self.assertEqual(entry[2], 66.3, "Humidity 1 did not match.")
        self.assertEqual(entry[3], 65.3, "Humidity 2 did not match.")
        # Verify the 23rd temperature entry.
        # [2020-08-11 22:00:00, 21.0, 24.6, 25.6]
        entry = temperature[22]
        self.assertEqual(
            entry[0],
            datetime.datetime(year=2020, month=8, day=11, hour=22, minute=0, second=0),
            "Temperature datetime did not match.",
        )
        self.assertEqual(entry[1], 21.0, "Temperature external did not match.")
        self.assertEqual(entry[2], 24.6, "Temperature 1 did not match.")
        self.assertEqual(entry[3], 25.6, "Temperature 2 did not match.")


class TestWriteMergedResults(unittest.TestCase):
    """ Test the functions prepare_date.write_merged_results and
    charts.load_data_file.
    """

    def test_short_file(self):
        # Write the file.
        results = [
            [datetime.datetime(2020, 8, 11, 0, 0), 18.1, 23.2, 24.3],
            [datetime.datetime(2020, 8, 11, 1, 0), 16.9, 23.1, 24.4],
            [datetime.datetime(2020, 8, 11, 2, 0), 17.0, 22.9, 24.3],
        ]
        file_path = temp_path + "/short_test.csv"
        pd.write_merged_results(results, file_path)
        # Verify by loading the file and checking entries.
        data = charts.load_data_file(file_path)
        self.assertEqual(len(data), 3, "Incorrect number of entries")
        # print(data)
        entry = data[0]
        self.assertEqual(
            entry.get("time_of_day"),
            datetime.datetime(2020, 8, 11, 0, 0),
            "Datetime incorrect.",
        )
        self.assertEqual(entry.get("external"), 18.1, "External incorrect.")
        self.assertEqual(entry.get("sensor1"), 23.2, "Sensor 1 incorrect.")
        self.assertEqual(entry.get("sensor2"), 24.3, "Sensor 2 incorrect.")
        entry = data[1]
        self.assertEqual(
            entry.get("time_of_day"),
            datetime.datetime(2020, 8, 11, 1, 0),
            "Datetime incorrect.",
        )
        entry = data[2]
        self.assertEqual(
            entry.get("time_of_day"),
            datetime.datetime(2020, 8, 11, 2, 0),
            "Datetime incorrect.",
        )
