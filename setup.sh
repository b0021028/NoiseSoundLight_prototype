#!/bin/bash

sudo DEBIAN_FRONTEND=nointeractive apt install -y python3-setuptools python3-pip python3-venv portaudio19-dev python3-pigpio

# pigpio install
# wget https://github.com/joan2937/pigpio/archive/refs/tags/v79.tar.gz
# tar -xvf v79.tar.gz
# cd pigpio-79

# make
# sudo make install

# # check liblary
# sudo ./x_pigpio # check C I/F

# sudo pigpiod    # start daemon

# sudo ./x_pigpio.py   # check Python I/F to daemon
# sudo apt install pigpio python3-pigpio
# cd ..
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U sounddevice numpy
deactivate

