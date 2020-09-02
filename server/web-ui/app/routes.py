from flask import render_template
from flask_table import Table, Col
from flask_googlecharts import LineChart
from app import app, charts


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
    my_chart = LineChart("my_chart", options={"title": "MyChart"})
    my_chart.add_column("string", "Competitor")
    my_chart.add_column("number", "Hot Dogs")
    my_chart.add_rows([["Matthew Stonie", 62],
                       ["Joey Chestnut", 60],
                       ["Eater X", 35.5],
                       ["Erik Denmark", 33],
                       ["Adrian Morgan", 31]])
    return render_template(
        'charts.html',
        title='Charts', chart_fn=charts, my_chart=my_chart)
