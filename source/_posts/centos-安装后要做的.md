---
title: centos-安装后要做的.md
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
title: centos-安装后要做的.md
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
###网卡配置
vi /etc/sysconfig/network-scripts/ifcfg-ens33 
~~~
IPV6INIT=no
OXY_METHOD="none"
BOOTPROTO="static"
IPADDR="192.168.1.117"
GATEWAY="192.168.1.1"
DEFROUTE="yes"
UUID="2c655c9f-0354-483c-a45e-5f603dee60e4"
DEVICE="ens33"
ONBOOT="yes"
~~~
/etc/init.d/network restart

之后可以用xshell连了


###其它
1、yum install lrzsz  文件传输,后面rz就行

2、yum install wget


3、关闭防火墙
CentOS 7.0默认使用的是firewall作为防火墙

查看防火墙状态
firewall-cmd --state

停止firewall
禁止firewall开机启动
systemctl stop firewalld.service
systemctl disable firewalld.service 


