import datetime
import gviz_api


def chart_today():
    # Work out today's date.
    # Read today's CSV files.
    # Merge data
    description = {
        "time_of_day": ("timeofday", "Time"),
        "external": ("number", "External"),
        "sensor1": ("number", "Upstairs"),
        "sensor2": ("number", "Downstairs"),
    }
    data = [
        {
            "time_of_day": datetime.time(hour=8, minute=30),
            "external": 37.8,
            "sensor1": 80.8,
            "sensor2": 41.8,
        },
        {
            "time_of_day": datetime.time(hour=9, minute=30),
            "external": 30.9,
            "sensor1": 69.5,
            "sensor2": 32.4,
        },
        {
            "time_of_day": datetime.time(hour=10, minute=30),
            "external": 25.4,
            "sensor1": 57.0,
            "sensor2": 25.7,
        },
        {
            "time_of_day": datetime.time(hour=11, minute=30),
            "external": 11.7,
            "sensor1": 18.8,
            "sensor2": 10.5,
        },
    ]
    chart_today = gviz_api.DataTable(description)
    chart_today.LoadData(data)
    jscode_today = chart_today.ToJSCode(
        "jscode_chart_today",
        columns_order=("time_of_day", "external", "sensor1", "sensor2"),
    )
    return jscode_today


def chart_seven_days():
    description = {
        "day": ("number", "Day"),
        "guardians": ("number", "Guardians of the Galaxy"),
        "avengers": ("number", "The Avengers"),
        "transformers": ("number", "Transformers: Age of Extinction"),
    }
    data = [
        {"day": 1, "guardians": 37.8, "avengers": 80.8, "transformers": 41.8},
        {"day": 2, "guardians": 30.9, "avengers": 69.5, "transformers": 32.4},
        {"day": 3, "guardians": 25.4, "avengers": 57.0, "transformers": 25.7},
        {"day": 4, "guardians": 11.7, "avengers": 18.8, "transformers": 10.5},
    ]
    chart_seven = gviz_api.DataTable(description)
    chart_seven.LoadData(data)
    jscode_seven = chart_seven.ToJSCode(
        "jscode_chart_seven",
        columns_order=("day", "guardians", "avengers", "transformers"),
    )
    return jscode_seven


def chart_thirty_days():
    description = {
        "day": ("number", "Day"),
        "guardians": ("number", "Guardians of the Galaxy"),
        "avengers": ("number", "The Avengers"),
        "transformers": ("number", "Transformers: Age of Extinction"),
    }
    data = [
        {"day": 1, "guardians": 37.8, "avengers": 80.8, "transformers": 41.8},
        {"day": 2, "guardians": 30.9, "avengers": 69.5, "transformers": 32.4},
        {"day": 3, "guardians": 25.4, "avengers": 57.0, "transformers": 25.7},
        {"day": 4, "guardians": 11.7, "avengers": 18.8, "transformers": 10.5},
    ]
    chart_thirty = gviz_api.DataTable(description)
    chart_thirty.LoadData(data)
    jscode_thirty = chart_thirty.ToJSCode(
        "jscode_chart_thirty",
        columns_order=("day", "guardians", "avengers", "transformers"),
    )
    return jscode_thirty
