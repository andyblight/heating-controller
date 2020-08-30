from flask import render_template
from flask_table import Table, Col
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
