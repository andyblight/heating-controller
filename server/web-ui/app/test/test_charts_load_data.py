import csv
import datetime
import os
import unittest

from app.prepare_data import FILE_SEVEN_DAYS_TEMPERATURE
from app.charts import load_data_file

# Set up path to test data once.
data_path = os.path.dirname(os.path.abspath(__file__)) + "/data"


EMPTY_FILE_NAME = data_path + "/empty.csv"
SINGLE_FILE_NAME = data_path + "/single.csv"
TWO_FILE_NAME = data_path + "/two.csv"
FIVE_FILE_NAME = data_path + "/five.csv"

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
    row.append(temperature_data[index]["time_of_day"])
    row.append(temperature_data[index]["external"])
    row.append(temperature_data[index]["sensor1"])
    row.append(temperature_data[index]["sensor2"])
    # print(row)
    return row


def create_files():
    with open(SINGLE_FILE_NAME, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        row = create_row(0)
        writer.writerow(row)

    with open(TWO_FILE_NAME, "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for i in range(0, 2):
            row = create_row(i)
            writer.writerow(row)

    with open(FIVE_FILE_NAME, "w", newline="") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for i in range(0, 5):
            row = create_row(i)
            writer.writerow(row)


class TestChartsLoadData(unittest.TestCase):
    """ Test the function load_data() in charts.py.
    """

    def setUp(self):
        # Only need to do this to create the files.
        # create_files()

    def test_file_not_found(self):
        load_data_file("not_found.csv")

    def test_empty_file(self):
        load_data_file("empty.csv")

    def test_single_entry(self):
        load_data_file("single.csv")

    def test_two_entries(self):
        load_data_file("two.csv")

    def test_five_entries(self):
        load_data_file("five.csv")

    def test_seven_days(self):
        """ Tests a real data file containing seven days of data. """
        load_data_file(FILE_SEVEN_DAYS_TEMPERATURE)
