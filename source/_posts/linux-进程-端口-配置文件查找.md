---
title: linux-进程-端口-配置文件查找.md
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
title: linux-进程-端口-配置文件查找.md
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
######查找指定端口上运行的nginx的配置文件
若系统中有多个配置文件，该如何定位具体是哪个配置文件在运行？通过如下方法定位当前正在运行的nginx的配置文件：

1、查看nginx的PID，以常用的80端口为例：
~~~
netstat -anop | grep 0.0.0.0:80
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-92242453fbcc3b22.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、 通过相应的进程ID(比如：28506）查询当前运行的nginx路径：
~~~
ll  /proc/28506/exe
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-91ffe8262dad3dff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、 获取到nginx的执行路径后，使用-t参数即可获取该进程对应的配置文件路径，如：
~~~
/usr/local/nginx/sbin/nginx -t
~~~
>nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful


######根据程序名称查找进程
~~~
 ps -ef|grep nginx
~~~
