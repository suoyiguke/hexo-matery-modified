---
title: mysql-主从复制之GTID模式.md
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
title: mysql-主从复制之GTID模式.md
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
从MySQL5.6开始增加了强大的GTID（Global Transaction ID，全局事务ID）这个特性，用来强化数据库的主备一致性， 故障恢复， 以及容错能力。用于取代过去传统的主从复制（即：基于binlog和position的异步复制）。

借助GTID，在发生主备切换的情况下，MySQL的其他slave可以自动在新主上找到正确的复制位置，这大大简化了复杂复制拓扑下集群的维护，也减少了人为设置复制position发生误操作的风险。另外，基于GTID的复制可以忽略已经执行过的事务，减少了数据发生不一致的风险。

只需要在之前的配置基础上加上 
~~~
gtid_mode=ON
enforce_gtid_consistency=1   # 强制执行GTID一致性。
~~~


配置示例：
~~~
[mysqld]
## server_id，一般设置为IP，注意要唯一
server_id=3305
log_bin=mysql-bin
## 需要主从复制的数据库
binlog-do-db=iam
## 开启二进制日志功能，以备Slave作为其它Slave的Master时使用
log_bin = mysql-bin
## 为每个session 分配的内存，在事务过程中用来存储二进制日志的缓存
binlog_cache_size=1M
## 主从复制的格式（mixed,statement,row，默认格式是statement）
binlog_format=row
## 二进制日志自动删除/过期的天数。默认值为0，表示不自动删除。
expire_logs_days=7
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如：1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
## relay_log配置中继日志
relay_log=replicas-mysql-relay-bin
## log_slave_updates表示slave将复制事件写进自己的二进制日志
log_slave_updates=1
lower_case_table_names = 1

gtid_mode=ON
enforce_gtid_consistency=1   # 强制执行GTID一致性。

~~~

使用如下让slave连接到master，不需要指定binlog文件和position了
~~~
CHANGE MASTER TO
MASTER_HOST='192.168.6.128',
MASTER_PORT=33065,
MASTER_USER='root',
MASTER_PASSWORD='root',
MASTER_AUTO_POSITION=1;
~~~
START SLAVE;

show slave status;



>Got fatal error 1236 from master when reading data from binary log: 'The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.'
