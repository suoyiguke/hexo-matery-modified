---
title: pip-install-可以直接安装whl文件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: pip-install-可以直接安装whl文件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
1、有些包在线使用pip安装不行。只能离线安装

有一些包安装的时候需要编译器，或者其他库，比如pip install numpy就可以，但是pip install scipy就不行了，缺一个线性代数的库，这个时候用康奈尔大学提供的二进制whl文件，用pip安装就行了。另外，早先bumpy、scipy都提供exe形式的安装包，现在都没有了。
pip install (whl文件路径）


2、在win10下我遇到过
该版本的 D:\python\Scripts\pip.exe 与你运行的 Windows 版本不兼容。请查看计算机的系统信息，然后联系软件发布者。

只能使用vm虚拟机解决。不知道内部是什么原因。网络上也没找到相关的答案


3、遇到安装不了的包。可以从其它机器现有的site-packages目录下直接复制。site-packages目录在python\Lib\site-packages下；指的是python的三方库
where命令可以在环境变量里找相关文件
D:\>where python
D:\python\python.exe
C:\Users\yinkai\AppData\Local\Microsoft\WindowsApps\python.exe
