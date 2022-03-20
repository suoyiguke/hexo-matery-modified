---
title: show-engine-innodb-status;.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: show-engine-innodb-status;.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
###show engine innodb status；监控开启方式
https://www.cnblogs.com/wangdong/p/9235249.html


show engine innodb status显示信息不全如何解决

执行 show engine innodb status\G 时，显示的信息不全，DEADLOCK相关信息太多，后面的都没了 
原因： 
这是mysql客户端的一个bug：BUG#19825，交互式客户端限制了输出信息最大为 64KB，因此更多的信息无法显示。 

解决办法： 
解决方法有两种： 
1. 启用 innodb_status_file 
修改 my.cnf，增加类似下面一行 
innodb_status_file = 1 
就可以了。 

2. 启用 innodb_monitor 
mysqld在线运行时，创建 innodb_monitor 表，即可记录相关信息到日志文件 
mysql> create table innodb_monitor ( id int ) engine = innodb; 
相关的信息就会输出到 .err 日志文件里了。

###innotop 分析工具
