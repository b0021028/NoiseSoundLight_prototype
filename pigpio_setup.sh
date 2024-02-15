#!/bin/bash


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
sudo ./x_pigpio # check C I/F

sudo pigpiod    # start daemon

./x_pigpiod_if2 # check C      I/F to daemon
./x_pigpio.py   # check Python I/F to daemon
./x_pigs        # check pigs   I/F to daemon
./x_pipe        # check pipe   I/F to daemon

sudo killall pigpiod
sudo pigpiod
