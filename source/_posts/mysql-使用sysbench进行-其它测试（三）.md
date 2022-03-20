---
title: mysql-使用sysbench进行-其它测试（三）.md
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
title: mysql-使用sysbench进行-其它测试（三）.md
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
1、 只查询的qps测试  /usr/local/share/sysbench/oltp_read_write.lua

~~~
sysbench /usr/local/share/sysbench/oltp_point_select.lua --mysql-host=192.168.0.100 --mysql-port=3306 --mysql-db=test1 --mysql-user=root --mysql-password=Sgl20@14 --table_size=200000 --tables=8 --threads=16 --report-interval=10 --rand-type=uniform --time=36000 --percentile=99 run > test.log
~~~
