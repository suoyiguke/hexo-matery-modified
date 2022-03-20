---
title: python-基础环境配置.md
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
title: python-基础环境配置.md
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
###安装Python 


https://www.python.org/downloads/windows/

>Gzipped source tarball	Source release	
XZ compressed source tarball	Source release		
macOS 64-bit installer	Mac OS X	for OS X 10.9 and later	
Windows help file	Windows		
Windows x86-64 embeddable zip file	Windows	for AMD64/EM64T/x64	
`选择这个 Windows x86-64 executable installer	Windows	for AMD64/EM64T/x64	`
Windows x86-64 web-based installer	Windows	for AMD64/EM64T/x64	
Windows x86 embeddable zip file	Windows		
Windows x86 executable installer	Windows		
Windows x86 web-based installer	Windows		


X86---32位。
X86-64---64位。
web-based--需要联网安装。
executable--可执行文件（.exe），本地安装。 一般选择这个了
embeddable zip--嵌入式版本，可以集成到其它应用中。

选则下载Windows x86-64 executable installer，执行exe安装即可。

然后配置环境变量，默认是安装到c盘的。这一点不能修改。
将以下路径添加到path变量下。这样python.exe和pip.exe 都可以直接执行而不需要再cd到具体目录下
~~~
C:\Users\yinkai\AppData\Local\Programs\Python\Python38
C:\Users\yinkai\AppData\Local\Programs\Python\Python38\Scripts
~~~

这个pip是py的包管理器类似于java的maven，js的npm/yarn

###pycharm中配置环境
1、先是配置python 的执行exe路径和依赖包路径
file->settings->
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2dc252461d7944a8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、配置执行



若有依赖没有下载，可以这样。鼠标放到上面 alt+回车。选择install即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8323527747298bd7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

本机python依赖可以到这里查看
![image.png](https://upload-images.jianshu.io/upload_images/13965490-efa71770c0bb1ced.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
