#!/bin/bash
set -e

sudo apt install -y python3-pip
pip3 install wheel
python3 -m venv ../venv
source ../venv/bin/activate
pip install -r requirements.txt
