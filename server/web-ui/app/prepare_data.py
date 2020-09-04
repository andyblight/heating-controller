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
import locations

# TODO Can these be shared with the scrapers? SSOT
DATA_DIRECTORY = "../data"
#
LOCATIONS = [
    ["external"],
    ["downstairs-back-room"],
    ["upstairs-landing"],
]


def load_file(file_name):
    """ Loads a single file of results.
    Returns a structure containing:
    (header, contents)
    header = [header_column, ...]
    header_column = string: the value read from the column of the first row of
                    the file.
    contents = [entry, ...]
    entry = [datetime: time, float: temperature, float: humidity]
    """
    header = []
    contents = []
    with open(file_name, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        for row in csv_reader:
            # print(row)
            # Add first row as header.
            # Row format: Time,Temperature C,Humidity %
            if header == []:
                for value in row:
                    header.append(value)
            # Exclude header rows (there can be more than one).
            # First entry of header row is always "Time".
            if row[0] != "Time":
                # Extract time, temperature and humidity.
                entry = []
                time = datetime.datetime.strptime(row[0], "%H:%M").time()
                entry.append(time)
                entry.append(round(float(row[1]), 1))
                entry.append(round(float(row[2]), 1))
                contents.append(entry)
    return (header, contents)


def __load_day_results(path, file_date):
    # The CSV files all have the same format:
    # <ISO date>-<location>.csv
    day_contents = []
    file_date_iso = file_date.isoformat()
    for location in LOCATIONS:
        location_string = location[0]
        file_name = path + "/"
        file_name += file_date_iso + "-"
        file_name += location_string + ".csv"
        # print("Loading file:", file_name)
        contents = load_file(file_name)
        day_contents.append((location_string, contents))
    return day_contents


def load_results(path, date_from, date_to):
    """ Loads results for the given range of dates.
    Returns a structure containing:
    (result_date, day_contents)
    result_date = datetime.
    day_contents = (location, contents)
    location = string representing the location of the results.
    contents = the value returned by load_file().
    """
    # print(date_from, date_to)
    raw_contents = []
    step = datetime.timedelta(days=1)
    while date_from <= date_to:
        # print(date_from.strftime('%Y_%m_%d'))
        day_contents = __load_day_results(path, date_from)
        raw_contents.append((date_from, day_contents))
        date_from += step
    return raw_contents


def __build_description():
    """ Use locations package to build up the description. """
    description = {"date_time": ("date", "Time")}
    for location in LOCATIONS:
        description[location.name] = ("number", location.label)
    print(description)
    return description


def merge_results(raw_results, interval_minutes=5):
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
    #         "time_of_day": datetime.time(hour=8, minute=30),
    #         "external": 37.8,
    #         "sensor1": 80.8,
    #         "sensor2": 41.8,
    #     },
    #     {
    #         "time_of_day": datetime.time(hour=9, minute=30),
    #         "external": 30.9,
    #         "sensor1": 69.5,
    #         "sensor2": 32.4,
    #     },
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
