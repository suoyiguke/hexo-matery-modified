---
title: mysql-主从复制-相关配置.md
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
title: mysql-主从复制-相关配置.md
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
1、从中设置log_slave_updates=ON且开启binlog（log_bin=mysql-bin）时，会将主库发过来的的events也记录为binlog保存下来；
show VARIABLES like '%log_slave_updates%'
常用于多级别、级联的主从复制架构中充当中间件的mysql从机；
若不配置则默认为NO，表示从机不记录从主库发过来的binlog

2、一致性相关
innodb_flush_log_at_trx_commit=1
sync_binlog=1


3、复制安全
relay_log_info_repository = TABLE
master_info_repository = TABLE
sync_relay_log = 1
sync_master_info = 1


4、影响复制安全的参数
结论
•5.6.22版本增加了Abort_server选项
•5.6版本默认值为IGNORE_ERROR
•5.7版本默认值为ABORT_SERVER
•该参数支持动态修改
•推荐生产环境配置ABORT_SERVER

分析
binlog_error_action
•ignore_error
•abort_server

验证：ABORT_SERVER
Error message: Binary logging not possible. Either disk
is full or file system is read only while rotating the
binlog. Aborting the server



binlog_error_action参数的意义在保证正确的写入binary log日志，
，默认值为 ABORT_SERVER，当出现错误的时候会使 MySQL 在写 binlog 遇到严重错误时直接退出( 即 Crash 动作)
当binlog_error_action设置为IGNORE_ERROR时，如果服务器遇到这样的错误，它将继续正在进行的事务，记录错误，然后停止日志记录，并继续执行更新。要恢复二进制日志记录，必须再次启用log_bin，这需要重新启动服务器。
