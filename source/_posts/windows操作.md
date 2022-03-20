---
title: windows操作.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
---
title: windows操作.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
###进程和端口操作
1、查看端口是否占用。回车，记下最后一位数字，即PID,这里是2720。
~~~
netstat -aon|findstr "8080"
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4473d8d860e264ba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、查看指定pid对应的程序名，得到执行文件名
~~~
tasklist|findstr "71464"
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9c48113ff2e3e5fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、杀死pid对应的进程
~~~
taskkill /f -pid 10256
~~~

4、杀死指定的执行文件
像nginx这样有多个进程，只杀死一个pid是不够的，杀死之后自己又会创建一个。所以必须这样子直接杀死指定执行文件
~~~
taskkill /f /t /im nginx.exe
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-103eb3ccf00eab98.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5、查看某个执行文件的进程。如查看nginx进程
~~~
tasklist /fi  "imagename eq nginx.exe"
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-02f0817259c66157.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###服务操作

1、Windows服务删除
~~~
C:\tools\instsrv.exe youService remove
~~~
其中Path\instsrv.exe 需要提前下载放在对应的目录

youService 为服务名称

2、Windows服务注册

以管理身份打开控制台程序输入命令：
~~~
cd C:\Windows\Microsoft.NET\Framework\v4.0.30319
InstallUtil.exe  "Path/WinServiceName.exe" 建议用"因为路径中有空格无法识别
~~~
其中Path表示ServiceName.exe所在的位置，回车即可

3、启动服务
~~~
net start ServiceName
~~~
 

4、查看服务，修改服务名
打开注册表
~~~
计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-800680c6c539802a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###检测连接
######telnet 
~~~
C:\Users\yinkai>telnet 192.168.1.103 1521
正在连接192.168.1.103...无法打开到主机的连接。 在端口 1521: 连接失败
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1244f02094d4b33d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######ping
~~~
~~~

######curl
~~~
~~~

C:\tools\instsrv.exe youService remove

"C:\IAS\mysql-3305\MySQL Server 5.7\bin\mysqld.exe" --defaults-file="C:\ca\IAS\mysql-3305\MySQL Server 5.7\my.ini" 3305
