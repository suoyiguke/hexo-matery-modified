---
title: linux-安装jdk.md
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
title: linux-安装jdk.md
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
1、先卸载自带的openJDK，这个jdk和我们工程使用的jdk不同，有些代码的jar包可能找不到。比如 java.lang.ClassNotFoundException: com.sun.image.codec.jpeg.JPEGCodec

输入：
~~~
rpm -qa | grep jdk 
~~~
 会查询出系统自带的OpenJDK及版本

[root@localhost /]# rpm -qa |grep jdk
java-1.7.0-openjdk-headless-1.7.0.51-2.4.5.5.el7.x86_64
java-1.7.0-openjdk-1.7.0.51-2.4.5.5.el7.x86_64
删除openJDK版本

[root@localhost /]# rpm -e --nodeps java-1.7.0-openjdk-headless-1.7.0.51-2.4.5.5.el7.x86_64
[root@localhost /]# rpm -e --nodeps java-1.7.0-openjdk-1.7.0.51-2.4.5.5.el7.x86_64
再次查询 OpenJDK及版本 此时 OpenJDK已经被删除

[root@localhost /]# rpm -qa |grep jdk
[root@localhost /]# java


2、安装自己的jdk
oracle的要注册登录账号，直接到github里下吧 https://github.com/frekele/oracle-java

选择版本
~~~
Linux ARM 64 Compressed Archive	70.79 MB	jdk-8u291-linux-aarch64.tar.gz
Linux x64 Compressed Archive	138.22 MB	jdk-8u291-linux-x64.tar.gz 选择这个
~~~

vi /etc/profile
底部添加
~~~
export JAVA_HOME=/ca/jdk1.8.0_144
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
~~~
执行 source /etc/profile 刷新环境变量

授权 chmod 777 -R jdk1.8.0_144


yum install  php-mysqlnd

yum install -y  php56w-php-mysqlnd
yum install php55w-mysqlnd.x86_64
