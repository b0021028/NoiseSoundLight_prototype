#!/bin/bash

apt install python3-setuptools python3-pip python3-venv

# pigpio install
wget https://github.com/joan2937/pigpio/archive/refs/tags/v79.tar.gz
tar -xvf v79.tar.gz
cd pigpio-79

make
make install
# If the Python part of the install fails it may be because you need the setup tools.
#sudo apt install python-setuptools python3-setuptools
# end install

# check liblary
./x_pigpio # check C I/F

pigpiod    # start daemon

./x_pigpiod_if2 # check C      I/F to daemon
./x_pigpio.py   # check Python I/F to daemon
./x_pigs        # check pigs   I/F to daemon
./x_pipe        # check pipe   I/F to daemon

killall pigpiod
pigpiod
cd ~
python3 -m venv .venv
source .venv/bin/activate
pip install sounddevice
