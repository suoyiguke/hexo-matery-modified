---
title: 为什么不推荐使用unsigned.md
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
title: 为什么不推荐使用unsigned.md
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
在整型类型中，有 signed 和 unsigned 属性，其表示的是整型的取值范围，默认为 signed。在设计时，我不建议你刻意去用 unsigned 属性，因为在做一些数据分析时，SQL 可能返回的结果并不是想要得到的结果。

来看一个“销售表 sale”的例子，其表结构和数据如下。这里要特别注意，列 sale_count 用到的是 unsigned 属性（即设计时希望列存储的数值大于等于 0）：

~~~
mysql> SHOW CREATE TABLE sale\G
*************************** 1. row ***************************
       Table: sale
Create Table: CREATE TABLE `sale` (
  `sale_date` date NOT NULL,
  `sale_count` int unsigned DEFAULT NULL,
  PRIMARY KEY (`sale_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
1 row in set (0.00 sec)

mysql> SELECT * FROM sale;
+------------+------------+
| sale_date  | sale_count |
+------------+------------+
| 2020-01-01 |      10000 |
| 2020-02-01 |       8000 |
| 2020-03-01 |      12000 |
| 2020-04-01 |       9000 |
| 2020-05-01 |      10000 |
| 2020-06-01 |      18000 |
+------------+------------+
6 rows in set (0.00 sec)

~~~
其中，sale_date 表示销售的日期，sale_count 表示每月的销售数量。现在有一个需求，老板想要统计每个月销售数量的变化，以此做商业决策。这条 SQL 语句需要应用到非等值连接，但也并不是太难写：

~~~
SELECT
    s1.sale_date, s2.sale_count - s1.sale_count AS diff
FROM
    sale s1
        LEFT JOIN
    sale s2 ON DATE_ADD(s2.sale_date, INTERVAL 1 MONTH) = s1.sale_date
ORDER BY sale_date;
然而，在执行的过程中，由于列 sale_count 用到了 unsigned 属性，会抛出这样的结果：
~~~

ERROR 1690 (22003): BIGINT UNSIGNED value is out of range in '(`test`.`s2`.`sale_count` - `test`.`s1`.`sale_count`)'
可以看到，MySQL 提示用户计算的结果超出了范围。其实，这里 MySQL 要求 unsigned 数值相减之后依然为 unsigned，否则就会报错。

为了避免这个错误，需要对数据库参数 sql_mode 设置为 NO_UNSIGNED_SUBTRACTION，允许相减的结果为 signed，这样才能得到最终想要的结果：

~~~
mysql> SET sql_mode='NO_UNSIGNED_SUBTRACTION';
Query OK, 0 rows affected (0.00 sec)
SELECT

    s1.sale_date,
    IFNULL(s2.sale_count - s1.sale_count,'') AS diff
FROM
    sale s1
    LEFT JOIN sale s2 
    ON DATE_ADD(s2.sale_date, INTERVAL 1 MONTH) = s1.sale_date
ORDER BY sale_date;

+------------+-------+
| sale_date  | diff  |
+------------+-------+
| 2020-01-01 |       |
| 2020-02-01 | 2000  |
| 2020-03-01 | -4000 |
| 2020-04-01 | 3000  |
| 2020-05-01 | -1000 |
| 2020-06-01 | -8000 |
+------------+-------+
6 rows in set (0.00 sec)
~~~
