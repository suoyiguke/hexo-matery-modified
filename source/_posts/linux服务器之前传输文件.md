---
title: linux服务器之前传输文件.md
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
title: linux服务器之前传输文件.md
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

1、将本地Linux系统文件发送到另一台
~~~
scp /etc/my.cnf root@10.0.153.39:/etc/my.cnf
~~~
2、从指定linux系统上拉去文件
~~~
scp -r root@10.0.153.38:/ca/java/mysql-5.7.31-linux-glibc2.12-x86_64 /ca/java/mysql-5.7.31-linux-glibc2.12-x86_64
~~~

> 若是一个文件夹则加上 -r
