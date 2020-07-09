import csv
from datetime import datetime
import requests
import sched
import time

# pip3 imports
from bs4 import BeautifulSoup

LOCATIONS = [["http://192.168.2.63", "Upstairs"], ["http://192.168.2.64", "Downstairs"]]
INTERVAL_TIME_S = 5

# Set up scheduler
scheduler = sched.scheduler(time.time, time.sleep)


def extract_readings(page):
    soup = BeautifulSoup(page.content, "html.parser")
    # Temperature
    temperature_item = soup.find(id="temperature")
    temperature_pretty = temperature_item.prettify()
    temperature_parts = temperature_pretty.split("\n")
    temperature = float(temperature_parts[1])
    # print("temperature", temperature)
    # Humidity
    humidity_item = soup.find(id="humidity")
    humidity_pretty = humidity_item.prettify()
    humidity_parts = humidity_pretty.split("\n")
    humidity = float(humidity_parts[1])
    # print("humidity", humidity)
    return (temperature, humidity)


def get_pages(csv_file, csv_writer):
    for url, location in LOCATIONS:
        try:
            response = requests.get(url)
            (temperature, humidity) = extract_readings(response)
            time_now = datetime.now()
            timestamp_seconds = int(time_now.timestamp())
            print("{0:12d} {1:10s}: {2:4}C, {3:4}%".format(timestamp_seconds, location, temperature, humidity))
            csv_writer.writerow([timestamp_seconds, location, temperature, humidity])
            csv_file.flush()
        except requests.exceptions.RequestException as e:
            _ = e  # print(e)
            print(location, "no response")
    # Queue next action.
    scheduler.enter(INTERVAL_TIME_S, 1, get_pages, argument=(csv_file, csv_writer,))


def main():
    # Open CSV file.
    with open("temperatures.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerow(["Timestamp", "Location", "Temperature", "Humidity"])
        # Get pages.
        get_pages(csv_file, csv_writer)
        # Run until all actions complete.
        scheduler.run()


if __name__ == "__main__":
    main()

# Add location to each URL. DONE.
# Get pages every 1 minute. DONE.
# Save readings to file with location and time stamp. DONE.
