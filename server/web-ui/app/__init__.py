from flask import Flask
from config import Config
import gviz_api


app = Flask(__name__)
app.config.from_object(Config)


def chart_today():
    description = {'day': ('number', 'Day'),
                   'guardians': ('number', 'Guardians of the Galaxy'),
                   'avengers': ('number', 'The Avengers'),
                   'transformers': ('number', 'Transformers: Age of Extinction')}
    data = [
        {'day':  1, 'guardians': 37.8, 'avengers': 80.8, 'transformers': 41.8},
        {'day':  2, 'guardians': 30.9, 'avengers': 69.5, 'transformers': 32.4},
        {'day':  3, 'guardians': 25.4, 'avengers': 57.0, 'transformers': 25.7},
        {'day':  4, 'guardians': 11.7, 'avengers': 18.8, 'transformers': 10.5},
    ]
    chart_today = gviz_api.DataTable(description)
    chart_today.LoadData(data)
    jscode_today = chart_today.ToJSCode('jscode_chart_today',
                                        columns_order=('day',
                                                'guardians',
                                                 'avengers',
                                                 'transformers'))
    return jscode_today


def chart_seven_days():
    description = {'day': ('number', 'Day'),
                   'guardians': ('number', 'Guardians of the Galaxy'),
                   'avengers': ('number', 'The Avengers'),
                   'transformers': ('number', 'Transformers: Age of Extinction')}
    data = [
        {'day':  1, 'guardians': 37.8, 'avengers': 80.8, 'transformers': 41.8},
        {'day':  2, 'guardians': 30.9, 'avengers': 69.5, 'transformers': 32.4},
        {'day':  3, 'guardians': 25.4, 'avengers': 57.0, 'transformers': 25.7},
        {'day':  4, 'guardians': 11.7, 'avengers': 18.8, 'transformers': 10.5},
    ]
    chart_seven = gviz_api.DataTable(description)
    chart_seven.LoadData(data)
    jscode_seven = chart_seven.ToJSCode('jscode_chart_seven',
                                       columns_order=('day',
                                                'guardians',
                                                 'avengers',
                                                 'transformers'))
    return jscode_seven


def chart_thirty_days():
    description = {'day': ('number', 'Day'),
                   'guardians': ('number', 'Guardians of the Galaxy'),
                   'avengers': ('number', 'The Avengers'),
                   'transformers': ('number', 'Transformers: Age of Extinction')}
    data = [
        {'day':  1, 'guardians': 37.8, 'avengers': 80.8, 'transformers': 41.8},
        {'day':  2, 'guardians': 30.9, 'avengers': 69.5, 'transformers': 32.4},
        {'day':  3, 'guardians': 25.4, 'avengers': 57.0, 'transformers': 25.7},
        {'day':  4, 'guardians': 11.7, 'avengers': 18.8, 'transformers': 10.5},
    ]
    chart_thirty = gviz_api.DataTable(description)
    chart_thirty.LoadData(data)
    jscode_thirty = chart_thirty.ToJSCode('jscode_chart_thirty',
                                        columns_order=('day',
                                                'guardians',
                                                 'avengers',
                                                 'transformers'))
    return jscode_thirty


from app import routes  # noqa: 401
