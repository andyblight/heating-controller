import requests
from bs4 import BeautifulSoup

URL = 'http://192.168.2.63'

def get_readings():
    page = requests.get(URL)
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


readings = get_readings()
print("Readings", readings)
