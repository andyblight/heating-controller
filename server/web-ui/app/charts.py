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


# def chart_thirty_days():
#     description = {
#         "day": ("number", "Day"),
#         "guardians": ("number", "Guardians of the Galaxy"),
#         "avengers": ("number", "The Avengers"),
#         "transformers": ("number", "Transformers: Age of Extinction"),
#     }
#     data = [
#         {"day": 1, "guardians": 37.8, "avengers": 80.8, "transformers": 41.8},
#         {"day": 2, "guardians": 30.9, "avengers": 69.5, "transformers": 32.4},
#         {"day": 3, "guardians": 25.4, "avengers": 57.0, "transformers": 25.7},
#         {"day": 4, "guardians": 11.7, "avengers": 18.8, "transformers": 10.5},
#     ]
#     chart_thirty = gviz_api.DataTable(description)
#     chart_thirty.LoadData(data)
#     jscode_thirty = chart_thirty.ToJSCode(
#         "jscode_chart_thirty",
#         columns_order=("day", "guardians", "avengers", "transformers"),
#     )
#     return jscode_thirty
