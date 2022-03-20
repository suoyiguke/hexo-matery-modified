---
title: Linux-共享库LIBRARY_PATH,-LD_LIBRARY_PATH-与ld-so-conf.md
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
title: Linux-共享库LIBRARY_PATH,-LD_LIBRARY_PATH-与ld-so-conf.md
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
 

参考:

1. Linux 共享库：LD_LIBRARY_PATH 与ld.so.conf
Linux环境变量名，该环境变量主要用于指定查找共享库(动态链接库)时除了默认路径之外的其他路径。(该路径在默认路径之前查找)
　　移植程序时的经常碰到需要使用一些特定的动态库，而这些编译好的动态库放在我们自己建立的目录里，这时可以将这些目录设置到LD_LIBRARY_PATH中。
　　当执行函数动态链接.so时，如果此文件不在缺省目录下‘/usr/local/lib’ and ‘/usr/lib’.
　　那么就需要指定环境变量LD_LIBRARY_PATH
　　假如现在需要在已有的环境变量上添加新的路径名，则采用如下方式：
　　LD_LIBRARY_PATH=NEWDIRS:$LD_LIBRARY_PATH.（newdirs是新的路径串）

2. LIBRARY_PATH和LD_LIBRARY_PATH环境变量的区别
LIBRARY_PATH和LD_LIBRARY_PATH是Linux下的两个环境变量，二者的含义和作用分别如下：

LIBRARY_PATH环境变量用于在程序编译期间查找动态链接库时指定查找共享库的路径，例如，指定gcc编译需要用到的动态链接库的目录。设置方法如下（其中，LIBDIR1和LIBDIR2为两个库目录）：

export LIBRARY_PATH=LIBDIR1:LIBDIR2:$LIBRARY_PATH


LD_LIBRARY_PATH环境变量用于在程序加载运行期间查找动态链接库时指定除了系统默认路径之外的其他路径，注意，LD_LIBRARY_PATH中指定的路径会在系统默认路径之前进行查找。设置方法如下（其中，LIBDIR1和LIBDIR2为两个库目录）：
~~~
export LD_LIBRARY_PATH=LIBDIR1:LIBDIR2:$LD_LIBRARY_PATH
~~~
