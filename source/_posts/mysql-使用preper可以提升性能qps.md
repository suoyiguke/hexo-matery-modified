---
title: mysql-使用preper可以提升性能qps.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-使用preper可以提升性能qps.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
姜承尧老师在视频号中分享了关于mysql 使用preper不但能防止sql注入还能提供QPS 20%  左右。

能在高并发下提高sql的执行效率(20%)  

mysql8.0.23版本 

1、lscpu 查看cpu核心数
2、使用top命令查看各个进程占用的cup逻辑核
3、WeTERM 远程软件

4、查看mysql qps ： Innodb_rows_read参数就是QPS

5、使用pref top -p `pidof mysqld`查看热点函数
由于没有执行prepear，MYSQLparse函数执行次数变多。需要进行更多的硬解析
