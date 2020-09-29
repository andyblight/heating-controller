#!/usr/bin/python3

import csv
import datetime
import os
import pathlib
import sys

# Add the locations directory to the system path so that the
# locations package can be imported.
__current_dir = os.path.dirname(os.path.abspath(__file__))
__path = pathlib.Path(__current_dir)
__parent_dir = __path.parent.parent
# print(__parent_dir)
__locations_dir = os.path.join(__parent_dir, "locations")
# print(locations_dir)
sys.path.insert(0, __locations_dir)
# print(sys.path)
from locations import Location, LOCATIONS  # noqa: E402

# File paths for charts.py to use.
__data_files_directory = os.path.join(__parent_dir, "data")
__temp_data_directory = os.path.join(__current_dir, "temp_data")
PATH_TODAY_HUMIDITY = os.path.join(__temp_data_directory, "today_humidity.csv")
PATH_TODAY_TEMPERATURE = os.path.join(__temp_data_directory, "today_temperature.csv")
PATH_SEVEN_DAY_HUMIDITY = os.path.join(__temp_data_directory, "seven_humidity.csv")
PATH_SEVEN_DAY_TEMPERATURE = os.path.join(
    __temp_data_directory, "seven_temperature.csv"
)


class SensorHeader:
    def __init__(self):
        # Hardcoded for now.
        self.columns = ["DateTime", "Temperature", "Humidity"]


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

    def append(self, entry: SensorEntry):
        self.entries.append(entry)

    def extend(self, day_results):
        if type(day_results) is not type(self):
            raise ValueError
        self.entries.extend(day_results.entries)

    def get(self, date_time):
        """Returns the first SensorEntry object that is equal to or greater
        than the given value of date_time.
        Returns None if there are no entries.
        """
        result = None
        for entry in self.entries:
            if entry.date_time >= date_time:
                result = entry
                break
        return result


def load_day_results(path, location, file_date):
    """Loads a single file (one day) of results for a single sensor.
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
    """Returns a SensorResults object containing the data for the given range
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
    """Returns a list of SensorResults objects, one per location.
    Each SensorResults object has the data for the given range of dates.
    """
    print("Loading results from ", date_from, " to ", date_to)
    all_results = []
    for location in LOCATIONS:
        day_results = load_results_for_location(path, location, date_from, date_to)
        all_results.append(day_results)
    return all_results


def merge_results(all_results, interval_minutes):
    """Merges all_results from external and all sensors into two lists, one
    for temperature and the other for humidity.
    all_results is a list of SensorResults.
    Each SensorResults object has a list of SensorEntry values.
    Each SensorResults object has to be iterated over for each location,
    adding the entry closest to the datetime being requested to the entry in
    the results dictionary.
    The entries in the lists are organised by time intervals.
    Each entry for humidity and temperature has the same order:
        [datetime, external, sensor1, sensor2]
    """
    humidity_results = []
    temperature_results = []
    # Use start and end times from external sensor data.
    external_entries = all_results[0].entries
    start_date = external_entries[0].date_time.date()
    end_date = external_entries[-1].date_time.date()
    end_date += datetime.timedelta(days=1)
    start_datetime = datetime.datetime.combine(start_date, datetime.time(0, 0))
    end_datetime = datetime.datetime.combine(end_date, datetime.time(0, 0))
    interval_timedelta = datetime.timedelta(minutes=interval_minutes)
    # Iterate by time intervals.
    # print("Start", start_datetime, ", End", end_datetime)
    while end_datetime > start_datetime:
        # print("Start", start_datetime)
        humidity_entry = []
        humidity_entry.append(start_datetime)
        temperature_entry = []
        temperature_entry.append(start_datetime)
        for location_results in all_results:
            # Look up entry using time as key into location dictionary.
            # datetime is ok to use as a key directly.
            # print(location_results.entries)
            location_entry = location_results.get(start_datetime)
            # print(location_entry.date_time)
            if location_entry:
                humidity_entry.append(location_entry.humidity)
                temperature_entry.append(location_entry.temperature)
        # Insert entries into results lists.
        humidity_results.append(humidity_entry)
        temperature_results.append(temperature_entry)
        # Next interval.
        start_datetime += interval_timedelta
    return (humidity_results, temperature_results)


def write_merged_results(results, file_path):
    """Writes the given results to a CSV file at the specified path.
    File has no header row.  Columns are:
        [datetime, external, sensor1, sensor2]
    """
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # The entries are in the correct order, so write it to file.
        for entry in results:
            writer.writerow(entry)


def create_files_today():
    """Creates two results files (temperature and humidity) from external and
    other sensor data files.
    The columns in each results file are:
        datetime, external, <sensor1 location name>, ..., <sensorN location name>
    """
    today = datetime.date.today()
    interval_minutes = 10
    all_results = load_results(__data_files_directory, today, today)
    (humidity_results, temperature_results) = merge_results(
        all_results, interval_minutes
    )
    write_merged_results(humidity_results, PATH_TODAY_HUMIDITY)
    write_merged_results(temperature_results, PATH_TODAY_TEMPERATURE)


def create_files_seven_days():
    """Creates two results files (temperature and humidity) from external and
    other sensor data files for the previous seven days (not including today).
    The columns in each results file are:
        datetime, external, <sensor1 location name>, ..., <sensorN location name>
    """
    today = datetime.date.today()
    datetime_from = datetime.datetime.combine(today, datetime.time(0, 0))
    datetime_to = datetime_from + datetime.timedelta(days=7)
    interval_minutes = 60
    all_results = load_results(__data_files_directory, datetime_from, datetime_to)
    (humidity_results, temperature_results) = merge_results(
        all_results, interval_minutes
    )
    write_merged_results(humidity_results, PATH_SEVEN_DAY_HUMIDITY)
    write_merged_results(temperature_results, PATH_SEVEN_DAY_TEMPERATURE)
