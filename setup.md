# Set up

## Configure the sensors

### Load and test the software

The NodeMCU temperature and humidity sensors need to have the software
installed using the Arduino IDE.  The software is in the directory
`nodemcu/nodemcu-dth22`.  Copy this directory to the `~/Arduino/code/` and
start the Arudino IDE.  Select the board type `NodeMCU 1.0 (EPS12E Module)`.
Open the file `File>Sketchbook>code>nodemcu-dth22`.  Connect the NodeMCU to the
PC using the USB lead.  Make sure that the Arduino IDE has detected the NodeMCU
being plugged in by going to `Tools>Port` and making sure `/dev/ttyUSB0` is
shown (`/dev/ttyUSB1` is also fine).  Then upload the software.

You can verify correct operation using `Tools>Serial Monitor`.  The defaults
should work (Newline, 115200 baud).  Unplug and plug in the NodeMCU and you
should see something like this:

```text
Connected: IPv4: 192.168.2.180, Hostname: Sensor5F1644
20.00
75.10
20.00
76.30
```

Note: the IP address may be different.

### Add MAC address rule to router

To fix the IP address of each sensor so that they can be read by the scraper
software, MAC address rules on the router are used.

1. On my Virgin Hub 3.0, login to the admin screen.
1. Click `Advanced settings>DHCP`.
1. Find the sensor in the list of attached devices.  The device name has the
format `SensorXXXXXX` where the `XXXXX` is the last 6 characters of the MAC
address.
1. Select the sensor in the list.  This populates the `Add reserved rule`
section at the bottom of the page (scroll down!).  Set the desired IP address
and click `Add rule`.  The router says `Please wait` for a while and then the
MAC address rule has been added to the `Reserved list` at the bottom of the
page.
1. Finally, as the NodeMCUs are too dumb to pick up the rule change, power
cycle the NodeMCU and verify that you can connect to it using the newly
allocated IP address.

## Configure the server

TODO
