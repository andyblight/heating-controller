import os
import unittest

from app.prepare_data import load_file, merge_results

class TestLoadFile(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))

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
        file_name = self.path + "/data/2020-09-03-downstairs-back-room.csv"
        # print(file_name)
        (header, contents) = load_file(file_name)
        # Verify header contents.
        # print("HEADER", header)
        self.assertEqual(header[0], "Time", "Header 0 wrong")
        self.assertEqual(header[1], "Temperature", "Header 1 wrong")
        self.assertEqual(header[2], "Humidity", "Header 2 wrong")
        # Verify readings.
        print("CONTENTS", contents)
        # Verify no header rows are in contents.
        for row in contents:
            self.assertNotEqual(row[0], "Time", "Header in contents")
        # Verify number of rows.
        self.assertEqual(len(contents), 3, "Should be 3 rows")
        # Verify row 1 contains 08:18,21.3,73.9.
        self.assertEqual(contents[1][0], "08:18", "Row 1,0 wrong")
        self.assertEqual(contents[1][1], "21.3", "Row 1,1 wrong")
        self.assertEqual(contents[1][2], "73.9", "Row 1,2 wrong")

