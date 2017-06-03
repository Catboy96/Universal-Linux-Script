#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------
# About exit codes:
# 0: ULS exited normally
# 1001: "/usr/share/uls/device.json" not found.
# 1002: ULS script path is invalid.
# 1003: Internet is unavailable for updating.
# 1004: "uls --getinfo" must be run as ROOT.
# 1005: "uls --update" must be run as ROOT.
# 1006: Invalid ULS keyword.
# Other: ULS will return what the converted shell script returns.
# ----------------------

import platform
import tempfile
import json
import uuid
import sys
import os

# Show help.
def ShowHelp():
    print("Universal Linux Script v7 by CYRO4S")
    print("Visit https://github.com/CYRO4S/Universal-Linux-Script for documents and more information.")
    print("")
    print("Usage:")
    print("uls --help: Show this help information.")
    print("uls --getinfo: Refresh system information.")
    print("uls --update: Update ULS to latest version.")
    print("uls --echo [ULS Keyword]: Print the value of specified ULS keyword.")
    print("uls [ULS Script Path]: Run ULS script.")
    exit(0)

# Getting system information & save to file.
def GetInfo():

    # Check for ROOT
    # If "uls --getinfo" is not run as ROOT, notify user & exit.
    print('Checking for ROOT...')
    if os.geteuid() != 0:
        print("ERR_1004: 'uls --getinfo' must be run as ROOT. Use 'sudo uls --getinfo' instead.")
        exit(1004)

    # Determine which Linux distro is running on the device.
    print('Determining Linux distribution...')
    strDist = platform.linux_distribution()[0].lower()
    pUpd, pIns, pUpg, pRem, strBase = '', '', '', '', ''
    if strDist == 'debian' or strDist == 'ubuntu' or strDist == 'kali' or strDist == 'raspbian':
        pUpd = 'apt-get -y upgrade'
        pIns = 'apt-get -y install'
        pUpg = 'apt-get -y upgrade'
        pRem = 'apt-get -y remove'
        strBase = 'debian'
    elif strDist == 'redhat' or strDist == 'redhat linux' or strDist == 'centos linux' or strDist == 'centos':
        pUpd = 'yum -y upgrade'
        pIns = 'yum -y install'
        pUpg = 'yum -y upgrade'
        pRem = 'yum -y remove'
        strBase = 'redhat'

    # Get short version of distro
    strVer = ''
    if strDist == 'centos linux' or strDist == 'centos':
        rVer = os.popen('grep -oE  "[0-9.]+" /etc/redhat-release')
        strVer = rVer.read().strip('\n')[0:1]
        rVer.close()
    elif strDist == 'debian':
        rVer = os.popen('grep -oE  "[0-9.]+" /etc/issue')
        strVer = rVer.read().strip('\n')[0:1]
        rVer.close()
    elif strDist == 'ubuntu':
        rVer = os.popen('lsb_release -r --short')
        strVer = rVer.read().strip('\n')[0:2]
        rVer.close()


    # Get virtualization technology
    print('Determining virtualization technology...')
    rVirt = os.popen('virt-what')
    strVirt = rVirt.read().strip('\n')
    rVirt.close()

    
    # Get system information
    print('Getting system version...')
    strVersion = platform.linux_distribution()[1]
    print('Getting device architecture...')
    strArch = platform.uname()[4]
    print('Getting kernel version...')
    strKernel = platform.uname()[2]
    print('Getting hostname')
    strHostname = platform.node()
    print('Getting OS bit...')
    strBit = platform.architecture()[0]

    
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
    print('Getting your local IPv4 address...')
    rLIP = os.popen("ifconfig -a | grep 'inet ' | cut -d ':' -f 2 |cut -d ' ' -f 1 | grep -v '^127'")
    strLocalIP = rLIP.read().strip('\n')
    rLIP.close()

    print('Getting your MAC address...')
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    strMac = ":".join([mac[e:e+2] for e in range(0,11,2)])

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
        'sys.baseos': strBase,
        'sys.version': strVersion,
        'sys.ver': strVer,
        'sys.arch': strArch,
        'sys.bit': strBit,
        'sys.kernel': strKernel,
        'sys.hostname': strHostname,
        'dev.virt': strVirt,
        'dev.cpu': strCPU,
        'dev.cores': strCores,
        'dev.freq': strFreq,
        'dev.ram': strRAM,
        'dev.swap': strSwap,
        'net.ip': strIP,
        'net.ipv6': strIP6,
        'net.localip': strLocalIP,
        'net.mac': strMac
    }

    strConfigPath = '/usr/share/uls/device.json'
    strConfigDir = os.path.dirname(strConfigPath)

    if not os.path.exists(strConfigDir):
        print("making directory: {DIR}".format(DIR=strConfigDir))
        os.makedirs(strConfigDir)
    with open(strConfigPath, 'w') as f:
        json.dump(strJson, f, sort_keys=False, indent=4)

    # Finalize
    print('--------------')
    print("All done. Now you can run ULS scripts by using 'uls [ULS Script Path]' command,")
    print("or you can refresh system information by using 'uls --getinfo' command,")
    print("or you can update ULS to the latest version by using 'uls --update command.'")


# Run the script.
def RunScript(strPath, strParam):

    # Check for ROOT
    strSudo = 'sudo '
    strRoot = 'false'
    if os.geteuid() == 0:
        strSudo = ''
        strRoot = 'true'

    # Check if device.json exists
    if not os.path.isfile('/usr/share/uls/device.json'):
        print("ERR_1001: 'device.json' not found. Run 'uls --getinfo' to generate.")
        exit(1001)

    # Prepare device.json
    j = json.loads(open('/usr/share/uls/device.json', 'r').read())

    # Check if ULS script exists
    if not os.path.isfile(strPath):
        print("ERR_1002: ULS script path invalid. Ensure you entered the correct path.")
        exit(1002)

    # Read ULS script file
    lines = open(strPath, 'r').readlines()
    # Create a temporary file
    f = tempfile.NamedTemporaryFile(mode='w+t')

    KeywordsList = [
            # pkg.* (package manage commands)
            # usually need root privileges
            ("pkg.install",  True), ("pkg.remove", True),
            ("pkg.update", True), ("pkg.upgrade", True),

            ("dev.cores", False), ("dev.cpu", False),
            ("dev.freq", False), ("dev.ram", False),
            ("dev.swap", False), ("dev.virt", False),

            ("net.ip", False), ("net.ipv6", False),
            ("net.localip", False), ("net.mac", False),

            ("sys.arch", False), ("sys.baseos", False),
            ("sys.bit", False), ("sys.hostname", False),
            ("sys.kernel", False), ("sys.os", False),
            ("sys.ver", False), ("sys.version", False)]
    # Start to replace
    for newLine in lines:
        for keyword, needRoot in KeywordsList:
            if keyword in newLine:
                jsonData = j.get(keyword).strip()
                if len(jsonData) < 1:
                    jsonData = "[warning] *{KWORD}* is None".format(KWORD=keyword)
                newLine = newLine.replace(keyword, jsonData)
                if needRoot:
                    newLine = strSudo + newLine
                # just allow one replacement perline
                break
        f.write(newLine)

    f.seek(0)

    # Then execute it
    strReturn = ''
    strReturn = os.system('bash ' + f.name + strParam)

    # Then close the temporary file
    f.close()

    # Finally, exit.
    exit(strReturn)

# Update ULS.
def Update():

    # Check for ROOT
    # If "uls --update" is not run as ROOT, notify user & exit.
    print('Checking for ROOT...')
    if os.geteuid() != 0:
        print("ERR_1005: 'uls --update' must be run as ROOT. Use 'sudo uls --update' instead.")
        exit(1005)

    # Check for Internet connection before update
    print('Checking for Internet connection...')
    rPing = os.popen("ping -c 3 raw.githubusercontent.com | grep '0 received' | wc -l")
    strPing = rPing.read().strip('\n')
    rPing.close()

    # If Internet is unavailable, exit.
    if strPing == '1':
        print('ERR_1003: Internet is unavailable. Check your connection before running update.')
        exit(1003)

    # Now, do the update 
    os.system("wget --no-check-certificate -O /usr/share/uls/uls_update.sh https://raw.githubusercontent.com/CYRO4S/Universal-Linux-Script/master/uls_update.sh && bash /usr/share/uls/uls_update.sh")
    exit(0)

# Echo
def Echo(strKey):
    # Check for ROOT
    strRoot = 'false'
    if os.geteuid() == 0:
        strRoot = 'true'

    # Check if device.json exists
    if not os.path.isfile('/usr/share/uls/device.json'):
        print("ERR_1001: 'device.json' not found. Run 'uls --getinfo' to generate.")
        exit(1001)

    # Prepare device.json
    j = json.loads(open('/usr/share/uls/device.json', 'r').read())

    # Print ULS Keywords
    if strKey == 'sys.root':
        print(strRoot)
        exit(0)
    strValue = j.get(strKey)
    if (strValue is None):
        print("ERR_1006: Invalid ULS Keyword.")
        exit(1006)
    strValue = strValue.strip()
    print(strValue)
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
        elif sys.argv[1] == "--echo":
            Echo(sys.argv[2])
        else:
            strParam = ""
            if len(sys.argv) > 2:
                for i in range(2, len(sys.argv)):
                    strParam = strParam + " " + sys.argv[i]
                RunScript(sys.argv[1], strParam)
            else:
                RunScript(sys.argv[1], strParam)
    exit(0)
