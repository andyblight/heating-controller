import datetime
import os
import unittest

import app.prepare_data as pd

# AJB HACK
LOCATIONS = [
    ["external"],
    ["downstairs-back-room"],
    ["upstairs-landing"],
]


class TestLoadDayResults(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = self.path + "/data"

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
        location = "downstairs-back-room"
        file_date = datetime.date(2020, 9, 3)
        # print(file_name)
        day_results = pd.load_day_results(self.data_path, location, file_date)
        # Verify location.
        self.assertEqual(day_results.location, location, "Location wrong")
        # Verify SensorHeader contents.
        # print("HEADER", day_results.header)
        header_columns = day_results.header.columns
        self.assertEqual(header_columns[0], "Time", "Header 0 wrong")
        self.assertEqual(header_columns[1], "Temperature", "Header 1 wrong")
        self.assertEqual(header_columns[2], "Humidity", "Header 2 wrong")
        # Verify readings.
        # print("ENTRIES", day_results.entries)
        # Verify no header rows are in contents.
        for entry in day_results.entries:
            self.assertNotEqual(entry.date_time, "Time", "Header in contents")
        # Verify number of rows.
        self.assertEqual(len(day_results.entries), 3, "Should be 3 rows")
        # Verify row 1 contains 08:18,21.3,73.9.
        entry = day_results.entries[1]
        time = datetime.time(8, 18)
        expected_datetime = datetime.datetime.combine(file_date, time)
        self.assertEqual(entry.date_time, expected_datetime, "Date time wrong")
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
        location = "upstairs-landing"
        file_date = datetime.date(2020, 9, 3)
        # print(file_name)
        day_results = pd.load_day_results(self.data_path, location, file_date)
        # Verify readings.
        # print("ENTRIES", day_results.entries)
        # Verify no header rows are in contents.
        for entry in day_results.entries:
            self.assertNotEqual(entry.date_time, "Time", "Header in contents")
        # Verify number of rows.
        self.assertEqual(len(day_results.entries), 1, "Should be 1 row")
        # Verify number of rows.
        # Verify row 1 contains 08:21,20.2,68.1.
        entry = day_results.entries[0]
        time = datetime.time(8, 21)
        expected_datetime = datetime.datetime.combine(file_date, time)
        self.assertEqual(entry.date_time, expected_datetime, "Date time wrong")
        self.assertEqual(entry.temperature, 20.2, "Temperature wrong")
        self.assertEqual(entry.humidity, 68.1, "Humidity wrong")

    def test_file_3(self):
        # Test different header row and no results.
        # The data in this file are:
        # Time,Temperature C,Humidity %,Wind m/s,Gust m/s
        location = "external"
        file_date = datetime.date(2020, 9, 3)
        # print(file_name)
        day_results = pd.load_day_results(self.data_path, location, file_date)
        # Verify entries are empty.
        self.assertEqual(len(day_results.entries), 0, "Should be 0 rows")


class TestLoadResultsForLocation(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = self.path + "/data"
        self.location = "external"

    def test_load_single_day(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 11)
        location_results = pd.load_results_for_location(
            self.data_path, self.location, date_from, date_to
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
            self.data_path, self.location, date_from, date_to
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
            self.data_path, self.location, date_from, date_to
        )
        # print(location_results)
        # Verify that single day from given location has been loaded.
        self.assertEqual(
            len(location_results.entries), 2014, "Incorrect number of entries"
        )


class TestMergeResults(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = self.path + "/data"

    def test_merge_one_day_full(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 11)
        raw_results = load_results(self.data_path, date_from, date_to)
        # Merge results using default.
        (description, data) = merge_results(raw_results, 5)
        # Output format has to be.
        # description = {
        #     "time_of_day": ("timeofday", "Time"),
        #     "external": ("number", "External"),
        #     "sensor1": ("number", "Upstairs"),
        #     "sensor2": ("number", "Downstairs"),
        # }
        # data = [
        #     {
        #         "time_of_day": datetime.time(hour=10, minute=30),
        #         "external": 25.4,
        #         "sensor1": 57.0,
        #         "sensor2": 25.7,
        #     },
        #     {
        #         "time_of_day": datetime.time(hour=11, minute=30),
        #         "external": 11.7,
        #         "sensor1": 18.8,
        #         "sensor2": 10.5,
        #     },
        # ]
        self.assertEqual(
            len(description), 4, "Incorrect number of entries in description"
        )

    # def test_merge_seven_days(self):
    #     date_from = datetime.date(2020, 8, 11)
    #     date_to = datetime.date(2020, 8, 17)
    #     raw_results = load_results(self.data_path, date_from, date_to)
    #     # Merge results using default.
    #     results = merge_results(raw_results)

    # def test_merge_one_day_part(self):
    #     date_from = datetime.date(2020, 9, 3)
    #     date_to = datetime.date(2020, 9, 3)
    #     raw_results = load_results(self.data_path, date_from, date_to)
    #     # Merge results using default.
    #     results = merge_results(raw_results)
