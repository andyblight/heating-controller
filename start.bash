#!/bin/bash

bash -c 'nohup python3 server/scrapers/record-temps.py &>/dev/null' &
bash -c 'nohup python3 server/scrapers/current-weather.py &>/dev/null' &

