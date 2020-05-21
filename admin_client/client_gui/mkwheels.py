#! /usr/bin/bash
python3 -m venv venv
source venv/bin/activate
python3 setup.py sdist bdist_wheel
