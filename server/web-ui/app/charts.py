import csv
import datetime
import gviz_api
import os
import app.prepare_data

description = {
    "time_of_day": ("timeofday", "Time"),
    "external": ("number", "External"),
    "sensor1": ("number", "Upstairs"),
    "sensor2": ("number", "Upstairs"),
}

temperature_data = [
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

humidity_data = [
    {
        "time_of_day": datetime.time(hour=8, minute=30),
        "external": 70.5,
        "sensor1": 80.8,
        "sensor2": 81.2,
    },
    {
        "time_of_day": datetime.time(hour=9, minute=30),
        "external": 67.5,
        "sensor1": 80.8,
        "sensor2": 81.2,
    },
    {
        "time_of_day": datetime.time(hour=10, minute=30),
        "external": 64.5,
        "sensor1": 80.8,
        "sensor2": 81.2,
    },
    {
        "time_of_day": datetime.time(hour=11, minute=30),
        "external": 60.5,
        "sensor1": 80.8,
        "sensor2": 81.2,
    },
]

def __convert_row(row):
    """ A row looks like this:
      ['2020-09-22 08:30:00', '15.4', '20.1', '22.3']
    and needs to be formatted like this:
        {
            "time_of_day": datetime.time(hour=11, minute=30),
            "external": 60.5,
            "sensor1": 80.8,
            "sensor2": 81.2,
        }
    """
    entry = {}
    date_time = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
    entry["time_of_day"] = date_time
    entry["external"] = float(row[1])
    entry["sensor1"] = float(row[2])
    entry["sensor2"] = float(row[3])
    return entry


def load_data_file(file_name):
    """ This loads the specified CSV file filling out an object containing the
    data in the required format for passing to the charts.  As the temperature
    and humidity have the same description, this function can be used for both
    data sets.
    """
    data = []
    print()
    print(file_name)
    file_exists = os.path.isfile(file_name)
    if file_exists:
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                print(row)
                entry = __convert_row(row)
                data.append(entry)
    else:
        # TODO Do something useful here
        print("File:", file_name, "not found.")
    print(data)
    return data


def chart_today_temperature():
    chart = gviz_api.DataTable(description)
    # TODO Call function that returns temperature_data for today.
    # Function in prepare_data.py is called to create a CSV file.
    # The prepared CSV file is then loaded into temperature_data and returned.
    # prepare_data.create_files_today()
    # temperature_data = load_data_file("today_temperature.csv")
    chart.LoadData(temperature_data)
    jscode_today_temperature = chart.ToJSCode(
        "jscode_chart_today_temperature",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_today_temperature


def chart_today_humidity():
    chart = gviz_api.DataTable(description)
    # TODO Call function that returns humidity_data for today.
    chart.LoadData(humidity_data)
    jscode_today_humidity = chart.ToJSCode(
        "jscode_chart_today_humidity",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_today_humidity


def chart_seven_temperature():
    chart = gviz_api.DataTable(description)
    # TODO Call function that returns temperature_data for last seven days.
    # Data is read from a CSV file if present, else function in prepare_data.py
    # is called to create the CSV file and then read in.
    chart.LoadData(temperature_data)
    jscode_seven_temperature = chart.ToJSCode(
        "jscode_chart_seven_temperature",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_seven_temperature


def chart_seven_humidity():
    chart = gviz_api.DataTable(description)
    # TODO Call function that returns humidity_data for last seven days.
    chart.LoadData(humidity_data)
    jscode_seven_humidity = chart.ToJSCode(
        "jscode_chart_seven_humidity",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_seven_humidity
