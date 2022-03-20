---
title: mysql-null-问题.md
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
title: mysql-null-问题.md
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
1、列中有Null值是可以用到索引的
~~~
mysql> EXPLAIN SELECT
	* 
FROM
	`test` FORCE INDEX ( idx_name ) 
WHERE
	isNull( `name` ) 
	AND id = 1
    -> ;
+----+-------------+-------+------------+------+---------------+----------+---------+-------------+------+----------+--------------------------+
| id | select_type | table | partitions | type | possible_keys | key      | key_len | ref         | rows | filtered | Extra                    |
+----+-------------+-------+------------+------+---------------+----------+---------+-------------+------+----------+--------------------------+
|  1 | SIMPLE      | test  | NULL       | ref  | idx_name      | idx_name | 1027    | const,const |    1 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+------+---------------+----------+---------+-------------+------+----------+--------------------------+
1 row in set (0.03 sec)

mysql> 
~~~

2、推荐使用isNull( `name` )  代替 name is null。阿里手册推荐这样写

【强制】使用 ISNULL()来判断是否为 NULL 值。
说明：NULL 与任何值的直接比较都为 NULL。 1） NULL<>NULL 的返回结果是 NULL，而不是 false。 2） NULL=NULL 的返回结果是 NULL，而不是 true。 3） NULL<>1 的返回结果是 NULL，而不是 true。
反例：在 SQL 语句中，如果在 null 前换行，影响可读性。select * from table where column1 is null and 
column3 is not null; 而`ISNULL(column)`是一个整体，简洁易懂。从性能数据上分析，`ISNULL(column)`
执行效率更快一些。


3、count 数据丢失。  请使用 count(*)

4、distint 数据丢失  count(name,age)  name其中有一个为null，数据就会丢失

5、where name<>'java'  、!= 不等于可会丢失Null数据

6、sum() 返回null，如果在java中没有非空判断，name会报空指针。
要么在java中解决，要么数据库中
~~~
SELECT
	SUM(IFNULL(`age`,0) ) 
FROM
	`test` 
~~~

