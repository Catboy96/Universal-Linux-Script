#!/bin/bash

echo "Installing required programs..."

apt-get -y install wget python3 virt-what
yum -y install wget python3 virt-what

echo "Downloading ULS..."
wget https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls.py && chmod +x uls.py

echo "Let ULS get your system information..."
./uls.py --getinfo

clear
echo "All Done."
echo "Now use './uls.py [Path-to-ULS-script]' to run a ULS script."
