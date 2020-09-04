import datetime
import os
import unittest

from app.prepare_data import load_file, load_results, merge_results, LOCATIONS


class TestLoadFile(unittest.TestCase):
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
        file_name = self.data_path + "/2020-09-03-downstairs-back-room.csv"
        # print(file_name)
        (header, contents) = load_file(file_name)
        # Verify header contents.
        # print("HEADER", header)
        self.assertEqual(header[0], "Time", "Header 0 wrong")
        self.assertEqual(header[1], "Temperature", "Header 1 wrong")
        self.assertEqual(header[2], "Humidity", "Header 2 wrong")
        # Verify readings.
        # print("CONTENTS", contents)
        # Verify no header rows are in contents.
        for row in contents:
            self.assertNotEqual(row[0], "Time", "Header in contents")
        # Verify number of rows.
        self.assertEqual(len(contents), 3, "Should be 3 rows")
        # Verify row 1 contains 08:18,21.3,73.9.
        self.assertEqual(contents[1][0], datetime.time(8, 18), "Row 1,0 wrong")
        self.assertEqual(contents[1][1], 21.3, "Row 1,1 wrong")
        self.assertEqual(contents[1][2], 73.9, "Row 1,2 wrong")

    def test_file_2(self):
        # The data in this file are:
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # Time,Temperature,Humidity
        # 08:21,20.2,68.1
        file_name = self.data_path + "/2020-09-03-upstairs-landing.csv"
        # print(file_name)
        (header, contents) = load_file(file_name)
        # Verify header contents.
        # print("HEADER", header)
        self.assertEqual(header[0], "Time", "Header 0 wrong")
        self.assertEqual(header[1], "Temperature", "Header 1 wrong")
        self.assertEqual(header[2], "Humidity", "Header 2 wrong")
        # Verify readings.
        # print("CONTENTS", contents)
        # Verify no header rows are in contents.
        for row in contents:
            self.assertNotEqual(row[0], "Time", "Header in contents")
        # Verify number of rows.
        self.assertEqual(len(contents), 1, "Should be 1 row")
        # Verify row 1 contains 08:18,21.3,73.9.
        self.assertEqual(contents[0][0], datetime.time(8, 21), "Row 1,0 wrong")
        self.assertEqual(contents[0][1], 20.2, "Row 1,1 wrong")
        self.assertEqual(contents[0][2], 68.1, "Row 1,2 wrong")

    def test_file_3(self):
        # Test different header row and no results.
        # The data in this file are:
        # Time,Temperature C,Humidity %,Wind m/s,Gust m/s
        file_name = self.data_path + "/2020-09-03-external.csv"
        # print(file_name)
        (header, contents) = load_file(file_name)
        # Verify header contents.
        # print("HEADER", header)
        self.assertEqual(header[0], "Time", "Header 0 wrong")
        self.assertEqual(header[1], "Temperature C", "Header 1 wrong")
        self.assertEqual(header[2], "Humidity %", "Header 2 wrong")
        self.assertEqual(header[3], "Wind m/s", "Header 3 wrong")
        self.assertEqual(header[4], "Gust m/s", "Header 4 wrong")
        # Verify readings.
        # print("CONTENTS", contents)
        # Verify contents are empty.
        self.assertEqual(len(contents), 0, "Should be 0 rows")


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
