---
title: linux和windows系统对大小写的处理.md
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
title: linux和windows系统对大小写的处理.md
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
windows 不区分大小写，同目录下A和a不可以同时存在

~~~

G:\mysql>dir
 驱动器 G 中的卷是 H
 卷的序列号是 4F71-E70A

 G:\mysql 的目录

2021/05/05  17:15    <DIR>          .
2021/05/05  17:15    <DIR>          ..
2021/05/05  17:15    <DIR>          A


G:\mysql>mkdir a
子目录或文件 a 已经存在。

~~~

linux 区分大小写，同目录下A和a可以同时存在
~~~
[root@localhost mysql-5.6.51-linux-glibc2.12-x86_64]# ll
总用量 228
drwxr-xr-x.  2 root  root       6 5月   5 17:15 a
drwxr-xr-x.  2 root  root       6 5月   5 17:15 A
~~~
