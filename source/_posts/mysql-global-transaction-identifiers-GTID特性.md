---
title: mysql-global-transaction-identifiers-GTID特性.md
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
title: mysql-global-transaction-identifiers-GTID特性.md
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
###如何知道事务是否在一组中
如何知道事务是否在一组中，又是一个问题，因为原版的MySQL并没有提供这样的信息。在MySQL 5.7版本中，其设计方式是将组提交的信息存放在GTID中。那么如果用户没有开启GTID功能，即将参数gtid_mode设置为OFF呢？故MySQL 5.7又引入了称之为Anonymous_Gtid的二进制日志event类型，如：
~~~
mysql> SHOW BINLOG EVENTS in 'mysql-bin.000006';
+------------------+-----+----------------+-----------+-------------+-----------------------------------------------+
| Log_name | Pos | Event_type | Server_id | End_log_pos | Info |
+------------------+-----+----------------+-----------+-------------+-----------------------------------------------+
| mysql-bin.000006 | 4 | Format_desc | 88 | 123 | Server ver: 5.7.7-rc-debug-log, Binlog ver: 4 |
| mysql-bin.000006 | 123 | Previous_gtids | 88 | 194 | f11232f7-ff07-11e4-8fbb-00ff55e152c6:1-2 |
| mysql-bin.000006 | 194 | Anonymous_Gtid | 88 | 259 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS' |
| mysql-bin.000006 | 259 | Query | 88 | 330 | BEGIN |
| mysql-bin.000006 | 330 | Table_map | 88 | 373 | table_id: 108 (aaa.t) |
| mysql-bin.000006 | 373 | Write_rows | 88 | 413 | table_id: 108 flags: STMT_END_F |
~~~
这意味着在 MySQL 5.7版本中即使不开启GTID，每个事务开始前也是会存在一个Anonymous_Gtid ，而这GTID中就存在着组提交的信息。

LOGICAL_CLOCK

然而，通过上述的SHOW BINLOG EVENTS，我们并没有发现有关组提交的任何信息。但是通过mysqlbinlog工具，用户就能发现组提交的内部信息：
>linux下使用   mysqlbinlog mysql-bin.0000006 | grep last_committed
>windows下使用  mysqlbinlog mysql-bin.0000006 | findstr last_committed
~~~
root@localhost:~# mysqlbinlog mysql-bin.0000006 | grep last_committed
#150520 14:23:11 server id 88 end_log_pos 259 CRC32 0x4ead9ad6 GTID last_committed=0 sequence_number=1
#150520 14:23:11 server id 88 end_log_pos 1483 CRC32 0xdf94bc85 GTID last_committed=0 sequence_number=2
#150520 14:23:11 server id 88 end_log_pos 2708 CRC32 0x0914697b GTID last_committed=0 sequence_number=3
#150520 14:23:11 server id 88 end_log_pos 3934 CRC32 0xd9cb4a43 GTID last_committed=0 sequence_number=4
#150520 14:23:11 server id 88 end_log_pos 5159 CRC32 0x06a6f531 GTID last_committed=0 sequence_number=5
#150520 14:23:11 server id 88 end_log_pos 6386 CRC32 0xd6cae930 GTID last_committed=0 sequence_number=6
#150520 14:23:11 server id 88 end_log_pos 7610 CRC32 0xa1ea531c GTID last_committed=6 sequence_number=7
#150520 14:23:11 server id 88 end_log_pos 8834 CRC32 0x96864e6b GTID last_committed=6 sequence_number=8
#150520 14:23:11 server id 88 end_log_pos 10057 CRC32 0x2de1ae55 GTID last_committed=6 sequence_number=9
#150520 14:23:11 server id 88 end_log_pos 11280 CRC32 0x5eb13091 GTID last_committed=6 sequence_number=10
#150520 14:23:11 server id 88 end_log_pos 12504 CRC32 0x16721011 GTID last_committed=6 sequence_number=11
#150520 14:23:11 server id 88 end_log_pos 13727 CRC32 0xe2210ab6 GTID last_committed=6 sequence_number=12
#150520 14:23:11 server id 88 end_log_pos 14952 CRC32 0xf41181d3 GTID last_committed=12 sequence_number=13
~~~
可以发现较之原来的二进制日志内容多了last_committed和sequence_number，last_committed表示事务提交的时候，上次事务提交的编号，如果事务具有相同的last_committed，表示这些事务都在一组内，可以进行并行的回放。例如上述last_committed为0的事务有6个，表示组提交时提交了6个事务，而这6个事务在从机是可以进行并行回放的。

上述的last_committed和sequence_number代表的就是所谓的LOGICAL_CLOCK。先来看源码中对于LOGICAL_CLOCK的定义：


###那些事务会被纳入同一组？怎么我的循环insert都是单个组并没有被纳入组？
