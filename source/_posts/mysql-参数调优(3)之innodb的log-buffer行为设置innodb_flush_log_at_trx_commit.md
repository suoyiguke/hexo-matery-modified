---
title: mysql-参数调优(3)之innodb的log-buffer行为设置innodb_flush_log_at_trx_commit.md
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
title: mysql-参数调优(3)之innodb的log-buffer行为设置innodb_flush_log_at_trx_commit.md
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
>这个参数直接影响到redo log 数据刷新到磁盘的性能，直接影响到插入、修改和删除的性能


innodb_flush_log_at_trx_commit	1（默认值），0/2 （性能更好，但稳定性更差）


文件操作三个步骤： open、write、fsync
###参数含义

0：redo log buffer将每秒一次地写入redo log file中，并且redo log file的fsync(刷到磁盘)操作同时进行。该模式下在事务提交的时候，不会主动触发写入磁盘的操作。（每秒写入 redo log file，每秒刷新到磁盘）

1：每次事务提交时MySQL都会把redo log buffer的数据写入redo log file，并且执行fsync，该模式为系统默认。（每次事务提交写入 redo log file，每次事务提交刷新到磁盘）

2：每次事务提交时MySQL都会把redo log buffer的数据写入 redo log file，但是fsync操作并不会同时进行。该模式下，MySQL会每秒执行一次 fsync操作。（每次事务提交写入redo log file，每秒批量地将操作系统缓存中地数据刷新到磁盘）

###推荐设置
当设置为0，该模式速度最快，但不太安全，mysqld进程的崩溃会导致上一秒钟所有事务数据的丢失。

当设置为1，该模式是最安全的，但也是最慢的一种方式，也是mysql默认的方式。在mysqld 服务崩溃或者服务器主机crash的情况下，binary log 只有可能丢失最多一个语句或者一个事务。

当设置为2，该模式速度较快，也比0安全，只有在操作系统崩溃或者系统断电的情况下，上一秒钟所有事务数据才可能丢失，mysql宕机都无所谓，因为数据保存在操作系统的文件缓存中。这个参数是5.6所没有的。一些不是对丢失事务零容忍的业务可以设置为2，来获得更好的性能！如果不配，默认为1，影响系统写性能。
~~~
[mysqld]
innodb_flush_log_at_trx_commit=2
~~~

相反对数据完整性要求大的业务 强烈建议使用 innodb_flush_log_at_trx_commit = 1； sync_binlog = 1 ；虽然会很影响性能，但是对于数据很重要的情况下，必须设置。



###应用

在导入大量数据的时候可以暂时将innodb_flush_log_at_trx_commit参数设置为0。来获得最大的执行事务的速度。导入完成后再改为1或者2。


下面看一个例子,比较 innodb_flush_log_at_trx_commit 对事务的影响。首先根据如 下代码创建表t1和存储过程
~~~
CREATE TABLE test_load ( a INT, b CHAR ( 80 ) ) ENGINE = INNODB;

CREATE PROCEDURE p_load ( count INT UNSIGNED ) BEGIN
	DECLARE
		s INT UNSIGNED DEFAULT 1;
	DECLARE
		c CHAR ( 80 ) DEFAULT REPEAT ( 'a', 80 );
		WHILE
				s <= count DO
				INSERT INTO test_load  SELECT NULL,c;	
			COMMIT;
			SET s = s + 1;
		END WHILE;
END;
~~~

存储过程p_load的作用是将数据不断地插入表 testload中,并且每插入条就进行 一次显式的COMMIT操作。在默认的设置下,即参数 innodb_flush_log_at_trx_commit 为1的情况下, InnoDB存储引擎会将重做日志缓冲中的日志写入文件,并调用一次 fsync操作。如果执行命令call p_load(500000) ,则会向表中插入50万行的记录, 并执行50万次的 fsync操作。

可以看到将参数 innodb_flush_log_at_trx_commit  设置为0后,插入50万行记录的时间缩短为了13.90秒,差不多是之前的12%。而形成这个现象的主要原因是:后者大大减少了 fsync的次数,从而提高了数据库执行的性能。


![image.png](https://upload-images.jianshu.io/upload_images/13965490-ec8bfafcef4f73d0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

虽然用户可以通过设置参数 innodb_flush_log_at_trx_commit 为0或2来提高事务提交的性能,但是需要牢记的是,这种设置方法丧失了事务的ACID特性。而针对上述存储过程,为了提高事务的提交性能,应该在将50万行记录插入表后进行一次的 COMMIT操作,而不是在每插入一条记录后进行一次 COMMIT操作。这样做的好处是 还可以使事务方法在回滚时回滚到事务最开始的确定状态。
