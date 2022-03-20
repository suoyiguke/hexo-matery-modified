---
title: mysql-运行到-ip-v6服务器中指定ivp4地址.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-运行到-ip-v6服务器中指定ivp4地址.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
###因为默认走ipv6所以只能这样

/bin/sh /mysql/bin/mysqld_safe --datadir=/mysql/data --pid-file=/mysql/data/localhost.localdomain.pid --bind-address=10.0.3.234

###那么应该如何执行远程登录呢？
# [mysql 远程连接不上，bind-address参数配置要求，以及怎么去使得mysql能够允许远程的客户端访问](https://www.cnblogs.com/isme-zjh/p/11540442.html)

刚安装了MySQL服务器，使用远程管理工具总是连接不上，因为知道mysql的默认端口是3306，于是使用telnet连接这个端口，(从这里可以学到telnet是可以这样用的)

telnet 192.168.1.10 3306

还是连接不上，于是怀疑是防火墙问题，便将防火墙关掉，
service iptables stop

再次telnet，还是没办法连上这个端口，然后通过netstat查看3306的端口状态是怎么样的（从这里可以学到netstat是可以这样用的)
netstat -apn | grep 3306

终于发现了一个比较奇怪的东西
tcp 0 0 127.0.0.1:3306 0.0.0.0:* LISTEN 3783/mysqld

上面标红的地方，监听端口正常，但却绑定了本地回旋地址，难怪总是连接不上，于是查了下资料，找到了解决办法：
修改mysql的配置文件/etc/mysql/my.conf，**将bind-address后面增加远程访问IP地址或者禁掉这句话就可以让远程机登陆访问了。**

**bind-address=127.0.0.1  139.196.197.138**
**(允许多个IP可访问mysql服务器，空格隔开)**

记得要重启mysql服务哦
service mysql restart

 *参考链接：[http://www.php512.com/?p=808](http://www.php512.com/?p=808)*
