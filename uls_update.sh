#!/bin/bash

# Remove link in /usr/bin/
rm -f /usr/bin/uls

# Remove current ULS
cd /usr/share/uls
rm -f uls.py

# Get the latest version
wget https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls.py && chmod +x uls.py

# Make a link
ln uls.py /usr/bin/uls

# Refresh system info
uls --getinfo

# Show message
clear
echo "ULS update completed."
