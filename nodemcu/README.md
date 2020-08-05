# NodeMCU sensors

The NodeMCUs are used for the temperature and humidity sensors and publish
their information using a built in web server.

## Parts

For each sensor:

| Number | Item | Source |
| ------ | ---- | ------ |
| 1 | NodeMCU ESP8266 Development Board | <https://smile.amazon.co.uk/gp/product/B074Q2WM1Y/> |
| 1 | DHT22 Temperature and humidity sensor | <https://smile.amazon.co.uk/gp/product/B072391SJV/> |
| 1 | USB micro to USB A cable | Whatever length you need. |
| 1 | USB plugtop | To supply 500mA minimum. |

## Hardware assembly

The article I followed is here: <https://randomnerdtutorials.com/esp8266-dht11dht22-temperature-and-humidity-web-server-with-arduino-ide/>

The good thing about the DTH22 units I ordered is that the pull up resistor is
built into the board and they also come with a suitable jumper cable.  All you
have to do is to plug it together.

## Programming

The most time consuming part is setting up the Arduino IDE for use with the
ESP8266.  I followed this guide <https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/>.
I followed the LED blink example and made it work.

Then I went back to the first guide, <https://randomnerdtutorials.com/esp8266-dht11dht22-temperature-and-humidity-web-server-with-arduino-ide/>.
After connecting the DTH22, I installed the Adafruit sensor libraries and the
ESPAsyncWebServer libraries.  I then added the code to the project and after
programming, it worked first time.  Amazing!

## To program the NodeMCU

### Initial configuration

### Loading the program

The source code is in the `nodemcu-dht22` directory.  Copy this directory into
your `~/Arduino/code/` directory and change the SSID and password near the top
of the file to suit your network.

Use the Arduino ID to load the program.

The NodeMCU software gets an IPv4 address from the network DHCP server.  The IP
address is printed out on the Arduino serial monitor program. Use this value
to access the web page, e.g. the IP address of one of my units was
`192.168.2.64` so I used <http://192.168.2.64> in my browser.  You should see
a page showing the temperatue and humidity.

NOTE: Refreshing the web page at intervals of less than 2 seconds can cause the
program to fail requiring a power cycle to fix it.

### Final configuration

To ensure the scraper program can find the sensors, the IP addresses must be
fixed.  I did this by adding a reserved rule to my router based on the MAC
address of the sensor.
