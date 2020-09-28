import csv
import datetime
import os
import unittest

from app.prepare_data import FILE_SEVEN_DAYS_TEMPERATURE
from app.charts import load_data_file

# Set up path to test data once.
data_path = os.path.dirname(os.path.abspath(__file__)) + "/data"


NOT_FOUND_PATH = data_path + "/not_found.csv"
EMPTY_PATH = data_path + "/empty.csv"
SINGLE_PATH = data_path + "/single.csv"
TWO_PATH = data_path + "/two.csv"
FIVE_PATH = data_path + "/five.csv"
SEVEN_DAYS_PATH = data_path + "/" + FILE_SEVEN_DAYS_TEMPERATURE

temperature_data = [
    {
        "time_of_day": datetime.time(hour=8, minute=0),
        "external": 14.2,
        "sensor1": 19.8,
        "sensor2": 21.9,
    },
    {
        "time_of_day": datetime.time(hour=8, minute=30),
        "external": 15.4,
        "sensor1": 20.1,
        "sensor2": 22.3,
    },
    {
        "time_of_day": datetime.time(hour=9, minute=30),
        "external": 16.4,
        "sensor1": 20.5,
        "sensor2": 22.8,
    },
    {
        "time_of_day": datetime.time(hour=10, minute=30),
        "external": 17.4,
        "sensor1": 21.1,
        "sensor2": 23.3,
    },
    {
        "time_of_day": datetime.time(hour=11, minute=30),
        "external": 18.4,
        "sensor1": 21.6,
        "sensor2": 23.8,
    },
]


def create_row(index):
    row = []
    # Create datetime from time.
    today = datetime.datetime.utcnow()
    entry_time = temperature_data[index]["time_of_day"]
    date_time = datetime.datetime.combine(today, entry_time)
    row.append(date_time)
    # Just append the rest of the values.
    row.append(temperature_data[index]["external"])
    row.append(temperature_data[index]["sensor1"])
    row.append(temperature_data[index]["sensor2"])
    # print(row)
    return row


def create_files():
    with open(SINGLE_PATH, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        row = create_row(0)
        writer.writerow(row)

    with open(TWO_PATH, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(0, 2):
            row = create_row(i)
            writer.writerow(row)

    with open(FIVE_PATH, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(0, 5):
            row = create_row(i)
            writer.writerow(row)


class TestChartsLoadData(unittest.TestCase):
    """ Test the function load_data() in charts.py.
    """

    # Only need to do this to create the files.
    # def setUp(self):
    #     create_files()

    def test_file_not_found(self):
        load_data_file(NOT_FOUND_PATH)

    def test_empty_file(self):
        load_data_file(EMPTY_PATH)

    def test_single_entry(self):
        load_data_file(SINGLE_PATH)

    def test_two_entries(self):
        load_data_file(TWO_PATH)

    def test_five_entries(self):
        load_data_file(FIVE_PATH)

    def test_seven_days(self):
        """ Use a data file containing seven days of data. """
        load_data_file(SEVEN_DAYS_PATH)
