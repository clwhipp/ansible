#!/bin/bash

sudo apt-get update
sudo apt-get -y install python3-pip python3-venv

python3 -m pip install --user pipx
python3 -m pipx ensurepath

python3 -m pipx install --include-deps ansible
python3 -m pipx ensurepath
