---
title: mysql-row类型的-binlog-分析.md
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
title: mysql-row类型的-binlog-分析.md
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
**binlog类型选择**
请一定选择ROW类型，因为它是稳定最安全的。使用其它格式则很可能造成主从不一致

**

当用户提交一条修改语句时(如, insert, update, delete)，MySQL会产生2个Binlog事件: 第一个就是Table_map，用于描述改变对应表的结构(表名, 列的数据类型等信息)；紧接着的是Write_rows，用于描述对应表的行的变化值.
>mysql-bin.000004	171613091	`Table_map`	1918	171613199	table_id: 447 (test.biz_cloudsign_cert_info)
mysql-bin.000004	171613199	`Write_rows`	1918	171615827	table_id: 447 flags: STMT_END_F

![image.png](https://upload-images.jianshu.io/upload_images/13965490-bffc6607757e8354.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**2、rows类型的binlog也可以记录原始sql**

开启binlog_rows_query_log_events参数可以让rows类型binlog也记录sql语句
show VARIABLES like '%binlog_rows_query_log_events%'
binlog_rows_query_log_events =1

如下，291、629、971 pos便是记录的三个insert的sql
~~~
mysql> show binlog EVENTS in 'mysql-bin.000007';
+------------------+------+----------------+-----------+-------------+------------------------------------------------------------+
| Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                       |
+------------------+------+----------------+-----------+-------------+------------------------------------------------------------+
| mysql-bin.000007 |    4 | Format_desc    |         1 |         123 | Server ver: 5.7.15-log, Binlog ver: 4                      |
| mysql-bin.000007 |  123 | Previous_gtids |         1 |         154 |                                                            |
| mysql-bin.000007 |  154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                       |
| mysql-bin.000007 |  219 | Query          |         1 |         291 | BEGIN                                                      |
| mysql-bin.000007 |  291 | Rows_query     |         1 |         369 | # INSERT INTO `test`.`ff`(`id`, `name`) VALUES (5, '44')   |
| mysql-bin.000007 |  369 | Table_map      |         1 |         417 | table_id: 108 (test.ff)                                    |
| mysql-bin.000007 |  417 | Write_rows     |         1 |         461 | table_id: 108 flags: STMT_END_F                            |
| mysql-bin.000007 |  461 | Xid            |         1 |         492 | COMMIT /* xid=26 */                                        |
| mysql-bin.000007 |  492 | Anonymous_Gtid |         1 |         557 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                       |
| mysql-bin.000007 |  557 | Query          |         1 |         629 | BEGIN                                                      |
| mysql-bin.000007 |  629 | Rows_query     |         1 |         709 | # INSERT INTO `test`.`ff`(`id`, `name`) VALUES (6, 'ffff') |
| mysql-bin.000007 |  709 | Table_map      |         1 |         757 | table_id: 108 (test.ff)                                    |
| mysql-bin.000007 |  757 | Write_rows     |         1 |         803 | table_id: 108 flags: STMT_END_F                            |
| mysql-bin.000007 |  803 | Xid            |         1 |         834 | COMMIT /* xid=29 */                                        |
| mysql-bin.000007 |  834 | Anonymous_Gtid |         1 |         899 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                       |
| mysql-bin.000007 |  899 | Query          |         1 |         971 | BEGIN                                                      |
| mysql-bin.000007 |  971 | Rows_query     |         1 |        1050 | # INSERT INTO `test`.`ff`(`id`, `name`) VALUES (7, 'jjj')  |
| mysql-bin.000007 | 1050 | Table_map      |         1 |        1098 | table_id: 108 (test.ff)                                    |
| mysql-bin.000007 | 1098 | Write_rows     |         1 |        1143 | table_id: 108 flags: STMT_END_F                            |
| mysql-bin.000007 | 1143 | Xid            |         1 |        1174 | COMMIT /* xid=32 */                                        |
+------------------+------+----------------+-----------+-------------+------------------------------------------------------------+
20 rows in set (0.03 sec)

mysql> 
~~~
