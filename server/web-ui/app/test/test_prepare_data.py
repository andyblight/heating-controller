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
        print("HEADER", header)
        self.assertEqual(header[0], "Time", "Header 0 wrong")
        self.assertEqual(header[1], "Temperature", "Header 1 wrong")
        self.assertEqual(header[2], "Humidity", "Header 2 wrong")

