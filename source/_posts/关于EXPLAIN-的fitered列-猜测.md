---
title: 关于EXPLAIN-的fitered列-猜测.md
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
title: 关于EXPLAIN-的fitered列-猜测.md
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
1、where走索引，fitered总是等于100，显示Using where; Using index，type显示range

2、`错误` 没有走索引就会出现小于100的数值，且显示Using where，type显示All

3、`错误` fitered等于100是最好的情况




走索引
~~~
mysql> EXPLAIN SELECT id,main_platform_order_no
 FROM jg_original_order force index(idx_main_platform_order_no)
 WHERE (main_platform_order_no IN ('|202111180008435318','|20211118000843531239','|2021111800084353151','|20211118000843531622','|202111180008435317','|202111180008435314','|202111180008435323','|202111180008435313','|202111180008435312410','|20211118000843531223','|20211118000811','|2021111800084312'));
+----+-------------+-------------------+------------+-------+----------------------------+----------------------------+---------+------+------+----------+--------------------------+
| id | select_type | table             | partitions | type  | possible_keys              | key                        | key_len | ref  | rows | filtered | Extra                    |
+----+-------------+-------------------+------------+-------+----------------------------+----------------------------+---------+------+------+----------+--------------------------+
|  1 | SIMPLE      | jg_original_order | NULL       | range | idx_main_platform_order_no | idx_main_platform_order_no | 403     | NULL |   12 |   100.00 | Using where; Using index |
+----+-------------+-------------------+------------+-------+----------------------------+----------------------------+---------+------+------+----------+--------------------------+
1 row in set (0.04 sec)

mysql> 
~~~

没走索引
~~~
mysql> EXPLAIN SELECT id,main_platform_order_no
 FROM jg_original_order ignore index(idx_main_platform_order_no)
 WHERE (main_platform_order_no IN ('|202111180008435318','|20211118000843531239','|2021111800084353151','|20211118000843531622','|202111180008435317','|202111180008435314','|202111180008435323','|202111180008435313','|202111180008435312410','|20211118000843531223','|20211118000811','|2021111800084312'));
+----+-------------+-------------------+------------+------+---------------+------+---------+------+------+----------+-------------+
| id | select_type | table             | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------------------+------------+------+---------------+------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | jg_original_order | NULL       | ALL  | NULL          | NULL | NULL    | NULL |   13 |    50.00 | Using where |
+----+-------------+-------------------+------------+------+---------------+------+---------+------+------+----------+-------------+
1 row in set (0.04 sec)

mysql> 
~~~



### filtered列正确的理解

该列表示按表条件过滤的表行的估计百分比。最大值为100，这表示未过滤行。值从100减小表示过滤量增加。

![图片](https://upload-images.jianshu.io/upload_images/13965490-94bad94138da7cd6?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

rows显示了检查的估计行数，rows× filtered显示了与下表连接的行数。例如，如果 rows为1000且 filtered为50.00（50％），则与下表连接的行数为1000×50％= 500
