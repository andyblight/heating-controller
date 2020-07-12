#!/usr/bin/env python3
# Based on:
# https://stackoverflow.com/questions/61358322/web-scrapping-specific-data-from-openweather-one-call-api-into-csv-file

import requests
import sched
import time

# pip3 imports
from bs4 import BeautifulSoup
import pandas


INTERVAL_TIME_S = 5
# INTERVAL_TIME_S = 60

# API call.
# Tested this using a browser.
OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?id=2640132&appid=96f114b6e51c0d7e6de6f4f19dd522ee"

# Set up scheduler
scheduler = sched.scheduler(time.time, time.sleep)


def get_current_weather():
    json_data = requests.get(OPEN_WEATHER_URL).json()
    print(json_data)
    df = pandas.DataFrame(json_data['main'],index=[0])
    print(df.to_string())
    df = pandas.DataFrame(json_data['wind'],index=[0])
    print(df.to_string())


def timed_read():
    get_current_weather()
    # Queue next action.
    scheduler.enter(INTERVAL_TIME_S, 1, timed_read)


def main():
    # Get pages.
    timed_read()
    # Run until all actions complete.
    scheduler.run()


if __name__ == "__main__":
    main()

