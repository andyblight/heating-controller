#!/usr/bin/env python3
# Based on:
# https://stackoverflow.com/questions/61358322/web-scrapping-specific-data-from-openweather-one-call-api-into-csv-file

import csv
from datetime import datetime, date
import requests
import sched
import time

# pip3 imports
from bs4 import BeautifulSoup
import pandas


INTERVAL_TIME_S = 5
# INTERVAL_TIME_S = 60 * 5

# API call.
# Tested this using a browser.
OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?id=2640132&appid="
API_KEY_FILE = "/home/andy/secrets/open-weather-api-key"
DEGREES_KELVIN = 273.15

# Set up scheduler
scheduler = sched.scheduler(time.time, time.sleep)

f_csv_file = None
f_csv_writer = None
f_today = None


def read_api_key():
    api_key = ""
    with open(API_KEY_FILE, "r") as key_file:
        api_key = key_file.read()
    return api_key

def open_file():
    # print("of")
    global f_today, f_csv_file, f_csv_writer
    f_today = date.today()
    file_name = f_today.isoformat() + "-external" + ".csv"
    try:
        f_csv_file = open(file_name, "w", newline="")
        f_csv_writer = csv.writer(
            f_csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        f_csv_writer.writerow(
            ["Time", "Temperature C", "Humidity %", "Wind m/s", "Gust m/s"]
        )
    except OSError as err:
        print("OS error: {0}".format(err))
    # print("f_today", f_today)


def close_file():
    # print("clf")
    global f_csv_file, f_csv_writer
    f_csv_writer = None
    if f_csv_file:
        f_csv_file.close()


def write_to_file(temperature, humidity, wind, degrees, gust):
    # print("wtf")
    global f_csv_file, f_csv_writer
    time_now = datetime.now()
    time_str = time_now.strftime("%H:%M")
    f_csv_writer.writerow([time_str, temperature, humidity, wind, degrees, gust])
    f_csv_file.flush()


def change_file():
    # print("chf")
    global f_today
    today = date.today()
    # print("f_today", f_today, "today", today)
    if f_today != today:
        close_file()
        open_file()


def get_current_weather():
    api_key = read_api_key()
    # print("api key:", api_key)
    url = OPEN_WEATHER_URL + api_key
    # print("url:", url)
    json_data = requests.get(url).json()
    # print(json_data)
    df = pandas.DataFrame(json_data["main"], index=[0])
    # print(df.to_string())
    #     temp  feels_like  temp_min  temp_max  pressure  humidity
    # 0  293.4      292.37    291.48    295.37      1025        46
    temperature = df["temp"][0] - DEGREES_KELVIN
    humidity = df["humidity"][0]
    # print("temperature {:.1f}C, humidity {:d}%".format(temperature, humidity))
    df = pandas.DataFrame(json_data["wind"], index=[0])
    # print(df.to_string())
    #    speed  deg  gust
    # 0   0.89  266  2.68
    wind_speed = df["speed"][0]
    wind_degrees = df["deg"][0]
    try:
        wind_gust = df["gust"][0]
    except KeyError:
        wind_gust = 0.0
    # print(
    #     "wind speed {:.2f}, degrees {:d}, gust {:.2f}".format(
    #         wind_speed, wind_degrees, wind_gust
    #     )
    # )
    write_to_file(temperature, humidity, wind_speed, wind_degrees, wind_gust)


def timed_read():
    change_file()
    get_current_weather()
    # Queue next action.
    scheduler.enter(INTERVAL_TIME_S, 1, timed_read)


def main():
    open_file()
    # Get pages.
    timed_read()
    # Run until all actions complete.
    scheduler.run()


if __name__ == "__main__":
    main()

