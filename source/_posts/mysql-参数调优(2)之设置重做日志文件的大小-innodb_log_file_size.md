---
title: mysql-参数调优(2)之设置重做日志文件的大小-innodb_log_file_size.md
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
title: mysql-参数调优(2)之设置重做日志文件的大小-innodb_log_file_size.md
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
>innodb_log_file_size 是仅次于innodb_buffer_pool_size的第二重要的参数。调整它能带来写入性能优化。

我们知道redo log包括 buffer和log file的部分，这里的innodb_log_file_size是配置log file的大小的。


innodb_log_file_size这个选项是设置 redo 日志（重做日志）的大小。这个值的默认为5M，是远远不够的，在安装完mysql时需要尽快的修改这个值。如果对 Innodb 数据表有大量的写入操作，那么选择合适的 innodb_log_file_size 值对提升MySQL性能很重要。然而设置太大了，就会增加恢复的时间，因此在MySQL崩溃或者突然断电等情况会令MySQL服务器花很长时间来恢复。

* 小日志文件使写入速度更慢，崩溃恢复速度更快

由于事务日志相当于一个写缓冲，而小日志文件会很快的被写满，这时候就需要频繁地刷新到硬盘，速度就慢了。如果产生大量的写操作，MySQL可能就不能足够快地刷新数据，那么写性能将会降低。



* 大日志文件使写入更快，崩溃恢复速度更慢

大的日志文件，另一方面，在刷新操作发生之前给你足够的空间来使用。反过来允许InnoDB填充更多的页面。对于崩溃恢复 – 大的重做日志意味着在服务器启动前更多的数据需要读取，更多的更改需要重做，这就是为什么崩溃恢复慢了。



如果不配的后果：默认是5M，这是肯定不够的。


###估算 innodb_log_file_size


最后，让我们来谈谈如何找出重做日志的正确大小。
幸运的是，你不需要费力算出正确的大小，这里有一个经验法则：在服务器繁忙期间，检查重做日志的总大小是否够写入1-2小时。你如何知道InnoDB写入多少，使用下面方法可以统计60秒内地增量数据大小：

mysql> show engine innodb status\G select sleep(60); show engine innodb status\G
Log sequence number 4631632062
...
Log sequence number 4803805448
 
mysql> select (4803805448-4631632062)*60/1024/1024;
+--------------------------------------+
| (4803805448-4631632062)*60/1024/1024 |
+--------------------------------------+
|                        9851.84017181 |
+--------------------------------------+
1 row in set (0.00 sec)

在这个60s的采样情况下，InnoDB每小时写入9.8GB数据。所以如果innodb_log_files_in_group没有更改(默认是2，是InnoDB重复日志的最小数字)，然后设置innodb_log_file_size为10G，那么你实际上两个日志文件加起来有20GB，够你写两小时数据了。

###更改重做日志大小

更改innodb_log_file_size的难易程度和能设置多大取决于你现在使用的MySQL版本。特别地，如果你使用的是5.6之前的版本，你不能仅仅的更改变量，期望服务器会自动重启。
好了，下面是步骤：
1、在my.cnf更改innodb_log_file_size
~~~
innodb_log_file_size=10G
innodb_log_files_in_group=2
~~~
2、停止mysql服务器
3、删除旧的日志,通过执行命令rm -f /var/lib/mysql/ib_logfile*
4、启动mysql服务器 – 应该需要比之前长点的时间，因为需要创建新的事务日志。最后，需要注意的是，有些mysql版本(比如5.6.2)限制了重做日志大小为4GB。所以在你设置innodb_log_file_size为2G或者更多时，请先检查一下MySQL的版本这方面的限制。
