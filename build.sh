#!/usr/bin/env bash

# Update & install dependencies as root
sudo apt-get update
sudo apt-get install -y wget gnupg2 unzip

# Download Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome as root
sudo apt install -y ./google-chrome-stable_current_amd64.deb
