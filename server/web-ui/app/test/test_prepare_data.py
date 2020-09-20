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
        entry = day_results.entries[0]
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


class TestLoadResults(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = self.path + "/data"

    def test_load_single_day(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 11)
        raw_contents = load_results(self.data_path, date_from, date_to)
        # print(raw_contents)
        # Verify that single day from three locations has been loaded.
        self.assertEqual(len(raw_contents), 1, "Incorrect number of days")
        day_results = raw_contents[0]
        results_date = day_results[0]
        self.assertEqual(results_date, date_from, "Incorrect date")
        # Verify number of locations.
        location_results = day_results[1]
        self.assertEqual(len(location_results), 3, "Incorrect number of locations")
        # Use location 0 (external)
        location_data = location_results[0]
        location = location_data[0]
        self.assertEqual(location, "external", "Incorrect location")
        contents = location_data[1]
        # Check header contents.
        header = contents[0]
        self.assertEqual(header[1], "Temperature C", "Incorrect header")
        # Check number of entries.
        entries = contents[1]
        self.assertEqual(len(entries), 288, "Incorrect number of entries")
        # Check the values in entry
        entry = entries[122]
        entry_time = entry[0]
        entry_temperature = entry[1]
        entry_humidity = entry[2]
        self.assertEqual(entry_time, datetime.time(10, 13), "Incorrect time")
        self.assertEqual(entry_temperature, 21.2, "Incorrect temperature")
        self.assertEqual(entry_humidity, 76.0, "Incorrect humidity")

    def test_load_two_days(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 12)
        raw_contents = load_results(self.data_path, date_from, date_to)
        # Verify that two days from three locations has been loaded.
        self.assertEqual(len(raw_contents), 2, "Incorrect number of days")
        # Use day 2
        day_results = raw_contents[1]
        results_date = day_results[0]
        self.assertEqual(results_date, date_to, "Incorrect date")
        # Verify number of locations.
        location_results = day_results[1]
        self.assertEqual(len(location_results), 3, "Incorrect number of locations")
        # Use location 1 (downstairs-back-room)
        location_data = location_results[1]
        location = location_data[0]
        self.assertEqual(location, "downstairs-back-room", "Incorrect location")
        contents = location_data[1]
        # Check header contents.
        header = contents[0]
        self.assertEqual(header[1], "Temperature", "Incorrect header")
        # Check number of entries.
        entries = contents[1]
        self.assertEqual(len(entries), 288, "Incorrect number of entries")
        # Check the values in entry
        entry = entries[122]
        entry_time = entry[0]
        entry_temperature = entry[1]
        entry_humidity = entry[2]
        self.assertEqual(entry_time, datetime.time(10, 13), "Incorrect time")
        self.assertEqual(entry_temperature, 24.2, "Incorrect temperature")
        self.assertEqual(entry_humidity, 72.8, "Incorrect humidity")

    def test_load_seven_days(self):
        date_from = datetime.date(2020, 8, 11)
        date_to = datetime.date(2020, 8, 17)
        raw_contents = load_results(self.data_path, date_from, date_to)
        # Verify that seven days from three locations has been loaded.
        self.assertEqual(len(raw_contents), 7, "Incorrect number of days")
        # Use day 7
        day_results = raw_contents[6]
        results_date = day_results[0]
        self.assertEqual(results_date, date_to, "Incorrect date")
        # Verify number of locations.
        location_results = day_results[1]
        self.assertEqual(len(location_results), 3, "Incorrect number of locations")
        # Use location 3 (upstairs-landing)
        location_data = location_results[2]
        location = location_data[0]
        self.assertEqual(location, "upstairs-landing", "Incorrect location")
        contents = location_data[1]
        # Check header contents.
        header = contents[0]
        self.assertEqual(header[1], "Temperature", "Incorrect header")
        # Check number of entries.
        entries = contents[1]
        self.assertEqual(len(entries), 288, "Incorrect number of entries")
        # Check the values in entry
        entry = entries[122]
        entry_time = entry[0]
        entry_temperature = entry[1]
        entry_humidity = entry[2]
        self.assertEqual(entry_time, datetime.time(10, 10), "Incorrect time")
        self.assertEqual(entry_temperature, 21.8, "Incorrect temperature")
        self.assertEqual(entry_humidity, 69.3, "Incorrect humidity")


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
        self.assertEqual(len(description), 4,
                         "Incorrect number of entries in description")

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

