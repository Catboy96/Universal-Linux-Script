# Universal Linux Script
A shell script with built-in variables which can simply script writting.  
For example, ```pkg.install nginx``` equals ```apt-get -y install nginx``` on Debian & ```yum -y install nginx``` on CentOS.  
  
## ULS language  
ULS's language is **same as Linux shell script's language**.  
In another word, ULS is a shell script with built-in variables which can be replaced to specific commands or strings when executed on your device.  
Here's a full example:  
**test.uls**:  
```
pkg.update  
pkg.install nginx  
echo net.ip  
if [ dev.virt == "kvm" ]; then  
    echo "KVM"  
elif [ dev.virt == "openvz" ]; then  
    echo "OpenVZ"  
fi  
```  
When **test.uls** runs on a Debian device with "123.123.123.123" as public IPv4 address & KVM as virtualization technology, it will be converted to:
```
apt-get update  
apt-get -y install nginx  
echo "123.123.123.123"  
if [ "kvm" == "kvm" ]; then  
    echo "KVM"  
elif [ "kvm" == "openvz" ]; then  
    echo "OpenVZ"  
fi  
```   
  
## Starting Guide: How to setup & run ULS script  
[Go to wiki](https://github.com/CYRO4S/Universal-Linux-Script/wiki/Starting-Guide:-How-to-setup-&-run-ULS-script)  
  
## All built-in variables  
[Go to wiki](https://github.com/CYRO4S/Universal-Linux-Script/wiki/All-built-in-variables)  
