#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import platform
import json
import sys
import os

# Show help.
def ShowHelp():
    print("Universal Linux Script v5 by CYRO4S")
    print("Visit https://github.com/CYRO4S/Universal-Linux-Script for documents and more information.")
    print("")
    print("Usage:")
    print("uls --help: Show this help information.")
    print("uls --getinfo: Refresh system information.")
    print("uls --update: Update ULS to latest version.")
    print("uls [ULS Script Path]: Run ULS script.")
    exit()

# Getting system information & save to file.
def GetInfo():

    # Determine which Linux distro is running on the device.
    print('Determining Linux distrubution...')
    strDist = platform.linux_distribution()[0].lower()
    pUpd, pIns, pUpg, pRem, strBase = '', '', '', '', ''
    if strDist == 'debian' or strDist == 'ubuntu' or strDist == 'elementary' or strDist == 'kali' or strDist == 'raspbian':
        pUpd = 'apt-get -y upgrade'
        pIns = 'apt-get -y install'
        pUpg = 'apt-get -y upgrade'
        pRem = 'apt-get -y remove'
        strBase = 'debian'
    elif strDist == 'redhat' or strDist == 'centos' or strDist == 'fedora' or strDist == 'redhat linux' or strDist == 'centos linux' or strDist == 'fedora linux':
        pUpd = 'yum -y upgrade'
        pIns = 'yum -y install'
        pUpg = 'yum -y upgrade'
        pRem = 'yum -y remove'
        strBase = 'redhat'

    # Get virtualization technology
    print('Determining virtualization technology...')
    rVirt = os.popen('virt-what')
    strVirt = rVirt.read().strip('\n')
    rVirt.close()
    
    # Get system information
    print('Getting system version...')
    strVersion = platform.linux_distribution()[1]
    print('Getting device architecture...')
    strArch = platform.uname().machine
    print('Getting kernel version...')
    strKernel = platform.uname().release
    print('Getting hostname')
    strHostname = platform.node()
    print('Getting OS bit...')
    strBit = platform.architecture()[0]

    print('Checking for ROOT...')
    strRoot = ''
    if os.geteuid() == 0:
        strRoot = 'true'
    else:
        strRoot = 'false'
    
    # Get hardware info
    print('Getting CPU information...')
    rCPU = os.popen("echo $( awk -F: '/model name/ {name=$2} END {print name}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//' )")
    strCPU = rCPU.read().strip('\n')
    rCPU.close()

    rCores = os.popen("echo $( awk -F: '/model name/ {core++} END {print core}' /proc/cpuinfo )")
    strCores = rCores.read().strip('\n')
    rCores.close()

    rFreq = os.popen("echo $( awk -F: '/cpu MHz/ {freq=$2} END {print freq}' /proc/cpuinfo | sed 's/^[ \t]*//;s/[ \t]*$//' )")
    strFreq = rFreq.read().strip('\n')
    rFreq.close()

    print('Getting RAM size...')
    rRAM = os.popen("echo $( free -m | awk '/Mem/ {print $2}' )")
    strRAM = rRAM.read().strip('\n')
    rRAM.close()

    print('Getting Swap size...')
    rSwap = os.popen("echo $( free -m | awk '/Swap/ {print $2}' )")
    strSwap = rSwap.read().strip('\n')
    rSwap.close()


    # Get network info
    print('Getting your public IPv4 address...')
    rIP = os.popen('wget -qO- -t1 -T2 ipv4.icanhazip.com')
    strIP = rIP.read().strip('\n')
    rIP.close()

    print('Getting your public IPv6 address...')
    rIP6 = os.popen('wget -qO- -t1 -T2 ipv6.icanhazip.com')
    strIP6 = rIP6.read().strip('\n')
    rIP6.close()

    # Finally write the JSON file.
    print("Now generating 'device.json'...")
    strJson = {
        'pkg.update': pUpd,
        'pkg.install': pIns,
        'pkg.upgrade': pUpg,
        'pkg.remove': pRem,
        'sys.os': strDist,
        'sys.osbase': strBase,
        'sys.version': strVersion,
        'sys.arch': strArch,
        'sys.bit': strBit,
        'sys.kernel': strKernel,
        'sys.hostname': strHostname,
        'sys.root': strRoot,
        'dev.virt': strVirt,
        'dev.cpu': strCPU,
        'dev.cores': strCores,
        'dev.freq': strFreq,
        'dev.ram': strRAM,
        'dev.swap': strSwap,
        'net.ip': strIP,
        'net.ipv6': strIP6
    }
    
    with open('/usr/share/uls/device.json', 'w') as f:
        json.dump(strJson, f, sort_keys=False, indent=4)

    # Finalize
    print('--------------')
    print("All done. Now you can run ULS scripts by using 'uls [ULS Script Path]' command,")
    print("or you can refresh system information by using 'uls --getinfo' command,")
    print("or you can update ULS to the latest version by using 'uls --update command.'")

# Run the script.
def RunScript(strPath):

    # Check if device.json exists
    if not os.path.isfile('/usr/share/uls/device.json'):
        print("'device.json' not found. Run 'uls --getinfo' to generate.")
        exit(1)

    # Prepare device.json
    j = json.loads(open('/usr/share/uls/device.json', 'r').read())

    # Check if ULS script exists
    if not os.path.isfile(strPath):
        print("ULS script not found. Ensure you entered the correct path.")
        exit(2)

    # Read ULS script file
    lines = open(strPath, 'r').readlines()
    f = open('/usr/share/uls/script.sh', 'w')

    # Start to replace
    for s in lines:
        f.write(
            # Replace PKG.*
            s.replace('pkg.update', j.get('pkg.update')) \
            .replace('pkg.install', j.get('pkg.install')) \
            .replace('pkg.upgrade', j.get('pkg.upgrade')) \
            .replace('pkg.remove', j.get('pkg.remove')) \
            
            # Replace SYS.*
            .replace('sys.os', '\"' + j.get('sys.os') + '\"') \
            .replace('sys.osbase', '\"' + j.get('sys.osbase') + '\"') \
            .replace('sys.version', '\"' + j.get('sys.version') + '\"') \
            .replace('sys.arch', '\"' + j.get('sys.arch') + '\"') \
            .replace('sys.bit', '\"' + j.get('sys.bit') + '\"') \
            .replace('sys.kernel', '\"' + j.get('sys.kernel') + '\"') \
            .replace('sys.hostname', '\"' + j.get('sys.hostname') + '\"') \
            .replace('sys.root', '\"' + j.get('sys.root') + '\"') \

            # Replace DEV.*
            .replace('dev.virt', '\"' + j.get('dev.virt') + '\"') \
            .replace('dev.cpu', '\"' + j.get('dev.cpu') + '\"') \
            .replace('dev.cores', '\"' + j.get('dev.cores') + '\"') \
            .replace('dev.freq', '\"' + j.get('dev.freq') + '\"') \
            .replace('dev.ram', '\"' + j.get('dev.ram') + '\"') \
            .replace('dev.swap', '\"' + j.get('dev.swap') + '\"') \

            # Replace NET.*
            .replace('net.ip', '\"' + j.get('net.ip') + '\"') \
            .replace('net.ipv6', '\"' + j.get('net.ipv6') + '\"')
        )

    # Save script.sh
    f.close()

    # Then execute it
    os.system('bash /usr/share/uls/script.sh')

    # Then remove 'script.sh'
    os.remove('/usr/share/uls/script.sh')

    # Finally, exit.
    exit()

# Update ULS.
def Update():
    os.system("wget -O /usr/share/uls/uls_update.sh https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls_update.sh && bash /usr/share/uls/uls_update.sh")
    exit(0)

# Main
if __name__ == '__main__':
    if len(sys.argv) == 1:
        ShowHelp()
    else:
        if sys.argv[1] == "--getinfo":
            GetInfo()
        elif sys.argv[1] == "--help":
            ShowHelp()
        elif sys.argv[1] == "--update":
            Update()
        else:
            RunScript(sys.argv[1])
    exit(0)
