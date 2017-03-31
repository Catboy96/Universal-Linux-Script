#!/bin/bash 

echo "Installing required programs..."
apt-get -y install wget python3 virt-what dos2unix
yum -y install wget python3 virt-what dos2unix

echo "Downloading ULS..." 
wget https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls.py && chmod +x uls.py 
dos2unix uls.py

echo "Make ULS a true command..."
mkdir /usr/share/uls
mv uls.py /usr/share/uls/uls.py
ln /usr/share/uls/uls.py /usr/bin/uls

echo "Let ULS get your system information..." 
uls --getinfo 

clear 

echo "All Done." 
echo "Now use 'uls [Path-to-ULS-script]' to run a ULS script."
