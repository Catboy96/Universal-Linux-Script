# Universal Linux Script
A shell script with built-in variables which can simply script writting.  
For example, ```pkg.install nginx``` equals ```apt-get -y install nginx``` on Debian & ```yum -y install nginx``` on CentOS.  
  
# ULS language  
ULS's language is same as Linux shell script's language.  
In another word, ULS is shell scripts with built-in variables which can be replaced to specific commands or strings when executing on your device.  
Here's a full example:  
**test.uls**:```   
pkg.update  
pkg.install nginx  
echo net.ip  
if [ dev.virt == "kvm" ]; then  
    echo "KVM"  
elif [ dev.virt == "openvz" ]; then  
    echo "OpenVZ"  
fi  
```  
When
