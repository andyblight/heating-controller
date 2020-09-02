from flask import render_template
from flask_table import Table, Col
import gviz_api
from app import app


class SensorTable(Table):
    name = Col("Name")
    temperature = Col("Temperature C")
    humidity = Col("Humidity %")


# Sensor values
class Sensor():
    def __init__(self, name, temperature, humidity):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity


@app.route('/')
@app.route('/index')
def index():
    sensor_values = [
        Sensor("External", 30, 90),
        Sensor("Upstairs", 27, 80),
        Sensor("Downstairs", 25, 70),
    ]
    return render_template(
        'index.html',
        title='Home',
        table=SensorTable(sensor_values))


@app.route('/charts')
def charts():
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
    chart_seven = gviz_api.DataTable(description)
    chart_seven.LoadData(data)
    jscode_seven = chart_seven.ToJSCode('jscode_chart_seven',
                                       columns_order=('day',
                                                'guardians',
                                                 'avengers',
                                                 'transformers'))
    chart_thirty = gviz_api.DataTable(description)
    chart_thirty.LoadData(data)
    jscode_thirty = chart_thirty.ToJSCode('jscode_chart_thirty',
                                        columns_order=('day',
                                                'guardians',
                                                 'avengers',
                                                 'transformers'))
    return render_template(
        'charts.html',
        title='Charts', jscode_chart_today=jscode_today, jscode_chart_seven=jscode_seven, jscode_chart_thirty=jscode_thirty)
