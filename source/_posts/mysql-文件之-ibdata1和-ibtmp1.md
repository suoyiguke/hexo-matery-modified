---
title: mysql-文件之-ibdata1和-ibtmp1.md
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
title: mysql-文件之-ibdata1和-ibtmp1.md
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

###ibdata1
ibdata1是InnoDB的共享表空间文件，默认情况下会把表空间存放在一个文件ibdata1中，会造成这个文件越来越大。

发现问题所在之后，解决方法就是，使用独享表空间，将表空间分别单独存放。MySQL开启独享表空间的参数是Innodb_file_per_table，会为每个Innodb表创建一个.ibd的文件。

###ibtmp1

ibtmp1是非压缩的innodb临时表的独立表空间,通过innodb_temp_data_file_path参数指定文件的路径，文件名和大小，默认配置为ibtmp1:12M:autoextend，也就是说在支持大文件的系统这个文件大小是可以无限增长的。
