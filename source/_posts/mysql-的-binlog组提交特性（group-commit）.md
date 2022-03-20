---
title: mysql-的-binlog组提交特性（group-commit）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-的-binlog组提交特性（group-commit）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
为了提高单位时间内的事务提交数，必须减少事务提交过程中的fsync调用次数
MySQL 从5.6版本开始引入 group commit 技术（MariaDB 5.3版本引入）
**基本思想是多个并发提交的事务共用一次fsync操作来实现持久化**

###原理
多个并发需要提交的事务**共享一次fsync操作**来进行数据的持久化。将fsync操作的开销平摊到多个并发的事务上去
group commit 不是在任何时候都能发挥作用，要有足够多并发的需要提交的事务


###实现
多个并发提交的事务在写redo log或binlog前会被加入到一个队列中；队列头部的事务所在的线程称为leader线程，其它事务所在的线程称为follower线程

leader线程 负责为队列中所有的事务进行写binlog操作，此时，所有的follower线程处于等待状态
然后leader线程 调用 一次fsync操作，将binlog持久化
最后通知follower线程可以继续往下执行


###参数
binlog_group_commit_sync_delay=N
定时发车，在等待N 微秒后，进行binlog刷盘操作
binlog_group_commit_sync_no_delay_count=N
人满发车，达到最大事务等待数量，开始binlog刷盘，忽略定时发车

注意 

1、当binlog_group_commit_sync_delay=0时，binlog_group_commit_sync_no_delay_count参数设置无效，即没有定时发车情况下，人满发车也就没有了~_~

2、当sync_binlog=0或sync_binlog=1，在刷盘前，对每个binlog应用定时发车
当sync_binlog=N（N>1），在每N个binlog后应用定时发车

3、设置了定时发车增加了并发提交事务的数量，从而增加slave并行apply的速度（slave开启多线程复制）
定时发车增加了事务提交的延迟，在高并发情况下，延迟有可能增加争用从而减少吞吐量
定时发车有优点也有缺点，要更具业务负载持续优化来决定最佳设置


###设置
SHOW VARIABLES LIKE '%binlog_group_commit_sync_delay%' 
SHOW VARIABLES LIKE '%binlog_group_commit_sync_no_delay_count%' 
SET GLOBAL binlog_group_commit_sync_delay = 100 
SET GLOBAL binlog_group_commit_sync_no_delay_count = 5







###binlog_group_commit_sync_delay
全局动态变量，单位微妙，默认0，范围：0～1000000（1秒）。
表示binlog提交后等待延迟多少时间再同步到磁盘，默认0，不延迟。设置延迟可以让多个事务在用一时刻提交，提高binlog组提交的并发数和效率，提高slave的吞吐量。


1、该参数控制mysql 组提交之前等待的微秒数，设置该参数可以让组提交的每个组里面的事务数更多（因为他等待了n微妙），因为每个组里面的事务可以在从库并行的去重放，所以设置该参数大于0，有助于提高从库应用日志的速度，减少从库延迟；
设置binlog_group_commit_sync_delay **可以增加从库的并行提交事务数，因此可以增加复制从属服务器上的并行执行能力**。要受益于此效果，从属服务器必须设置slave_parallel_type=LOGICAL_CLOCK，并且在还设置binlog_transaction_dependency_tracking=COMMIT_ORDER时效果更显著。在调整binlog_group_commit_sync_delay的设置时，必须同时考虑主设备的吞吐量和从设备的吞吐量。

2、但是设置binlog_group_commit_sync_delay会增加主服务器上事务的延迟，这可能会影响客户端应用程序。此外，在高度并发的工作负载上，可能会增加争用，从而降低吞吐量，导致数据库性能降低，还能在错误日志中看到很多RECORD LOCK信息。(所以主库请不要设置)

3、当设置sync_binlog=0或sync_binlog=1时，binlog_group_commit_sync_delay指定的延迟将作用于每个事务组提交。当sync_binlog设置为大于1的值n时，该参数的延迟作用于每n个二进制日志提交组提交之间；

建议：该参数设置一定要结合实际情况，评估出mysql的并发量，计算出单位时间内的并发量，然后合理设置binlog_group_commit_sync_delay和binlog_group_commit_sync_no_delay_count（单位时间每组的事务数） ，一定要限制每个组的事务个数，因为如果不设置的话，如果你的实际并发量挺大，这就会导致你的每个组的事务数可能非常多，然后我们知道组提交的commit阶段是分三个步骤的，每个阶段都是有队列的，如果每个组太多事务，就会导致内存队列不够用，而使用临时文件，这样就降低了commit的性能，造成更多的延迟， 所以要使用 binlog_group_commit_sync_no_delay_count 来限制你的每个组的事务数，这样就能尽可能多的把同一个组的事务数增多，但是也不至于太多，限制在一个合理的范围，这些事务可以在从库并发执行，而如果不设置的话，那么这些事务可能有很多是串行的， 也有可能事务太多导致性能降低而产生更多的延迟！






###2：binlog_group_commit_sync_no_delay_count
全局动态变量，单位个数，默认0，范围：0～1000000。
表示等待延迟提交的最大事务数，如果上面参数的时间没到，但事务数到了，则直接同步到磁盘。若没有开启，则该参数也不会开启。


###开始实验
主库创建4个表 test1 test2 test3 test4，分别执行4个存储过程insert1 insert2 insert3 insert4 。且从库开启log_slave_updates=ON；binlog_group_commit_sync_delay=500；binlog_group_commit_sync_no_delay_count=5

记录主库发过来的binlog
~~~
CREATE TABLE `test`.`test1`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5804943 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

CREATE DEFINER=`root`@`%` PROCEDURE `insert1`(in start int(10),in max_num int(10))
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 repeat
 set i=i+1;
 INSERT INTO `test`.`test`(`id`) VALUES (null);
 until i=max_num end repeat;
end
~~~


主从复制完毕后开分析存库binlog
~~~
mysqlbinlog mysql-bin.000004 | findstr last_committed >log.log
~~~
得到结果如下，相同的last_committed 4个一组，说明存在组提交！
~~~
#210224 14:45:54 server id 1  end_log_pos 573196 CRC32 0x6d8370fb 	Anonymous_GTID	last_committed=2323	sequence_number=2324
#210224 14:45:54 server id 1  end_log_pos 573443 CRC32 0xf80ea86b 	Anonymous_GTID	last_committed=2323	sequence_number=2325
#210224 14:45:54 server id 1  end_log_pos 573690 CRC32 0x7e4d65e8 	Anonymous_GTID	last_committed=2323	sequence_number=2326
#210224 14:45:54 server id 1  end_log_pos 573937 CRC32 0xabb23bd6 	Anonymous_GTID	last_committed=2323	sequence_number=2327
#210224 14:45:54 server id 1  end_log_pos 574183 CRC32 0xfd70d3d8 	Anonymous_GTID	last_committed=2327	sequence_number=2328
#210224 14:45:54 server id 1  end_log_pos 574430 CRC32 0xe5e91798 	Anonymous_GTID	last_committed=2327	sequence_number=2329
#210224 14:45:54 server id 1  end_log_pos 574676 CRC32 0xe3e59f18 	Anonymous_GTID	last_committed=2327	sequence_number=2330
#210224 14:45:54 server id 1  end_log_pos 574923 CRC32 0xad21b314 	Anonymous_GTID	last_committed=2327	sequence_number=2331
#210224 14:45:54 server id 1  end_log_pos 575170 CRC32 0xb002f817 	Anonymous_GTID	last_committed=2331	sequence_number=2332
#210224 14:45:54 server id 1  end_log_pos 575417 CRC32 0xbf7ae6a6 	Anonymous_GTID	last_committed=2331	sequence_number=2333
#210224 14:45:54 server id 1  end_log_pos 575664 CRC32 0x028e0ce8 	Anonymous_GTID	last_committed=2331	sequence_number=2334
#210224 14:45:54 server id 1  end_log_pos 575911 CRC32 0x7ab44045 	Anonymous_GTID	last_committed=2331	sequence_number=2335
#210224 14:45:54 server id 1  end_log_pos 576157 CRC32 0xb27baa63 	Anonymous_GTID	last_committed=2335	sequence_number=2336
#210224 14:45:54 server id 1  end_log_pos 576404 CRC32 0x1ce72de5 	Anonymous_GTID	last_committed=2335	sequence_number=2337
#210224 14:45:54 server id 1  end_log_pos 576651 CRC32 0xbc613b8b 	Anonymous_GTID	last_committed=2335	sequence_number=2338
#210224 14:45:54 server id 1  end_log_pos 576897 CRC32 0x542f8969 	Anonymous_GTID	last_committed=2335	sequence_number=2339
#210224 14:45:54 server id 1  end_log_pos 577144 CRC32 0xbb97c194 	Anonymous_GTID	last_committed=2339	sequence_number=2340
~~~


>mysql5.7多线程复制技术就是基于组提交的。但是经过我的实验吗，同步的速度并没有显著的提升啊。
可以试试mysql 丁奇 transfer 工具
