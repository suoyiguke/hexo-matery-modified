---
title: linux-安装依赖遇到的问题.md
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
title: linux-安装依赖遇到的问题.md
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
1、报错 ImportError: libSM.so.6: cannot open shared object file: No such file or director

我们可以通过  libSM.so.6这个文件去寻找相关的依赖，使用yum whatprovides libSM.so.6如下
~~~
[root@localhost PaddleOCR]# yum whatprovides libSM.so.6
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirrors.ustc.edu.cn
 * epel: mirrors.ustc.edu.cn
 * extras: mirrors.ustc.edu.cn
 * updates: mirrors.tuna.tsinghua.edu.cn
libSM-1.2.2-2.el7.i686 : X.Org X11 SM runtime library
源    ：base
匹配来源：
提供    ：libSM.so.6


~~~

得到了 libSM-1.2.2-2.el7.i686，安装如下。这样就行了
~~~


[root@localhost PaddleOCR]# yum install libSM-1.2.2-2.el7.i686
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile

~~~
