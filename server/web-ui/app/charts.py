import csv
import datetime
import gviz_api
import os
import app.prepare_data as pd


# Common description used to create the charts.
description = {
    "time_of_day": ("timeofday", "Time"),
    "external": ("number", "External"),
    "sensor1": ("number", "Downstairs"),
    "sensor2": ("number", "Upstairs"),
}


def __convert_row(row):
    """ A row looks like this:
      ['2020-09-22 08:30:00', '15.4', '20.1', '22.3']
    and needs to be formatted like this:
        {
            "time_of_day": datetime.datetime(2020, 9, 22, 8, 30),
            "external": 15.4,
            "sensor1": 20.1,
            "sensor2": 22.3,
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
    # print()
    # print(file_name)
    file_exists = os.path.isfile(file_name)
    if file_exists:
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                # print(row)
                entry = __convert_row(row)
                data.append(entry)
    else:
        # TODO Do something useful here
        print("File:", file_name, "not found.")
    # print(data)
    return data


def chart_today_temperature():
    chart = gviz_api.DataTable(description)
    pd.create_files_today()
    data = load_data_file(pd.PATH_TODAY_TEMPERATURE)
    chart.LoadData(data)
    jscode_today_temperature = chart.ToJSCode(
        "jscode_chart_today_temperature",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_today_temperature


def chart_today_humidity():
    chart = gviz_api.DataTable(description)
    pd.create_files_today()
    data = load_data_file(pd.PATH_TODAY_HUMIDITY)
    chart.LoadData(data)
    jscode_today_humidity = chart.ToJSCode(
        "jscode_chart_today_humidity",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_today_humidity


def chart_seven_temperature():
    chart = gviz_api.DataTable(description)
    data = load_data_file(pd.PATH_SEVEN_DAY_TEMPERATURE)
    chart.LoadData(data)
    jscode_seven_temperature = chart.ToJSCode(
        "jscode_chart_seven_temperature",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_seven_temperature


def chart_seven_humidity():
    chart = gviz_api.DataTable(description)
    data = load_data_file(pd.PATH_SEVEN_DAY_HUMIDITY)
    chart.LoadData(data)
    jscode_seven_humidity = chart.ToJSCode(
        "jscode_chart_seven_humidity",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_seven_humidity
