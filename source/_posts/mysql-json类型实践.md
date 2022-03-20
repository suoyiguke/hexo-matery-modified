---
title: mysql-json类型实践.md
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
title: mysql-json类型实践.md
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
###create
create table t2 (id int primary key, r1 json);


###insert
~~~
INSERT INTO `test`.`t2`(`id`, `r1`) VALUES (1, '{\"x\": \"1\", \"y\": 10}');
INSERT INTO `test`.`t2`(`id`, `r1`) VALUES (2, '{\"x\": \"2\", \"y\": 20}');
INSERT INTO `test`.`t2`(`id`, `r1`) VALUES (3, '{\"x\": \"a\", \"y\": 20}');
INSERT INTO `test`.`t2`(`id`, `r1`) VALUES (4, '{\"x\": \"A\", \"y\": 20}');
~~~
###select
 select * from t2 where r1->>'$.x'='a'



###如何让json类型的查询走索引？
>在mysql8中我们可以使用函数索引来达到这个目的


所以针对 JSON 字段来建立新的函数索引：
~~~
<localhost|mysql>alter table t2 add key idx_func_index_2((cast(r1->>'$.x' as char(1)) collate utf8mb4_bin));
Query OK, 0 rows affected (0.07 sec)
Records: 0  Duplicates: 0  Warnings: 0
~~~
看下表结构，操作符 ->> 被转换为 json_unquote(json_extract(…))，并且排序规则为 utf8mb4_bin。

~~~
<localhost|mysql>show create table t2\G
*************************** 1. row ***************************
      Table: t2
...
 KEY `idx_func_index_2` (((cast(json_unquote(json_extract(`r1`,_utf8mb4'$.x')) as char(1) charset utf8mb4) collate utf8mb4_bin)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
~~~
接下来插入几条记录，看看这个函数索引的使用。
~~~
<localhost|mysql>select * from t2;
+----+---------------------+
| id | r1                  |
+----+---------------------+
|  1 | {"x": "1", "y": 10} |
|  2 | {"x": "2", "y": 20} |
|  3 | {"x": "a", "y": 20} |
|  4 | {"x": "A", "y": 20} |
+----+---------------------+
4 rows in set (0.00 sec)
~~~
执行下 SQL 2，并且看下执行计划，直接走了刚才创建的函数索引。
~~~
# SQL 2
<localhost|mysql>select * from t2 where r1->>'$.x'='a';
+----+---------------------+
| id | r1                  |
+----+---------------------+
|  3 | {"x": "a", "y": 20} |
+----+---------------------+
1 row in set (0.00 sec)

<localhost|mysql>explain select * from t2 where r1->>'$.x'='a'\G
*************************** 1. row ***************************
          id: 1
 select_type: SIMPLE
       table: t2
  partitions: NULL
        type: ref
possible_keys: idx_func_index_2
         key: idx_func_index_2
     key_len: 7
         ref: const
        rows: 1
    filtered: 100.00
       Extra: NULL
1 row in set, 1 warning (0.00 sec)
~~~
