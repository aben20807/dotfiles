#!/bin/bash

sudo apt-get install git -y && \
    git clone https://github.com/aben20807/dotfiles.git && \
    cd ./dotfiles/ && \
    sudo -E python3 driver.py
