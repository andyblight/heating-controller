#!/usr/bin/env python3

import csv
from datetime import datetime, date
import requests
import sched
import time

# pip3 imports
from bs4 import BeautifulSoup

from locations import DATA_DIRECTORY

# INTERVAL_TIME_S = 5
INTERVAL_TIME_S = 60 * 5

# Set up scheduler
scheduler = sched.scheduler(time.time, time.sleep)


class TemperatureReader:
    def __init__(self, location, url):
        self.location = location
        self.url = url
        self.temperature = 0
        self.humidity = 0
        self.csv_file = None
        self.csv_writer = None
        self.today = 0

    def open_file(self):
        self.today = date.today()
        file_name = DATA_DIRECTORY + "/" + self.today.isoformat() + "-" + self.location + ".csv"
        self.csv_file = open(file_name, "a", newline="")
        self.csv_writer = csv.writer(
            self.csv_file, delimiter=",", quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )
        self.csv_writer.writerow(["Time", "Temperature", "Humidity"])
        self.csv_file.flush()

    def close_file(self):
        self.csv_writer = None
        self.csv_file.close()

    def extract_readings(self, page):
        soup = BeautifulSoup(page.content, "html.parser")
        # Temperature
        temperature_item = soup.find(id="temperature")
        temperature_pretty = temperature_item.prettify()
        temperature_parts = temperature_pretty.split("\n")
        self.temperature = float(temperature_parts[1])
        # print("temperature", temperature)
        # Humidity
        humidity_item = soup.find(id="humidity")
        humidity_pretty = humidity_item.prettify()
        humidity_parts = humidity_pretty.split("\n")
        self.humidity = float(humidity_parts[1])
        # print("humidity", humidity)

    def write_to_file(self):
        time_now = datetime.now()
        time_str = time_now.strftime("%H:%M")
        # print(
        #     "{0:5s} {1:20s}: {2:4}C, {3:4}%".format(
        #         time_str, self.location, self.temperature, self.humidity
        #     )
        # )
        self.csv_writer.writerow([time_str, self.temperature, self.humidity])
        self.csv_file.flush()

    def get_temps(self):
        try:
            page = requests.get(self.url)
            self.extract_readings(page)
            self.write_to_file()
        except requests.exceptions.RequestException as e:
            print(self.location, "no response", e)

    def change_files(self):
        today = date.today()
        if self.today != today:
            self.close_file()
            self.open_file()


def timed_read(readers):
    for reader in readers:
        reader.change_files()
        reader.get_temps()
    # Queue next action.
    scheduler.enter(INTERVAL_TIME_S, 1, timed_read, argument=(readers,))


def main():
    readers = []
    for location, ip_address in LOCATIONS:
        reader = TemperatureReader(location, ip_address)
        reader.open_file()
        readers.append(reader)
    # Get pages.
    timed_read(readers)
    # Run until all actions complete.
    scheduler.run()


if __name__ == "__main__":
    main()

# Add location to each URL. DONE.
# Get pages every 1 minute. DONE.
# Save readings to file with location and time stamp. DONE.
# Create daily file for each location. DONE.
# Change timestamp to human readable times. DONE.
# Auto change over of files at midnight. DONE.
