#!/usr/bin/python3

import csv
import datetime

import os, sys, pathlib

current_dir = os.path.dirname(os.path.abspath(__file__))
path = pathlib.Path(current_dir)
parent_dir = path.parent.parent
# print(parent_dir)
locations_dir = os.path.join(parent_dir, "locations")
# print(locations_dir)
sys.path.insert(0, locations_dir)
# print(sys.path)
from locations import Location, LOCATIONS


# Filenames for charts.py to use.
FILE_TODAY_HUMIDITY = "today_humidity.csv"
FILE_TODAY_TEMPERATURE = "today_temperature.csv"
FILE_SEVEN_DAYS_HUMIDITY = "seven_humidity.csv"
FILE_SEVEN_DAYS_TEMPERATURE = "seven_temperature.csv"


class SensorHeader:
    def __init__(self):
        # Hardcoded for now.
        self.columns = ["Time", "Temperature", "Humidity"]


class SensorEntry:
    def __init__(
        self, date_time: datetime.datetime, temperature: float, humidity: float
    ):
        self.date_time = date_time
        self.temperature = temperature
        self.humidity = humidity


class SensorResults:
    def __init__(self, location: Location):
        self.location = location
        self.header = SensorHeader()
        self.entries = []

    def append(self, entry):
        self.entries.append(entry)

    def extend(self, day_results):
        if self.location != day_results.location:
            raise ValueError
        self.entries.extend(day_results.entries)


def load_day_results(path, location, file_date):
    """ Loads a single file (one day) of results for a single sensor.
    Returns an instance of SensorResults.
    """
    sensor_results = SensorResults(location)
    file_name = path + "/"
    file_date_iso = file_date.isoformat()
    file_name += file_date_iso + "-"
    # print("Location is ", location)
    file_name += location.file_name + ".csv"
    with open(file_name, newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # print(row)
            # TODO Could use this but currently hard coded in SensorHeader.
            # Add first row as header.
            # Row format: Time,Temperature,Humidity
            # if header == []:
            #     for value in row:
            #         header.append(value)
            # Exclude header rows (there can be more than one).
            # First entry of header row is always "Time".
            if row[0] != "Time":
                # Extract time, temperature and humidity.
                time = datetime.datetime.strptime(row[0], "%H:%M").time()
                # Use file_date to make time into datetime.
                date_time = datetime.datetime.combine(file_date, time)
                temperature_rounded = round(float(row[1]), 1)
                humidity_rounded = round(float(row[2]), 1)
                entry = SensorEntry(date_time, temperature_rounded, humidity_rounded)
                sensor_results.append(entry)
    return sensor_results


def load_results_for_location(path, location, date_from, date_to):
    """ Returns a SensorResults object containing the data for the given range
    of dates.
    """
    # print(date_from, date_to)
    location_results = SensorResults(location)
    step = datetime.timedelta(days=1)
    while date_from <= date_to:
        # print(date_from.strftime('%Y_%m_%d'))
        day_results = load_day_results(path, location, date_from)
        location_results.extend(day_results)
        date_from += step
    return location_results


def load_results(path, date_from, date_to):
    """ Returns a list of SensorResults objects, one per location.
    Each SensorResults object has the data for the given range of dates.
    """
    all_results = []
    for location in LOCATIONS:
        day_results = load_results_for_location(path, location, date_from, date_to)
        all_results.append(day_results)
    return all_results


def merge_results(all_results, interval_minutes):
    """ Merges results from external and all sensors into two CSV files, one
    for temperature and the other for humidity.
    The columns in each file are:
        datetime, external, <sensor1 location name>, ..., <sensorN location name>
    """
    for location_results in all_results:
        for entry in location_results.entries:
            data_points = __build_data_points(entry)
            data.append(data_points)


def create_files_today():
    """ """
    # today = ...
    # path = ...
    # interval_minutes = 15
    # all_results = load_result(path, today, today)
    # (humidity_results, temperature_results) = merge_results(all_results, interval_minutes)
    # write_results(humidity_results)
    # write_results(temperature_results)
    pass


def create_files_seven_days():
    """ """
    # load
    pass
