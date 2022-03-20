---
title: Sorted-set.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: Sorted-set.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
1、Sorted-set  是一个按value排序的key-value Map结构。 而java中的TreeMap是按key排序的Map结构。
2、Sorted-set里面使用了跳表的数据结构，因此排序查找等操作性能非常好



127.0.0.1:6379> ZADD SDATA 1 S1
(integer) 1
127.0.0.1:6379> ZADD SDATA 2 S2
(integer) 1
127.0.0.1:6379> ZADD SDATA 3 S3
(integer) 1
127.0.0.1:6379> ZADD SDATA 4 A1
(integer) 1
127.0.0.1:6379> ZADD SDATA 4 A2
(integer) 1
127.0.0.1:6379> ZADD SDATA 4 A3
(integer) 1
127.0.0.1:6379> ZADD SDATA 4 A4
(integer) 1
127.0.0.1:6379> ZRANGE SDATA 0 10 WITHSCORES
 1) "S1"
 2) "1"
 3) "S2"
 4) "2"
 5) "S3"
 6) "3"
 7) "A1"
 8) "4"
 9) "A2"
10) "4"
11) "A3"
12) "4"
13) "A4"
14) "4"
