---
title: dbt3和官方的empoyee库.md
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
title: dbt3和官方的empoyee库.md
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
俩个库：dbt3和官方的empoyee库（Exampel databsles）

###dbt3库
下订单的库
~~~
(root@localhost) [(none)]>use dbt3;
Database changed
(root@localhost) [dbt3]>show tables;
+-----------------+
| Tables_in_dbt3  |
+-----------------+
| customer    客户    |
| lineitem   订单详情     |
| nation          |
| orders     订单表     |
| part            |
| partsupp        |
| region          |
| supplier        |
| time_statistics  |
+-----------------+
9 rows in set (0.00 sec)

(root@localhost) [dbt3]>show table status;
+-----------------+--------+---------+------------+---------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+-------------------+----------+----------------+---------+
| Name            | Engine | Version | Row_format | Rows    | Avg_row_length | Data_length | Max_data_length | Index_length | Data_free | Auto_increment | Create_time         | Update_time | Check_time | Collation         | Checksum | Create_options | Comment |
+-----------------+--------+---------+------------+---------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+-------------------+----------+----------------+---------+
| customer        | InnoDB |      10 | Dynamic    |  147674 |            202 |    29949952 |               0 |      3686400 |         0 |           NULL | 2021-05-29 17:24:53 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| lineitem        | InnoDB |      10 | Dynamic    | 5393375 |            155 |   836763648 |               0 |   1402290176 |   4194304 |           NULL | 2021-05-29 17:24:58 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| nation          | InnoDB |      10 | Dynamic    |      25 |            655 |       16384 |               0 |        16384 |         0 |           NULL | 2021-05-29 18:09:37 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| orders          | InnoDB |      10 | Dynamic    | 1372000 |            134 |   184221696 |               0 |     73547776 |   6291456 |           NULL | 2021-05-29 18:09:37 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| part            | InnoDB |      10 | Dynamic    |  198303 |            166 |    33095680 |               0 |            0 |         0 |           NULL | 2021-05-29 18:13:40 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| partsupp        | InnoDB |      10 | Dynamic    |  781222 |            182 |   142278656 |               0 |     31522816 |   6291456 |           NULL | 2021-05-29 18:13:45 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| region          | InnoDB |      10 | Dynamic    |       5 |           3276 |       16384 |               0 |            0 |         0 |           NULL | 2021-05-29 18:14:17 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| supplier        | InnoDB |      10 | Dynamic    |    9674 |            272 |     2637824 |               0 |       294912 |         0 |           NULL | 2021-05-29 18:14:17 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
| time_statistics | InnoDB |      10 | Dynamic    |      15 |           1092 |       16384 |               0 |            0 |         0 |           NULL | 2021-05-29 18:14:17 | NULL        | NULL       | latin1_swedish_ci |     NULL |                |         |
+-----------------+--------+---------+------------+---------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+-------------------+----------+----------------+---------+
9 rows in set (0.00 sec)
(root@localhost) [dbt3]>select count(*) from lineitem;
+----------+
| count(*) |
+----------+
|  6001215 |
+----------+
1 row in set (1 min 48.57 sec)


~~~


###employees库

~~~
(root@localhost) [dbt3]>use employees;
Database changed
(root@localhost) [employees]>show table status;
+--------------+--------+---------+------------+---------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------+
| Name         | Engine | Version | Row_format | Rows    | Avg_row_length | Data_length | Max_data_length | Index_length | Data_free | Auto_increment | Create_time         | Update_time         | Check_time | Collation          | Checksum | Create_options | Comment |
+--------------+--------+---------+------------+---------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------+
| departments  | InnoDB |      10 | Dynamic    |       9 |           1820 |       16384 |               0 |        16384 |         0 |           NULL | 2021-05-30 17:25:30 | 2021-05-30 17:25:30 | NULL       | utf8mb4_general_ci |     NULL |                |         |
| dept_emp     | InnoDB |      10 | Dynamic    |  331143 |             36 |    12075008 |               0 |     11567104 |   4194304 |           NULL | 2021-05-30 17:25:30 | 2021-05-30 17:25:37 | NULL       | utf8mb4_general_ci |     NULL |                |         |
| dept_manager | InnoDB |      10 | Dynamic    |      24 |            682 |       16384 |               0 |        32768 |         0 |           NULL | 2021-05-30 17:25:37 | 2021-05-30 17:25:37 | NULL       | utf8mb4_general_ci |     NULL |                |         |
| employees    | InnoDB |      10 | Dynamic    |  300043 |             50 |    15220736 |               0 |            0 |   4194304 |           NULL | 2021-05-30 17:25:37 | 2021-05-30 17:25:42 | NULL       | utf8mb4_general_ci |     NULL |                |         |
| salaries     | InnoDB |      10 | Dynamic    | 2838426 |             35 |   100270080 |               0 |     36241408 |   5242880 |           NULL | 2021-05-30 17:25:42 | 2021-05-30 17:26:12 | NULL       | utf8mb4_general_ci |     NULL |                |         |
| titles       | InnoDB |      10 | Dynamic    |  442605 |             46 |    20512768 |               0 |     11059200 |   6291456 |           NULL | 2021-05-30 17:26:12 | 2021-05-30 17:26:18 | NULL       | utf8mb4_general_ci |     NULL |                |         |
+--------------+--------+---------+------------+---------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------+
6 rows in set (0.00 sec)

(root@localhost) [employees]>show tables;
+---------------------+
| Tables_in_employees |
+---------------------+
| departments         |
| dept_emp            |
| dept_manager        |
| employees           |
| salaries            |
| titles              |
+---------------------+
6 rows in set (0.00 sec)

~~~
