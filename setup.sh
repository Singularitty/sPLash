#!/bin/bash

# Needs to run as root to install pip
# For some reason fresh installs of ubuntu do not come with pip and apt needs sudo
if [ "$(id -u)" -ne 0 ]; then
        echo 'This script must be run by root' >&2
        exit 1
fi

# weird stuff with python versions on ubuntu 22 lts let's make sure we use python3.10
apt update;
apt -y install python3.10;
apt -y install python3.10-venv python3-pip;
apt -y install llvm

# Create virtual environment to install dependencies to it
python3.10 -m venv env
source env/bin/activate

# Install requirements
python3.10 -m pip install -r requirements.txt
