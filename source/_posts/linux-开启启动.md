---
title: linux-开启启动.md
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
title: linux-开启启动.md
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
###1、/etc/rc.d/rc.local

这个脚本里不能访问到环境变量 java_home ，只能写上java_home的路径了
~~~

[root@localhost ~]# vi /etc/rc.d/rc.local vi /etc/rc.d/rc.local vi /etc/rc.d/rc.local/etc/rc.d/rc.local

5 files to edit

#!/bin/bash

# THIS FILE IS ADDED FOR COMPATIBILITY PURPOSES

#

# It is highly advisable to create own systemd services or udev rules

# to run scripts during boot instead of using this file.

#

# In contrast to previous versions due to parallel execution during boot

# this script will NOT be run after all other services.

#

# Please note that you must run 'chmod +x /etc/rc.d/rc.local' to ensure

# that this script will be executed during boot.



touch /var/lock/subsys/local

/ias/start.sh

~~~



当然有办法解决


###### rc.local与环境变量的问题

今天又遇到了同样的问题，决定把它记下来。

当服务器上安装了tomcat服务，通常我们希望系统启动的时候能够自动将tomcat启动起来，很自然我们就会想到rc.local，于是就这样做：

echo “/usr/local/bin/tomcat/bin/startup.sh” >> /etc/rc.d/rc.local

可是事实总是屡试都爽，证明这样是行不通的，每次重启服务器都不能自动重启tomcat服务

于是我们便在/usr/local/bin/tomcat/bin/startup.sh 后面加上 >>/tmp/startup.log

跟踪日志发现找不到环境变量JAVA_HOME，这是为什么呢？

rc.local is a file, owned by root.root and should be mode 755\. The rc.local file is for initialization of programs after the system has fully booted. This script is run right before login prompts are displayed. You can use the file to run last minute startups, set certain environment variables, etc.

Conversely, if you want to start something before everything else, you would use the regular file in /etc/rc.d called rc.sysinit, which should have the same owner and permissions. 

这说明rc.local运行在操作系统完全引导成功但是尚未启动login shell之前，所以我们配置在/etc/profiles或bashrc里的环境变量并未得到执行，因此在rc.local执行阶段看不到任何环境变量。

该问题的解决办法有两种：

1\. 在rc.local中在startup命令之前加上export JAVA_HOME=***********

2\. 可以在crontab中配置一个tomcat服务的监控脚本，1分钟探测一次tomcat是否正在运行，如果没有运行就启动一下tomcat


