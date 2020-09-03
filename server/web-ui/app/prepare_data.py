#!/usr/bin/python3

import csv
import datetime

# TODO Can these be shared with the scrapers? SSOT
DATA_DIRECTORY = "../data"
LOCATIONS = [
    # The CSV files all have the same format:
    # <ISO date>-<location>.csv
    ["external"],
    ["downstairs-back-room"],
    ["upstairs-landing"],
]


def load_file(file_name):
    header = []
    contents = []
    with open(file_name, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        for row in csv_reader:
            print(row)
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
                entry.append(row[0])
                entry.append(row[1])
                entry.append(row[2])
                contents.append(entry)
    return (header, contents)


def merge_results(raw_contents, interval_minutes):
    description = {"time_of_day": ("timeofday", "Time")}
    data = []
    for location_contents in raw_contents:
        # location_contents contains (location, (header, data)).
        # Add each sensor entry.
        location = location_contents[0]
        description[location] = ("number", location.title())
        # Copy time and temperature data. Entries are roughly aligned using the
        # time values in each row of data.
        # Assume that entries are always data[0] = time, data[1] = temperature.
        # Could parse header but too lazy!
        raw_data = location_contents[1][1]
        for row in raw_data:
            pass
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
