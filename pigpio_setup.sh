#!/bin/bash

sudo apt install -y python3-setuptools python3-pip python3-venv portaudio19-dev

# pigpio install
wget https://github.com/joan2937/pigpio/archive/refs/tags/v79.tar.gz
tar -xvf v79.tar.gz
cd pigpio-79

make
sudo make install
# If the Python part of the install fails it may be because you need the setup tools.
#sudo apt install python-setuptools python3-setuptools
# end install

# check liblary
./x_pigpio # check C I/F

sudo pigpiod    # start daemon

./x_pigpio.py   # check Python I/F to daemon

cd ..
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U -y sounddevice
