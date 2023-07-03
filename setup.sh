#!/bin/bash

sudo apt-get install git -y && \
    yes | sudo rm -rf dotfiles/ && \
    git clone https://github.com/aben20807/dotfiles.git && \
    cd ./dotfiles/ && \
    python3 driver.py install
