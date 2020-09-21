from flask import render_template
from flask_table import Table, Col
from app import app
from app.charts import chart_today_temperature, chart_today_humidity, chart_seven_temperature, chart_seven_humidity


class SensorTable(Table):
    name = Col("Name")
    temperature = Col("Temperature C")
    humidity = Col("Humidity %")


# Sensor values
class Sensor:
    def __init__(self, name, temperature, humidity):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity


@app.route("/")
@app.route("/index")
def index():
    sensor_values = [
        Sensor("External", 30, 90),
        Sensor("Upstairs", 27, 80),
        Sensor("Downstairs", 25, 70),
    ]
    return render_template("index.html", title="Home", table=SensorTable(sensor_values))


@app.route("/today")
def today():
    jscode_today_temperature = chart_today_temperature()
    jscode_today_humidity = chart_today_humidity()
    return render_template(
        "today.html",
        title="Today",
        jscode_chart_today_temperature=jscode_today_temperature,
        jscode_chart_today_humidity=jscode_today_humidity,
    )


@app.route("/seven")
def seven():
    jscode_seven_temperature = chart_seven_temperature()
    jscode_seven_humidity = chart_seven_humidity()
    return render_template(
        "seven.html",
        title="Last seven days",
        jscode_chart_seven_temperature=jscode_seven_temperature,
        jscode_chart_seven_humidity=jscode_seven_humidity,
    )
