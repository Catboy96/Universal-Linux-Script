# 通用Linux脚本 (Universal Linux Script, ULS)
*ULS 发音为 "U-Less"*  
一个内建系统信息变量的Shell脚本，可以帮助你简化Shell脚本的开发。    
比如, ```pkg.install nginx``` 相当于 Debian 上的```apt-get -y install nginx``` 和 CentOS 上的 ```yum -y install nginx```。 
  
## ULS 语言  
ULS的语言**与Shell脚本语言相同**。  
换句话说， ULS是一个内建了系统信息变量的Shell脚本，在执行时这些变量会根据你的系统信息被替换为相应的命令或字符串。  
完整示例：  
  
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
  
当 **test.uls** 公网IPv4地址为 "**123.123.123.123**"、虚拟化技术为 **KVM**、系统为 **Debian** 的设备上执行时，它将被转化为：  
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
  
## 走近ULS: 全新的Shell编程体验 
[前往Wiki](https://github.com/CYRO4S/Universal-Linux-Script/wiki/%E8%B5%B0%E8%BF%91ULS:-%E5%85%A8%E6%96%B0%E7%9A%84Shell%E7%BC%96%E7%A8%8B%E4%BD%93%E9%AA%8C%E3%80%82)  
  
## 安装与使用ULS  
[前往Wiki](https://github.com/CYRO4S/Universal-Linux-Script/wiki/%E5%AE%89%E8%A3%85%E4%B8%8E%E4%BD%BF%E7%94%A8ULS)  
  
## 所有内建的语句和变量 
[前往Wiki](https://github.com/CYRO4S/Universal-Linux-Script/wiki/All-built-in-variables)  
  
## 更新历史
[前往Wiki](https://github.com/CYRO4S/Universal-Linux-Script/wiki/Update-history)
