#!/bin/bash

echo "Updating source..."
apt-get update

echo "Installing required packages..."
apt-get -y install wget python3 virt-what
yum -y install wget python34 virt-what

echo "Downloading ULS..."
wget https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls.py && chmod +x uls.py

echo "Let's make ULS a true command..."
mkdir /usr/share/uls
mv uls.py /usr/share/uls/uls.py
ln /usr/share/uls/uls.py /usr/bin/uls

clear

echo "Let ULS get your system information..."
uls --getinfo

echo "All done."
echo "Now use 'uls [Path-to-ULS-script]' to run a ULS script."
