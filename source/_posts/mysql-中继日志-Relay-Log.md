---
title: mysql-中继日志-Relay-Log.md
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
title: mysql-中继日志-Relay-Log.md
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


其实中继日志文件Relay Log的文件格式、内容和二进制日志文件 Binlog一样，唯一的区别在于从库上的SQL线程在执行完当前中继日志文件Relay Log 中的事件之后，SQL线程会自动删除当前中继日志文件 Relay Log，避免从库上的中继日志文件Relay Log占用过多的磁盘空间。
