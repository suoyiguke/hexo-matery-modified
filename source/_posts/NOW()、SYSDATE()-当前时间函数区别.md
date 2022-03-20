---
title: NOW()、SYSDATE()-当前时间函数区别.md
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
title: NOW()、SYSDATE()-当前时间函数区别.md
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

观察下面的例子

~~~
mysql> SELECT now(),SYSDATE(),sleep(10),now(),SYSDATE();
+-------------------+-------------------+----------+-------------------+-------------------+
| now()             | SYSDATE()        | sleep(10) | now()             | SYSDATE()        |
+-------------------+-------------------+----------+-------------------+-------------------+
| 2021-06-23 15:10:42 | 2021-06-23 15:10:42 |        0 | 2021-06-23 15:10:42 | 2021-06-23 15:10:52 |
+-------------------+-------------------+----------+-------------------+-------------------+
1 row in set (10.04 sec)
~~~

now()是sql语句开始执行的时间，SYSDATE()则是执行到本函数的时间
