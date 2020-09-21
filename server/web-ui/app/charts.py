import datetime
import gviz_api


def chart_today_temperature():
    # TODO Get data from somewhere.
    # Convert into
    description = {
        "time_of_day": ("timeofday", "Time"),
        "external": ("number", "External"),
        "sensor1": ("number", "Upstairs"),
        "sensor2": ("number", "Upstairs"),
    }
    data = [
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
    chart = gviz_api.DataTable(description)
    chart.LoadData(data)
    jscode_today_temperature = chart.ToJSCode(
        "jscode_chart_today_temperature",
        columns_order=("time_of_day", "external", "sensor1", "sensor2")
    )
    return jscode_today_temperature


def chart_today_humidity():
    # TODO Get data from somewhere.
    # Convert into
    description = {
        "time_of_day": ("timeofday", "Time"),
        "external": ("number", "External"),
        "sensor1": ("number", "Upstairs"),
        "sensor2": ("number", "Upstairs"),
    }
    data = [
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
    chart = gviz_api.DataTable(description)
    chart.LoadData(data)
    jscode_today_humidity = chart.ToJSCode(
        "jscode_chart_today_humidity",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_today_humidity


def chart_seven_temperature():
    # TODO Get data from somewhere.
    # Convert into
    description = {
        "time_of_day": ("timeofday", "Time"),
        "external": ("number", "External"),
        "sensor1": ("number", "Upstairs"),
        "sensor2": ("number", "Upstairs"),
    }
    data = [
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
    chart = gviz_api.DataTable(description)
    chart.LoadData(data)
    jscode_seven_temperature = chart.ToJSCode(
        "jscode_chart_seven_temperature",
        columns_order=("time_of_day", "external", "sensor1", "sensor2")
    )
    return jscode_seven_temperature


def chart_seven_humidity():
    # TODO Get data from somewhere.
    # Convert into
    description = {
        "time_of_day": ("timeofday", "Time"),
        "external": ("number", "External"),
        "sensor1": ("number", "Upstairs"),
        "sensor2": ("number", "Upstairs"),
    }
    data = [
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
    chart = gviz_api.DataTable(description)
    chart.LoadData(data)
    jscode_seven_humidity = chart.ToJSCode(
        "jscode_chart_seven_humidity",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_seven_humidity
