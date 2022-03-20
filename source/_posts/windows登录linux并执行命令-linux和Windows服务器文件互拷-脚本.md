---
title: windows登录linux并执行命令-linux和Windows服务器文件互拷-脚本.md
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
title: windows登录linux并执行命令-linux和Windows服务器文件互拷-脚本.md
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
使用 plink和pscp命令实现

###上传文件
1. 使用Putty提供的plink.exe来自动登陆一个机器并执行命令，完成后自己关闭

bat文件内容如下： 

```
D:\Download\Software\Putty-0.60\plink.exe -pw jointforce2004 root@192.168.0.1 "/root/testconn.sh; getkey" 
```

这个命令就是登陆到192.168.0.1上，执行命令：/root/testconn.sh; getkey ，然后自动退出。 

linux下getkey这个命令会等待用户输入，然后回显用户输入的字符，然后命令退出。这里用这个命令来停住窗口，看完随便敲下键盘plink就退出了，因为所有命令已经执行完毕了。

###执行命令
2. 使用Putty提供的pscp.exe命令实现Linux文件上传与下载：

| 

命令格式：pscp localfile rootuser@remoteip:/fileDirectory
拷贝整个文件夹： pscp -r localDir rootuser@remoteip:/fileDirectory

注：如果是从linux拷贝文件，是同样的方法，只不过是把前后地址对换一下即可; 

 |

例1：比如我想把windows下e:\htk 整个目录的所有文件复制到linux /root目录下，命令如下：

```
pscp -r -l root -pw 1234567890 e:\htk 192.168.0.204:/root
```

| 说明：
-r 复制目录下所有文件;
-l 对方机器(linux)的用户名(root);
-pw 密码(1234567890 );
e:\htk 源文件/文件夹的地址
192.168.0.204:/root 目的文件/文件夹的地址。
       192.168.0.204为linux机器的ip地址。  |

例2：反过来，把linux soundRcg目录下的test.txt文件传输到windows e:\下，同样在windows命令行中敲入命令：

```
pscp -l root -pw 1234567890 192.168.0.204:/soundRcg/test.txt E:\
```

3\. Putty下载地址：[http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)


###部署web文件实例
~~~
@echo off

set fileSrc=./zip/
set fileName=dist.zip
set serverHost=root@192.168.1.54
set password=XUNxiao000@***
set filePath=/home/mgb_treasure_system/
rem 上传文件
echo 上传文件到 %serverHost% %filePath%
pscp -pw %password% %fileSrc%%fileName% %serverHost%:%filePath%

rem 等待5秒文件上传完毕
rem TIMEOUT /T 5 /NOBREAK
rem 执行命令
plink -pw %password% %serverHost% "cd %filePath% && chmod 777 %fileName% && sh rest.sh" 
echo 部署完毕...

@cmd.exe
exist
~~~
