import requests
from bs4 import BeautifulSoup


URLS = ['http://192.168.2.63', 'http://192.168.2.64']


def extract_readings(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    # Temperature
    temperature_item = soup.find(id='temperature')
    temperature_pretty = temperature_item.prettify()
    temperature_parts = temperature_pretty.split("\n")
    temperature = float(temperature_parts[1])
    # print("temperature", temperature)
    # Humidity
    humidity_item = soup.find(id='humidity')
    humidity_pretty = humidity_item.prettify()
    humidity_parts = humidity_pretty.split("\n")
    humidity = float(humidity_parts[1])
    # print("humidity", humidity)
    return (temperature, humidity)


for url in URLS:
    try:
        response = requests.get(url)
        readings = extract_readings(response)
        print("URL", url, "readings", readings)
    except requests.exceptions.RequestException as e:
        _ = e  # sprint(e)
        print("URL", url, "no response")
