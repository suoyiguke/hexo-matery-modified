---
title: explain-for-connection用法.md
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
title: explain-for-connection用法.md
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
当show processlist时遇到慢sql通常会去看sql的执行计划。如果sql过长会显示不全。一般我们会使用show full processlist去查看完整的语句并explain语句得到执行计划。也可以使用explain for connection直接查看正在执行sql的执行计划。例如：

mysql> show processlist;
+----+------+-----------------+------+---------+------+----------+------------------+
| Id | User | Host            | db   | Command | Time | State    | Info             |
+----+------+-----------------+------+---------+------+----------+------------------+
|  4 | root | localhost:51335 | NULL | Query   |    0 | starting | select * from cctest |
+----+------+-----------------+------+---------+------+----------+------------------+

mysql> explain for connection 4;
+----+-------------+--------+------------+------+---------------+------+---------+------+------+----------+-------+
| id | select_type | table  | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra |
+----+-------------+--------+------------+------+---------------+------+---------+------+------+----------+-------+
|  1 | SIMPLE      | cctest | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    2 |   100.00 | NULL  |
+----+-------------+--------+------------+------+---------------+------+---------+------+------+----------+-----
