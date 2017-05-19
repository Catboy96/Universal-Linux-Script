#!/bin/bash

# Change to ULS directory
cd /usr/share/uls

# Get the latest version
wget --no-check-certificate -O /usr/share/uls/uls https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls.py
str=$?
if [[ $str != "0" ]]; then
  clear
  echo "Failed downloading the latest version. Update aborted."
  exit
fi

# Remove old version and replace with the latest version
rm -f uls.py
mv uls uls.py
chmod +x uls.py

# Remove link & create a new link
rm -f /usr/bin/uls
ln uls.py /usr/bin/uls

# Refresh system info
uls --getinfo

# Show message
clear
echo "ULS update completed."
