#!/usr/bin/env bash

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver (automatically handled by webdriver-manager)
