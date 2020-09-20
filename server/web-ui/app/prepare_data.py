#!/usr/bin/python3

import csv
import datetime

import os,sys,pathlib
current_dir = os.path.dirname(os.path.abspath(__file__))
path = pathlib.Path(current_dir)
parent_dir = path.parent.parent
# print(parent_dir)
locations_dir = os.path.join(parent_dir, "locations")
# print(locations_dir)
sys.path.insert(0, locations_dir)
# print(sys.path)
from locations import Location, LOCATIONS


# TODO Can this be shared with the scrapers? SSOT
DATA_DIRECTORY = "../data"


class SensorHeader:
    def __init__(self):
        # Hardcoded for now.
        self.columns = ["Time","Temperature","Humidity"]


class SensorEntry:
    def __init__(self, date_time: datetime.datetime, temperature :float, humidity :float):
        self.date_time = date_time
        self.temperature = temperature
        self.humidity = humidity


class SensorResults:
    def __init__(self, location: str):
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
    file_name += location + ".csv"
    with open(file_name, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
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
                temperature_rounded = (round(float(row[1]), 1))
                humidity_rounded = (round(float(row[2]), 1))
                entry = SensorEntry(date_time, temperature_rounded, humidity_rounded)
                sensor_results.append(entry)
    return sensor_results


def load_results_for_location(path, location, date_from, date_to):
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
    combined_results = []
    for location in LOCATIONS:
        day_results = load_results_for_location(path, location,
                                                date_from, date_to)
        combined_results.append(day_results)
    return combined_results


def __build_description():
    """ Use locations package to build up the description. """
    description = {"date_time": ("date", "Time")}
    for location in LOCATIONS:
        print(location)
        print(location.name, location.label)
        description[location.name] = ("number", location.label)
    print(description)
    return description


def merge_results(raw_results, interval_minutes):
    description = __build_description()
    data = []
    for day_results in raw_results:
        location_results = day_results[1]
        # for sensor in
        # for location_data in location_results:
        #     location = location_data[0]
        #     # Add each sensor entry label to description
        #     description[location] = ("number", location.title())
    return (description, data)

    # Output format has to be.
    # description = {
    #     "time_of_day": ("timeofday", "Time"),
    #     "external": ("number", "External"),
    #     "sensor1": ("number", "Upstairs"),
    #     "sensor2": ("number", "Downstairs"),
    # }
    # data = [
    #     {
    #         "time_of_day": datetime.time(hour=11, minute=30),
    #         "external": 11.7,
    #         "sensor1": 18.8,
    #         "sensor2": 10.5,
    #     },
    # ]


def prepare_todays_results():
    # Work out today's date.
    today = datetime.date.today()
    file_today = today.isoformat()
    raw_contents = []
    # Read today's CSV files.
    for location in LOCATIONS:
        file_name = DATA_DIRECTORY + "/" + file_today + "-" + location + ".csv"
        contents = load_file(file_name)
        raw_contents.append(location, contents)
    # Merge data from all files.
    (description, data) = merge_results(raw_contents, 5)
    return (description, data)
