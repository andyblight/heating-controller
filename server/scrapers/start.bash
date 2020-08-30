#!/bin/bash

bash -c 'nohup python3 ./record-temps.py &>/dev/null' &
bash -c 'nohup python3 ./current-weather.py &>/dev/null' &
