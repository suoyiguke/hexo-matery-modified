---
title: centerOS7真机安装.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
---
title: centerOS7真机安装.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
**1、出现这种超时错误** 
![图片发自简书App](http://upload-images.jianshu.io/upload_images/13965490-9be8be89fe8b6cb5.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1080/q/50)

原因是找不到u盘的路径

- 修改u盘名为CENTOS
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f091f8eb6eb793e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 编辑文件  u盘盘符:\isolinux\isolinux.cfg，将名字替换为CENTOS
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e0a73d3a19f15ce7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 append initrd=initrd.img inst.stage2=hd:LABEL=CENTOS
~~~
default vesamenu.c32
timeout 600

display boot.msg

# Clear the screen when exiting the menu, instead of leaving the menu displayed.
# For vesamenu, this means the graphical background is still displayed without
# the menu itself for as long as the screen remains in graphics mode.
menu clear
menu background splash.png
menu title CentOS 7
menu vshift 8
menu rows 18
menu margin 8
#menu hidden
menu helpmsgrow 15
menu tabmsgrow 13

# Border Area
menu color border * #00000000 #00000000 none

# Selected item
menu color sel 0 #ffffffff #00000000 none

# Title bar
menu color title 0 #ff7ba3d0 #00000000 none

# Press [Tab] message
menu color tabmsg 0 #ff3a6496 #00000000 none

# Unselected menu item
menu color unsel 0 #84b8ffff #00000000 none

# Selected hotkey
menu color hotsel 0 #84b8ffff #00000000 none

# Unselected hotkey
menu color hotkey 0 #ffffffff #00000000 none

# Help text
menu color help 0 #ffffffff #00000000 none

# A scrollbar of some type? Not sure.
menu color scrollbar 0 #ffffffff #ff355594 none

# Timeout msg
menu color timeout 0 #ffffffff #00000000 none
menu color timeout_msg 0 #ffffffff #00000000 none

# Command prompt text
menu color cmdmark 0 #84b8ffff #00000000 none
menu color cmdline 0 #ffffffff #00000000 none

# Do not display the actual menu unless the user presses a key. All that is displayed is a timeout message.

menu tabmsg Press Tab for full configuration options on menu items.

menu separator # insert an empty line
menu separator # insert an empty line

label linux
  menu label CENTOS
  kernel vmlinuz
  append initrd=initrd.img inst.stage2=hd:LABEL=CENTOS     quiet

label check
  menu label Test this ^media & install CentOS 7
  menu default
  kernel vmlinuz
  append initrd=initrd.img inst.stage2=hd:LABEL=CENTOS     rd.live.check quiet

menu separator # insert an empty line

# utilities submenu
menu begin ^Troubleshooting
  menu title Troubleshooting

label vesa
  menu indent count 5
  menu label Install CentOS 7 in ^basic graphics mode
  text help
	Try this option out if you're having trouble installing
	CentOS 7.
  endtext
  kernel vmlinuz
  append initrd=initrd.img inst.stage2=hd:LABEL=CENTOS     xdriver=vesa nomodeset quiet

label rescue
  menu indent count 5
  menu label ^Rescue a CentOS system
  text help
	If the system will not boot, this lets you access files
	and edit config files to try to get it booting again.
  endtext
  kernel vmlinuz
  append initrd=initrd.img inst.stage2=hd:LABEL=CENTOS     rescue quiet

label memtest
  menu label Run a ^memory test
  text help
	If your system is having issues, a problem with your
	system's memory may be the cause. Use this utility to
	see if the memory is working correctly.
  endtext
  kernel memtest

menu separator # insert an empty line

label local
  menu label Boot from ^local drive
  localboot 0xffff

menu separator # insert an empty line
menu separator # insert an empty line

label returntomain
  menu label Return to ^main menu
  menu exit

menu end

~~~
-  然后启动电脑进入U盘安装界面------>按e编辑，同样替换为CENTOS -------->编辑完后按ctrl+x启动
~~~
vmlinuz initrd=initrd.img
inst.stage2=hd:LABEL=CentOS\x207\x20x86_64 rd.live.check quiet
改为：
vmlinuz initrd=initrd.img
inst.stage2=hd:/dev/CENTOS quiet
Ctrl+X保存即可

~~~
**2、配置网卡**
- 进入目录编辑网卡配置文件
 cd /etc/sysconfig/network-scripts
 vi ifcfg-enp2s0

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f8163b7fa0f754e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-5482b2ee9961afbd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
~~~
TYPE="Ethernet"
BOOTPROTO="dhcp"
DEFROUTE="yes"
PEERDNS="yes"
PEERROUTES="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_PEERDNS="yes"
IPV6_PEERROUTES="yes"
IPV6_FAILURE_FATAL="no"
NAME="ens33"
UUID="2c655c9f-0354-483c-a45e-5f603dee60e4"
DEVICE="ens33"
ONBOOT="yes"
~~~
- 使用ip addr 查看ip，如果刚修改完配置。使用ping验证后可以上网。但是无法得到ipv4地址。请reboot重启下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a19e4422d3878858.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 
- 然后使用xshell连了
- 可以设置静态ip
cd  /etc/sysconfig/network-scripts
vi ifcfg-ens33
~~~
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
#BOOTPROTO="dhcp"
BOOTPROTO="static"
IPADDR="192.168.10.11"   # 设置的静态IP地址
NETMASK="255.255.255.0"    # 子网掩码
GATEWAY="192.168.10.1"   # 网关地址
#DNS1="192.168.241.2"       # DNS服务器
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="ens33"
UUID="2c655c9f-0354-483c-a45e-5f603dee60e4"
DEVICE="ens33"
ONBOOT="yes"
~~~
重启网络
service network restart

**3、安装后的配置**
- 安装vim
yum install vim
 - 安装wge 
 
yum -y install wget

- 使用阿里巴巴提供的DNS域名解析

vi /etc/resolv.conf
~~~
# Generated by NetworkManager
nameserver 8.8.8.8
nameserver 223.5.5.5
nameserver 223.6.6.6
~~~

- 更换yum源为国内


备份原镜像文件，便于后期恢复 
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup

 

下载新的CentOS-Base.repo 到/etc/yum.repos.d/  Centos7地址：
 wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

清除缓存 yum clean all

生成缓存 yum makecache

更新 sudo yum update

- 关闭防火墙和SELinux


systemctl status firewalld.service (查看防火墙状态)
systemctl stop firewalld.service (关闭防火墙)

这只是简单的关闭防火墙，电脑再重启后依然会自动开启的，所以要想永久的关闭防火墙就必须：
systemctl disable  firewalld.service 
然后还有就是center os自带了一个安全软件SELinux我们还需要将它关闭，避免以后操作会出现莫名的错误。

vi /etc/selinux/config
将SELINUX=******改为SELINUX=disabled然后保存就可以。

- 安装 unzip
yum install -y unzip zip

- 安装端口工具
yum -y install net-tools
可通过netstat -lnp|grep 88 查看端口

- 安装lrzsz，配合xshell使用 rz命令上传文件
yum -y install lrzsz

- 同步网络时间
~~~
yum install ntpdate -y
ntpdate -u ntp.api.bz
~~~

**4、安装docker**
centerOs条件：

必须是 64 位操作系统
建议内核在 3.8 以上
查看内核版本

uname -r 

- 安装　　
　　rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
　　yum -y install docker-io

查看版本
　　docker version
启动
　　service docker start

添加开启自启动
sudo systemctl enable docker

- docker启动失败，报错 Error starting daemon: SELinux is not supported with the overlay2 graph driver on this kernel. Either boot into a newer kernel or disable selinux in docker (--...-enabled=false)

vi  /etc/sysconfig/docker
将配置文件的“--selinux-enabled”改成“--selinux-enabled=false”，然后再重启docker。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2c29aab3be5cdf34.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

重启docker
 systemctl restart docker
 systemctl status docker.service

- 这个也是安装docker必须要做的
修改vi /etc/docker/daemon.json这个文件
~~~
{

"registry-mirrors": ["https://registry.docker-cn.com"]

}


~~~
**5、docker-compose安装**
https://github.com/docker/compose/releases

**6、docker和docker-compose 安装的批处理**
https://www.cnblogs.com/devops-ITboge/p/11012846.html
