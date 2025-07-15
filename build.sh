#!/usr/bin/env bash

# Install system packages (including wget)
apt-get update && apt-get install -y wget gnupg2 unzip

# Download and install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
