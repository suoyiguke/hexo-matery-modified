---
title: mysql-并行复制技术-Enhanced-Multi-Threaded-Slave(MTS).md
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
title: mysql-并行复制技术-Enhanced-Multi-Threaded-Slave(MTS).md
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
MySQL从5.6开始有了SQL Thread多个的概念，可以并发还原数据，即并行复制技术。只可惜5.6的并行复制技术只能基于schema库层面，而多数场景下我们都是使用一库多表的形式。所以就显得比较鸡肋了。
　
不过在MySQL 5.7中，引入了基于组提交的并行复制（Enhanced Multi-threaded Slaves），设置参数slave_parallel_workers>0并且global.slave_parallel_type＝‘LOGICAL_CLOCK’，即可支持一个schema下，slave_parallel_workers个的worker线程并发执行relay log中主库提交的事务。


###MySQL5.7并行复制原理：
基于组复制（group commit）实现

###如何知道事务是否在同一组中？
在MySQL 5.7版本中，其设计方式是将组提交的信息存放在GTID中。那么如果用户没有开启GTID功能，即：将参数gtid_mode设置为OFF呢？
MySQL 5.7引入了称之为Anonymous_Gtid（ANONYMOUS_GTID_LOG_EVENT）的二进制日志event类型，组提交信息存放在 Anonymous_Gtid 中。


当开启GTID时，每一个操作语句（DML/DDL）执行前就会添加一个GTID事件，记录当前全局事务ID；同时在MySQL 5.7版本中，组提交信息也存放在GTID事件中，有两个关键字段last_committed，sequence_number就是用来标识组提交信息的。在InnoDB中有一个全局计数器（global counter），在每一次存储引擎提交之前，计数器值就会增加。在事务进入prepare阶段之前，全局计数器的当前值会被储存在事务中，这个值称为此事务的commit-parent（也就是last_committed）。last_committed表示事务提交的时候，上次事务提交的编号，如果事务具有相同的last_committed，表示这些事务都在一组内，可以进行并行的回放。而sequence_number是顺序增长的，每个事务对应一个序列号。

这意味着在MySQL 5.7版本中即使不开启GTID，每个事务开始前也是会存在一个Anonymous_Gtid，而这个Anonymous_Gtid事件中就存在着组提交的信息。反之，如果开启了GTID后，就不会存在这个Anonymous_Gtid了，从而组提交信息就记录在非匿名GTID事件中。



###MySQL如何将这些事务进行分组的？
一个组提交的事务都是可以并行回放，因为这些事务都已进入到事务的prepare阶段，则说明事务之间没有任何冲突（否则就不可能提交） 

其核心思想：一个组提交的事务都是可以并行回放（配合binary log group commit）；slave机器的relay log中 last_committed相同的事务（sequence_num不同）可以并发执行。
具体配置如下：
其中，变量slave-parallel-type可以有两个值：DATABASE 默认值，基于库的并行复制方式；LOGICAL_CLOCK：基于组提交的并行复制方式
MySQL 5.7开启Enhanced Multi-Threaded Slave配置：

~~~
# slave
slave-parallel-type=LOGICAL_CLOCK
slave-parallel-workers=16
slave_pending_jobs_size_max = 2147483648
slave_preserve_commit_order=1
master_info_repository=TABLE
relay_log_info_repository=TABLE
relay_log_recovery=ON
~~~
至此，MySQL彻底解决了复制延迟问题；可以看到下面出现了16个Waiting for an event from Coordinator状态的线程；
~~~
mysql> show processlist;
+----+-------------+-----------------+------+---------+------+--------------------------------------------------------+------------------+
| Id | User        | Host            | db   | Command | Time | State                                                  | Info             |
+----+-------------+-----------------+------+---------+------+--------------------------------------------------------+------------------+
|  1 | system user |                 | NULL | Connect |  929 | Waiting for master to send event                       | NULL             |
|  2 | system user |                 | NULL | Connect |   54 | Slave has read all relay log; waiting for more updates | NULL             |
|  3 | system user |                 | NULL | Connect |  728 | Waiting for an event from Coordinator                  | NULL             |
|  4 | system user |                 | NULL | Connect |  733 | Waiting for an event from Coordinator                  | NULL             |
|  5 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
|  6 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
|  7 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
|  8 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
|  9 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 10 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 11 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 12 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 13 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 14 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 15 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 16 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 17 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 18 | system user |                 | NULL | Connect |  929 | Waiting for an event from Coordinator                  | NULL             |
| 20 | root        | localhost:58055 | NULL | Sleep   |  826 |                                                        | NULL             |
| 21 | root        | localhost:58081 | NULL | Query   |    0 | starting                                               | show processlist |
| 22 | root        | localhost:58082 | test | Sleep   |    2 |                                                        | NULL             |
| 23 | root        | localhost:58085 | NULL | Sleep   |  667 |                                                        | NULL             |
| 24 | root        | localhost:58084 | NULL | Sleep   |   20 |                                                        | NULL             |
| 25 | root        | localhost:58086 | NULL | Sleep   |  667 |                                                        | NULL             |
+----+-------------+-----------------+------+---------+------+--------------------------------------------------------+------------------+
~~~



###MySQL5.7应用事务顺序和realy log记录事务顺序不一样的问题：
MySQL 5.7后的MTS可以实现更小粒度的并行复制，但需要将slave_parallel_type设置为LOGICAL_CLOCK，但仅仅设置为LOGICAL_CLOCK也会存在问题，因为此时在slave上应用事务的顺序是无序的，和relay log中记录的事务顺序不一样，这样数据一致性是无法保证的，为了保证事务是按照relay log中记录的顺序来回放，就需要开启参数slave_preserve_commit_order=1


###master_info_repository请设置为TABLE
开启MTS功能后，务必将参数master_info_repostitory设置为TABLE，这样性能可以有50%~80%的提升。这是因为并行复制开启后对于元master.info这个文件的更新将会大幅提升，资源的竞争也会变大。

####slave_parallel_workers

若将slave_parallel_workers设置为0，则MySQL 5.7退化为原单线程复制，但将slave_parallel_workers设置为1，则SQL线程功能转化为coordinator线程，但是只有1个worker线程进行回放，也是单线程复制。然而，这两种性能却又有一些的区别，因为多了一次coordinator线程的转发，因此slave_parallel_workers=1的性能反而比0还要差，测试下还有20%左右的性能下降

MySQL 5.7新特性：并行复制原理（MTS）

这里其中引入了另一个问题，如果主机上的负载不大，那么组提交的效率就不高，很有可能发生每组提交的事务数量仅有1个，那么在从机的回放时，虽然开启了并行复制，但会出现性能反而比原先的单线程还要差的现象，即延迟反而增大了。聪明的小伙伴们，有想过对这个进行优化吗？

###slave_preserve_commit_order

MySQL 5.7后的MTS可以实现更小粒度的并行复制，但需要将slave_parallel_type设置为LOGICAL_CLOCK，但仅仅设置为LOGICAL_CLOCK也会存在问题，因为此时在slave上应用事务的顺序是无序的，和relay log中记录的事务顺序不一样，这样数据一致性是无法保证的，为了保证事务是按照relay log中记录的顺序来回放，就需要开启参数slave_preserve_commit_order。开启该参数后，执行线程将一直等待, 直到提交之前所有的事务。当从线程正在等待其他工作人员提交其事务时, 它报告其状态为等待前面的事务提交。所以虽然MySQL 5.7添加MTS后，虽然slave可以并行应用relay log，但commit部分仍然是顺序提交，其中可能会有等待的情况。

当开启slave_preserve_commit_order参数后，slave_parallel_type只能是LOGICAL_CLOCK，如果你有使用级联复制，那LOGICAL_CLOCK可能会使离master越远的slave并行性越差。

但是经过测试，这个参数在MySQL 5.7.18中设置之后，也无法保证slave上事务提交的顺序与relay log一致。 在MySQL 5.7.19设置后，slave上事务的提交顺序与relay log中一致（所以生产要想使用MTS特性，版本大于等于MySQL 5.7.19才是安全的）。

 

 
###查询从机MTS的并行程度
那么怎样知道从机MTS的并行程度又是一个难度不小。简单的一种方法（姜总给出的），可以使用performance_schema库来观察，比如下面这条SQL可以统计每个Worker Thread执行的事务数量，在此基础上再做一个聚合分析就可得出每个MTS的并行度:

~~~
SELECT
	thread_id,
	count_star 
FROM
	PERFORMANCE_SCHEMA.events_transactions_summary_by_thread_by_event_name 
WHERE
	thread_id IN ( SELECT thread_id FROM PERFORMANCE_SCHEMA.replication_applier_status_by_worker );
~~~

如果线程并行度太高，不够平均，其实并行效果并不会好，可以试着优化。这种场景下，可以通过调整主服务器上的参数binlog_group_commit_sync_delay、binlog_group_commit_sync_no_delay_count。前者表示延迟多少时间提交事务，后者表示组提交事务凑齐多少个事务再一起提交。总体来说，都是为了增加主服务器组提交的事务比例，从而增大从机MTS的并行度。

虽然MySQL 5.7推出的Enhanced Multi-Threaded Slave在一定程度上解决了困扰MySQL长达数十年的复制延迟问题。然而，目前MTS机制基于组提交实现，简单来说在主上是怎样并行执行的，从服务器上就怎么回放。这里存在一个可能，即若主服务器的并行度不够，则从机的并行机制效果就会大打折扣。MySQL 8.0最新的基于writeset的MTS才是最终的解决之道。即两个事务，只要更新的记录没有重叠（overlap），则在从机上就可并行执行，无需在一个组，即使主服务器单线程执行，从服务器依然可以并行回放。相信这是最完美的解决之道，MTS的最终形态。
>最后，如果MySQL 5.7要使用MTS功能，必须使用最新版本，最少升级到5.7.19版本，修复了很多Bug。



###MySQL5.7在线开启并行复制（多线程复制）：

 在Slave服务器上停止所有链路的复制 

stop slave
set global slave-parallel-type=LOGICAL_CLOCK
set global slave-parallel-workers=16
start slave
show processlist（看到16个SQL线程）  


###其他的解决主从同步延迟问题的方法
mysql 丁奇 transfer 
