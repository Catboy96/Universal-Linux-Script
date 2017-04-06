#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#=================================================================#
#   System Required:  CentOS 6+, Debian 7+, Ubuntu 14+            #
#   Description: Install ULS                                      #
#   Author: @CYRO4S                                               #
#   Intro:  https://github.com/CYRO4S/Universal-Linux-Script      #
#=================================================================#

# Get distro version
function GetVersion(){
    if [[ -s /etc/redhat-release ]];then
        grep -oE  "[0-9.]+" /etc/redhat-release
    else
        grep -oE  "[0-9.]+" /etc/issue
    fi
}

# Get CentOS version
function GetCentosVersion(){
    local code=$1
    local version="`GetVersion`"
    local main_ver=${version%%.*}
    if [ $main_ver == $code ];then
        return 0
    else
        return 1
    fi
}

# Install on Debian 7+, Ubuntu 14+
function InstallDeb() {
    echo "Updating source..."
    apt-get update

    echo "Installing required packages..."
    apt-get install python3 virt-what

    echo "Downloading ULS..."
    mkdir /usr/share/uls/
    wget -O /usr/share/uls/uls.py https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls.py && chmod +x /usr/share/uls/uls.py

    echo "Let's make ULS a true command..."
    ln /usr/share/uls/uls.py /usr/bin/uls

    clear

    echo "Let ULS get your system information..."
    uls --getinfo

    echo "All done."
    echo "Now use 'uls [Path-to-ULS-script]' to run a ULS script."
}

# Install on CentOS 7+
function InstallCent() {
    echo "Installing required packages..."
    yum -y install epel-release
    yum -y install python34 virt-what

    echo "Downloading ULS..."
    mkdir /usr/share/uls/
    wget -O /usr/share/uls/uls.py https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls.py && chmod +x /usr/share/uls/uls.py

    echo "Let's make ULS a true command..."
    ln /usr/share/uls/uls.py /usr/bin/uls

    clear

    echo "Let ULS get your system information..."
    uls --getinfo

    echo "All done."
    echo "Now use 'uls [Path-to-ULS-script]' to run a ULS script."
}

# Get distro
function GetDist(){
    if [ -f /etc/redhat-release ];then
        if GetCentosVersion 5; then
            echo "CentOS 5 is not supported. Auto-Install aborted."
            exit 1
        else
            InstallCent
        fi

    elif [ ! -z "`cat /etc/issue | grep bian`" ];then
        if GetVersion 6; then
            echo "Debian 6 is not supported. Auto-Install aborted."
            exit 1
        else
            InstallDeb
        fi
    elif [ ! -z "`cat /etc/issue | grep Ubuntu`" ];then
        InstallDeb
    else
        echo "Distribution not supported. Auto-Install aborted."
        echo "Try installing manually"
        exit 1
    fi
}

# Initialization step
clear
GetDist
