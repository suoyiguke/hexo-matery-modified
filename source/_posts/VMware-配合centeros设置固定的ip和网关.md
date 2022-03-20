---
title: VMware-配合centeros设置固定的ip和网关.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: VMware
categories: VMware
---
---
title: VMware-配合centeros设置固定的ip和网关.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: VMware
categories: VMware
---
平时经常切换网络环境，在公司和宿舍里连不同的wifi。使用VMware 的话就需要手动的修改网络配置，不然连SSH不上，一直改很麻烦又不能复制粘贴。有没有一种方式一劳永逸呢。就算切换也不用改，直接可以连？
网上找了下还真有办法。

1、编辑->虚拟网络编辑器
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8286acf22629fd5b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2、选择设置VMnet8网卡
>使用 NAT模式
设置 子网IP 192.168.6.0
子网掩码  255.255.255.0

![image.png](https://upload-images.jianshu.io/upload_images/13965490-a2e821d2ccdb1a84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>点进去 NAT 设置 。设置网关IP为 192.168.6.2

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c7ceb39356c1c3dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>点进去DHCP设置

![image.png](https://upload-images.jianshu.io/upload_images/13965490-822e0ab77d54d158.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、设置VMware的网卡 VMnet8。这里的网关值要和之前的一样、注意ip是192.168.6.1
 反正按我这个来就好。
>ip 192.168.6.1
子网掩码 255.255.255.0
网关 192.168.6.2

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c93e76a4b3261367.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7b4a8fce7fb36ac0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


4、在虚拟机界面右下角，右键配置虚拟网络
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f93f4af159e31dc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
关联配置VMnet8网卡
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e0d7233f4457b22e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


5、配置linux静态固定ip
选择一个局域网内IP，我这里是C类
>局域网可使用的网段（私网地址段）zhidao有三大段：
10.0.0.0~10.255.255.255（A类）回
172.16.0.0~172.31.255.255（B类）
192.168.0.0~192.168.255.255（C类）

ip我这里指定为`192.168.6.128`，  网关指定为  `192.168.6.2` 和上面保持一致！
ip的范围可以在192.168.6.3 ~ 192.168.6.254 （闭区间）之间，其中192.168.6.1（之前已使用）、192.168.6.2（网关）已经被占用、192.168.6.255被broadcast广播地址占用




centeros 网络固定ip配置实例
~~~
TYPE="Ethernet"
PROXY_METHOD="none"
BOOTPROTO="static"
IPADDR="192.168.6.128"
GATEWAY="192.168.6.2"
DEFROUTE="yes"
UUID="2c655c9f-0354-483c-a45e-5f603dee60e4"
DEVICE="ens33"
ONBOOT="yes"
~~~

6、reboot重启linux


###测试
ping www.baidu.com 外网可连
ping 192.168.6.1
ping  192.168.6.2
ping  本机IP

切换WIFI网络，不需要再修改配置了。nice

