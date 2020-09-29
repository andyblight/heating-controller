#!/bin/bash
set -ex

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &>/dev/null  && pwd )"
#echo "THIS_DIR = $THIS_DIR"
VENV_DIR=${THIS_DIR}/../venv

sudo apt install -y python3-pip python3-venv
python3 -m venv ${VENV_DIR}
source ${VENV_DIR}/bin/activate
pip3 install wheel
pip install -r ${THIS_DIR}/requirements.txt
.