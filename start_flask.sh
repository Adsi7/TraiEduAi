#!/bin/bash

echo "starting..."
python3 -m venv env
source env/bin/activate
pip3 install flask
flask run
