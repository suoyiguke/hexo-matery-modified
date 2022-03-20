---
title: mysql-Storage-Engines.md
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
title: mysql-Storage-Engines.md
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
https://dev.mysql.com/doc/refman/5.7/en/storage-engines.html

show engines; 查看当前支持的存储引擎
~~~
(root@localhost) [test]>show engines;
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
9 rows in set (0.00 sec)
~~~

###存储引擎配置
1、请禁用除了innodb以外的其它存储引擎。
5.7中不能skip myisam和skip memory。因为他们有用在系统表中。5.7中我们能配的就是禁用以下三个：
~~~
[mysqld]
skip-federated
skip-archive
skip-blackhole
~~~
~~~
(root@localhost) [(none)]>show engines;
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
| BLACKHOLE          | NO      | /dev/null storage engine (anything you write to it disappears) | NULL         | NULL | NULL       |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
| ARCHIVE            | NO      | Archive storage engine                                         | NULL         | NULL | NULL       |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
9 rows in set (0.00 sec)
~~~

2、show table status 检查业务表的引擎，若有用到其它引擎，请换为innodb。
~~~
alter table test1 engine = innodb;
~~~
>注意，数据量很大的话就要锁表。


###官方存储引擎和第三方存储引擎
官方：
- MyISAM
- InnoDB
- Memory
- federated
- CSV
- Archive

第三方：
- TokuDB
- InfoBright
- Spider
（其实这些东西都不推荐去学习，会有很多问题的）

###是否支持事务？
支持事务：FalconI、InnoDB、TokuDB、WiredTiger
不支持事务：Aria、BlitzDB、MyISAM、InfiniDB

###选择哪一个？
尽可能地使用Innodb，官方的其它引擎已经不再维护！而其它第三方存储引擎说性能有多强，都是在特定的环境下测试的。我们普遍来讲innodb才是最可靠的。

只在特定场景下使用第三方的存储引擎：
- TokuDB：插入密集型
- InfoBright：OLAP场景
这些三方引擎都有问题，TokuDB插入的确很快，查询性能不能接受，像range查询起来慢。只是快了某一方面。
InfoBright只对某些类型查询，如SUM快。但是大量的JOIN根本跑不出结果，JOIN列是无序的， 没有二级存。
Spider分布式引擎也有很多坑。

我们只需要把精力都放到innodb上，不要浪费时间到其它引擎上，规避其它引擎的坑。抓住最有价值的innodb！

###mysql系统表的引擎
mysql8之前的版本系统表有些是myisam、csv有些是innodb；
~~~
(root@localhost) [(none)]>use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
(root@localhost) [mysql]>show table status;
+---------------------------+--------+---------+------------+------+----------------+-------------+--------------------+--------------+-----------+----------------+---------------------+---------------------+------------+-------------------+----------+--------------------+-----------------------------------------+
| Name                      | Engine | Version | Row_format | Rows | Avg_row_length | Data_length | Max_data_length    | Index_length | Data_free | Auto_increment | Create_time         | Update_time         | Check_time | Collation         | Checksum | Create_options     | Comment                                 |
+---------------------------+--------+---------+------------+------+----------------+-------------+--------------------+--------------+-----------+----------------+---------------------+---------------------+------------+-------------------+----------+--------------------+-----------------------------------------+
| columns_priv              | MyISAM |      10 | Fixed      |    0 |              0 |           0 | 241505530017742847 |         4096 |         0 |           NULL | 2021-04-18 10:36:36 | 2021-04-18 10:36:36 | NULL       | utf8_bin          |     NULL |                    | Column privileges                       |
| db                        | MyISAM |      10 | Fixed      |    4 |            488 |        1952 | 137359788634800127 |         5120 |         0 |           NULL | 2021-04-18 10:36:36 | 2021-04-18 18:50:08 | NULL       | utf8_bin          |     NULL |                    | Database privileges                     |
| engine_cost               | InnoDB |      10 | Dynamic    |    2 |           8192 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 |                                         |
| event                     | MyISAM |      10 | Dynamic    |    0 |              0 |           0 |    281474976710655 |         2048 |         0 |           NULL | 2021-04-18 10:36:37 | 2021-04-18 10:36:37 | NULL       | utf8_general_ci   |     NULL |                    | Events                                  |
| func                      | MyISAM |      10 | Fixed      |    0 |              0 |           0 | 162974011515469823 |         1024 |         0 |           NULL | 2021-04-18 10:36:36 | 2021-04-18 10:36:36 | NULL       | utf8_bin          |     NULL |                    | User defined functions                  |
| general_log               | CSV    |      10 | Dynamic    |    2 |              0 |           0 |                  0 |            0 |         0 |           NULL | NULL                | NULL                | NULL       | utf8_general_ci   |     NULL |                    | General log                             |
| gtid_executed             | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | latin1_swedish_ci |     NULL |                    |                                         |
| help_category             | InnoDB |      10 | Dynamic    |   48 |            341 |       16384 |                  0 |        16384 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | help categories                         |
| help_keyword              | InnoDB |      10 | Dynamic    |  970 |            118 |      114688 |                  0 |       114688 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | help keywords                           |
| help_relation             | InnoDB |      10 | Dynamic    | 2221 |             44 |       98304 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | keyword-topic relation                  |
| help_topic                | InnoDB |      10 | Dynamic    |  647 |           2456 |     1589248 |                  0 |        98304 |   4194304 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | help topics                             |
| innodb_index_stats        | InnoDB |      10 | Dynamic    |    7 |           2340 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_bin          |     NULL | stats_persistent=0 |                                         |
| innodb_table_stats        | InnoDB |      10 | Dynamic    |    2 |           8192 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_bin          |     NULL | stats_persistent=0 |                                         |
| ndb_binlog_index          | MyISAM |      10 | Dynamic    |    0 |              0 |           0 |    281474976710655 |         1024 |         0 |           NULL | 2021-04-18 10:36:37 | 2021-04-18 10:36:37 | NULL       | latin1_swedish_ci |     NULL |                    |                                         |
| plugin                    | InnoDB |      10 | Dynamic    |    1 |          16384 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | MySQL plugins                           |
| proc                      | MyISAM |      10 | Dynamic    |   48 |           6277 |      301304 |    281474976710655 |         4096 |         0 |           NULL | 2021-04-18 10:36:37 | 2021-04-18 10:36:37 | NULL       | utf8_general_ci   |     NULL |                    | Stored Procedures                       |
| procs_priv                | MyISAM |      10 | Fixed      |    0 |              0 |           0 | 266275327968280575 |         4096 |         0 |           NULL | 2021-04-18 10:36:37 | 2021-04-18 10:36:37 | NULL       | utf8_bin          |     NULL |                    | Procedure privileges                    |
| proxies_priv              | MyISAM |      10 | Fixed      |    1 |            837 |         837 | 235594555506819071 |         9216 |         0 |           NULL | 2021-04-18 10:36:37 | 2021-04-18 10:36:37 | NULL       | utf8_bin          |     NULL |                    | User proxy privileges                   |
| server_cost               | InnoDB |      10 | Dynamic    |    6 |           2730 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 |                                         |
| servers                   | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | MySQL Foreign Servers table             |
| slave_master_info         | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Master Information                      |
| slave_relay_log_info      | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Relay Log Information                   |
| slave_worker_info         | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Worker Information                      |
| slow_log                  | CSV    |      10 | Dynamic    |    2 |              0 |           0 |                  0 |            0 |         0 |           NULL | NULL                | NULL                | NULL       | utf8_general_ci   |     NULL |                    | Slow log                                |
| tables_priv               | MyISAM |      10 | Fixed      |    2 |            947 |        1894 | 266556802944991231 |         9216 |         0 |           NULL | 2021-04-18 10:36:36 | 2021-04-18 10:36:37 | NULL       | utf8_bin          |     NULL |                    | Table privileges                        |
| time_zone                 | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |              1 | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Time zones                              |
| time_zone_leap_second     | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Leap seconds information for time zones |
| time_zone_name            | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Time zone names                         |
| time_zone_transition      | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Time zone transitions                   |
| time_zone_transition_type | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                  0 |            0 |         0 |           NULL | 2021-04-18 10:37:50 | NULL                | NULL       | utf8_general_ci   |     NULL | stats_persistent=0 | Time zone transition types              |
| user                      | MyISAM |      10 | Dynamic    |    5 |            129 |         648 |    281474976710655 |         4096 |         0 |           NULL | 2021-04-18 10:36:36 | 2021-05-03 10:59:08 | NULL       | utf8_bin          |     NULL |                    | Users and global privileges             |
+---------------------------+--------+---------+------------+------+----------------+-------------+--------------------+--------------+-----------+----------------+---------------------+---------------------+------------+-------------------+----------+--------------------+-----------------------------------------+

~~~
在mysql8.0后系统表把原来的myisam统一为innodb了，当然general_log 和slow_log 还是CSV。如下：
~~~
(root@localhost) [(none)]>use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
(root@localhost) [mysql]>show table status;
+------------------------------------------------------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+--------------------+----------+---------------------------------------+------------------------------------------+
| Name                                                 | Engine | Version | Row_format | Rows | Avg_row_length | Data_length | Max_data_length | Index_length | Data_free | Auto_increment | Create_time         | Update_time | Check_time | Collation          | Checksum | Create_options                        | Comment                                  |
+------------------------------------------------------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+--------------------+----------+---------------------------------------+------------------------------------------+
| columns_priv                                         | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Column privileges                        |
| component                                            | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |              1 | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC                    | Components                               |
| db                                                   | InnoDB |      10 | Dynamic    |    2 |           8192 |       16384 |               0 |        16384 |   4194304 |           NULL | 2021-05-05 16:19:55 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Database privileges                      |
| default_roles                                        | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Default roles                            |
| engine_cost                                          | InnoDB |      10 | Dynamic    |    2 |           8192 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 |                                          |
| func                                                 | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | User defined functions                   |
| general_log                                          | CSV    |      10 | Dynamic    |    2 |              0 |           0 |               0 |            0 |         0 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL |                                       | General log                              |
| global_grants                                        | InnoDB |      10 | Dynamic    |   67 |            978 |       65536 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Extended global grants                   |
| gtid_executed                                        | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8mb4_0900_ai_ci |     NULL | row_format=DYNAMIC                    |                                          |
| help_category                                        | InnoDB |      10 | Dynamic    |   53 |            309 |       16384 |               0 |        16384 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | help categories                          |
| help_keyword                                         | InnoDB |      10 | Dynamic    |  868 |            151 |      131072 |               0 |       131072 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | help keywords                            |
| help_relation                                        | InnoDB |      10 | Dynamic    | 1706 |             57 |       98304 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | keyword-topic relation                   |
| help_topic                                           | InnoDB |      10 | Dynamic    |  574 |           2768 |     1589248 |               0 |        98304 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | help topics                              |
| innodb_index_stats                                   | InnoDB |      10 | Dynamic    |   10 |           1638 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 08:19:51 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 |                                          |
| innodb_table_stats                                   | InnoDB |      10 | Dynamic    |    3 |           5461 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 08:19:51 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 |                                          |
| password_history                                     | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Password history for user accounts       |
| plugin                                               | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | MySQL plugins                            |
| procs_priv                                           | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |        16384 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Procedure privileges                     |
| proxies_priv                                         | InnoDB |      10 | Dynamic    |    1 |          16384 |       16384 |               0 |        16384 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | User proxy privileges                    |
| replication_asynchronous_connection_failover         | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |        16384 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | The source configuration details         |
| replication_asynchronous_connection_failover_managed | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | The managed source configuration details |
| role_edges                                           | InnoDB |      10 | Dynamic    |    1 |          16384 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Role hierarchy and role grants           |
| server_cost                                          | InnoDB |      10 | Dynamic    |    6 |           2730 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 |                                          |
| servers                                              | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | MySQL Foreign Servers table              |
| slave_master_info                                    | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Master Information                       |
| slave_relay_log_info                                 | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Relay Log Information                    |
| slave_worker_info                                    | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Worker Information                       |
| slow_log                                             | CSV    |      10 | Dynamic    |    2 |              0 |           0 |               0 |            0 |         0 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL |                                       | Slow log                                 |
| tables_priv                                          | InnoDB |      10 | Dynamic    |    2 |           8192 |       16384 |               0 |        16384 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Table privileges                         |
| time_zone                                            | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |              1 | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Time zones                               |
| time_zone_leap_second                                | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Leap seconds information for time zones  |
| time_zone_name                                       | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Time zone names                          |
| time_zone_transition                                 | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Time zone transitions                    |
| time_zone_transition_type                            | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_general_ci    |     NULL | row_format=DYNAMIC stats_persistent=0 | Time zone transition types               |
| user                                                 | InnoDB |      10 | Dynamic    |    7 |           2340 |       16384 |               0 |            0 |   4194304 |           NULL | 2021-05-05 16:19:56 | NULL        | NULL       | utf8_bin           |     NULL | row_format=DYNAMIC stats_persistent=0 | Users and global privileges              |
+------------------------------------------------------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+--------------------+----------+---------------------------------------+------------------------------------------+
35 rows in set (0.04 sec)

(root@localhost) [mysql]>
~~~

这是一个非常大的改进，未来可能支持ddl的回滚。数据定义的回滚。
mysql8 已经实现ddl的原子性了。





###一些引擎的介绍信息
**MyISAM**

- mysql5.1之前的默认引擎
- 表锁设计
- 堆表数据结构
- 支持数据静态压缩
- 不支持事务
- 数据容易丢失
- 索引容易损坏
- 优点：1、数据文件可以直接copy到另一台服务器使用 2、count(*) 快

myisam是非常糟糕的；有人说myisam读取快，是不成立的。现在的innodb在读方面绝对比myisam快。
我们现在count(*) 都是放缓存的。通过CAS进行计数，通过值来访问。


**Memory**
- 全内存存储
- 数据库重启后数据丢失
- 支持哈希索引
- 不支持事务

有人多人喜欢使用memory引擎，因为放到内存中快；其实少量数据放在innodb上它也是放在内存的，只是说数据量大了就会放到磁盘；
而且memory并发并不好，他也是表锁的。
当然memory会用在临时表上，分组时会用到；memory的用处是在数据库内部，而不是对用户。
想要放到内存中为什么不用redis？redis肯定性能更好啊，用mysql还会多一层sql解析。



**CSV**
csv格式是以文本的方式保存数据的。
slow_log表就是CSV引擎的，可以直接查看slow_log.CSV：
~~~
[root@localhost mysql]# cat slow_log.CSV
"2021-05-16 19:03:36.833839","root[root] @ localhost []","00:00:00.000385","00:00:00.000000",1,0,"",0,0,10,"select @@version_comment limit 1",2
"2021-05-16 19:03:36.882537","root[root] @ localhost []","00:00:00.000069","00:00:00.000000",1,0,"",0,0,10,"select USER()",2
"2021-05-16 19:03:54.704466","root[root] @ localhost []","00:00:00.000074","00:00:00.000000",1,0,"",0,0,10,"SELECT DATABASE()",2
"2021-05-16 19:03:54.705472","root[root] @ localhost []","00:00:00.000148","00:00:00.000000",1,0,"mysql",0,0,10,"Init DB",2
"2021-05-16 19:03:54.709006","root[root] @ localhost []","00:00:00.000836","00:00:00.000120",5,5,"mysql",0,0,10,"show databases",2
"2021-05-16 19:03:54.709913","root[root] @ localhost []","00:00:00.000491","00:00:00.000093",31,31,"mysql",0,0,10,"show tables",2
~~~
以逗号分割，那如果字段中包含逗号是不是就有问题了？没有太大的必要去使用它，虽然有些人说使用csv可以直接将txt导入数据库。但是这有必要吗。


~~~
(root@localhost) [(none)]>show create table mysql.slow_log \g
+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table    | Create Table                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| slow_log | CREATE TABLE `slow_log` (
  `start_time` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `user_host` mediumtext NOT NULL,
  `query_time` time(6) NOT NULL,
  `lock_time` time(6) NOT NULL,
  `rows_sent` int(11) NOT NULL,
  `rows_examined` int(11) NOT NULL,
  `db` varchar(512) NOT NULL,
  `last_insert_id` int(11) NOT NULL,
  `insert_id` int(11) NOT NULL,
  `server_id` int(10) unsigned NOT NULL,
  `sql_text` mediumblob NOT NULL,
  `thread_id` bigint(21) unsigned NOT NULL
) ENGINE=CSV DEFAULT CHARSET=utf8 COMMENT='Slow log' |
+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.07 sec)

~~~



**Federated**
非常类似于oracle的dblink，只支持mysql远程访问mysql。有很多问题啊，不要用啊；






###拓展
1、innodb不支持分布式事务。
2、生产环境一定要开双1，毫无疑问！ 当然mysql5.5时双1性能会慢10倍，这个bug 5.6时已经修正。
3、alter table test1 engine = innodb;在修改引擎的过程中表会被锁住。
4、开启slow log 会有性能影响吗？不会，除非系统有很多的慢查询。

