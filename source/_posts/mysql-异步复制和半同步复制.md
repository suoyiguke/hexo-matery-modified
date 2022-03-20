---
title: mysql-异步复制和半同步复制.md
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
title: mysql-异步复制和半同步复制.md
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
在MySQL5.5之前，MySQL 的复制是异步操作，主库和从库的数据之间存在一定的延迟，这样存在一个隐患:当在主库上写入一个事务并提交成功，而从库尚未得到主库推送的Binlog日志时，主库宕机了，例如主库可能因磁盘损坏、内存故障等造成主库上该事务Binlog丢失，此时从库就可能损失这个事务，从而造成主从不一致。
为了解决这个问题, MySQL5.5引人了半同步复制机制。

###异步复制
在MySQL 5.5之前的异步复制时，主库执行完 Commit提交操作后，在主库写入 Binlog日志后即可成功返回客户端，无需等待Binlog日志传送给从库，如图31-7所示。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-d1e748b76c920eb3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>异步复制中主库不会在意从库是否已同步到数据

###半同步复制
而半同步复制时，为了保证主库上的每一个 Binlog 事务都能够被可靠的复制到从库上，主库在每次事务成功提交时，并不及时反馈给前端应用用户，而是等待其中一个从库也接收到 Binlog事务并成功写入中继日志后，主库才返回Commit操作成功给客户端。**半同步复制保证了事务成功提交后，至少有两份日志记录**，一份在主库的 Binlog日志上，另一份在至少一个从库的中继日志Relay Log 上，从而更进一步保证了数据的完整性。半同步复制的大致流程如图31-8所示。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3313e83440c94dbc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

半同步复制模式下，假如在图31-8的步骤1、2、3中的任何一个步骤中主库宕机，则事务并未提交成功，从库上也没有收到事务对应的 Binlog日志，所以主从数据是一致的;
假如在步骤4传送 Binlog日志到从库时，从库宕机或者网络故障，导致 Binlog并没有及时地传送到从库上，此时主库上的事务会等待一段时间(时间长短由参数rpl_semi_sync_master_timeout设置的毫秒数决定)，如果 Binlog 在这段时间内都无法成功推送到从库上，则 MySQL自动调整复制为异步模式，事务正常返回提交结果给客户端。

半同步复制很大程度上取决于主从库之间的网络情况，往返时延RTT 越小决定了从库的实时性越好。通俗地说，主从库之间网络越快，从库越实时。
>注意:往返时延RTT ( Round-Trip Time)在计算机网络中是一个重要的性能指标，它表示从发送端发送数据开始到发送端接收到接收端的确认，总共经历的时长。


>半同步复制保证至少有一个从机同步到了主库数据


####mysql配置实现半同步复制
半同步模式是作为MySQL5.5的一个插件来实现的，主库和从库使用不同的插件。安装比较简单，在上一小节异步复制的环境上，安装半同步复制插件即可。

1、首先,判断MySQL服务器是否支持动态增加插件:
~~~
mysql> SELECT @@have_dynamic_loading;
+------------------------+
| @@have_dynamic_loading |
+------------------------+
| YES                    |
+------------------------+
1 row in set (0.01 sec)
~~~
2、安装插件
~~~
 INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.dll'; --主
 INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.dll'; -- 从
~~~

3、可以查看到已安装的插件
~~~
mysql> 	SELECT * from mysql.plugin;
+----------------------+---------------------+
| name                 | dl                  |
+----------------------+---------------------+
| rpl_semi_sync_master | semisync_master.dll |
| rpl_semi_sync_slave  | semisync_slave.dll  |
+----------------------+---------------------+
2 rows in set (0.01 sec)

~~~

4、在安装完插件后，半同步复制默认是关闭的，这时需设置参数来开启半同步
主：
~~~
mysql> SET GLOBAL rpl_semi_sync_master_enabled = 1;
~~~
从：
~~~
mysql> SET GLOBAL rpl_semi_sync_slave_enabled = 1;
~~~

以上的启动方式是在命令行操作，也可写在配置文件中。
主：

~~~
plugin-load=rpl_semi_sync_master=semisync_master.so
rpl_semi_sync_master_enabled=1
~~~
从：
~~~
plugin-load=rpl_semi_sync_slave=semisync_slave.so
rpl_semi_sync_slave_enabled=1
~~~

4、重启从上的IO线程
从：
~~~
mysql> STOP SLAVE IO_THREAD; START SLAVE IO_THREAD;
Query OK, 0 rows affected (0.06 sec)
Query OK, 0 rows affected (0.00 sec)
~~~
如果没有重启，则默认还是异步复制，重启后，slave会在master上注册为半同步复制的slave角色。这时候，主的error.log中会打印如下信息：

> 2016-08-05T10:03:40.104327Z 5 [Note] While initializing dump thread for slave with UUID , found a zombie dump thread with the same UUID. Master is killing the zombie dump thread(4). 2016-08-05T10:03:40.111175Z 4 [Note] Stop asynchronous binlog_dump to slave (server_id: 2) 2016-08-05T10:03:40.119037Z 5 [Note] Start binlog_dump to master_thread_id(5) slave_server(2), pos(mysql-bin.000003, 621) 2016-08-05T10:03:40.119099Z 5 [Note] Start semi-sync binlog_dump to slave (server_id: 2), pos(mysql-bin.000003, 621)

查看半同步是否在运行

主：
~~~
mysql> show status like 'Rpl_semi_sync_master_status';

+-----------------------------+-------+
| Variable_name               | Value |
+-----------------------------+-------+
| Rpl_semi_sync_master_status | ON    |
+-----------------------------+-------+
1 row in set (0.00 sec)
~~~

从：
~~~
mysql> show status like 'Rpl_semi_sync_slave_status';
+----------------------------+-------+
| Variable_name              | Value |
+----------------------------+-------+
| Rpl_semi_sync_slave_status | ON    |
+----------------------------+-------+
1 row in set (0.20 sec)
~~~
这两个变量常用来监控主从是否运行在半同步复制模式下。至此，MySQL半同步复制搭建完毕~

###分析设置参数
~~~
mysql> SHOW VARIABLES LIKE '%rpl%';
+-------------------------------------------+------------+
| Variable_name                             | Value      |
+-------------------------------------------+------------+
| rpl_semi_sync_master_enabled              | ON    半同步复制功能开关     |
| rpl_semi_sync_master_timeout              | 10000（毫秒）  从库反馈响应主库时的超时时间，超过这段时间（10秒）就会降级为异步复制，主库在timeout时间结束之后就会返回信息给客户端    |
| rpl_semi_sync_master_trace_level          | 32         |
| rpl_semi_sync_master_wait_for_slave_count | 1          |
| rpl_semi_sync_master_wait_no_slave        | ON         |
| rpl_semi_sync_master_wait_point           | AFTER_SYNC |
| rpl_semi_sync_slave_enabled               | OFF        |
| rpl_semi_sync_slave_trace_level           | 32         |
| rpl_stop_slave_timeout                    | 31536000   |
+-------------------------------------------+------------+
9 rows in set (0.01 sec)

~~~



###着重分析下半同步有关状态参数

~~~
mysql> show status like '%semi_sync%';
+--------------------------------------------+-------+
| Variable_name                              | Value |
+--------------------------------------------+-------+
| Rpl_semi_sync_master_clients               | 1     |
| Rpl_semi_sync_master_net_avg_wait_time     | 0     |
| Rpl_semi_sync_master_net_wait_time         | 0     |
| Rpl_semi_sync_master_net_waits             | 0     |
| Rpl_semi_sync_master_no_times              | 0     |
| Rpl_semi_sync_master_no_tx                 | 0   当前不是半同步复制下从库反馈的事件数（这个值大说明从库到主库之间可能网络有问题）  |
| Rpl_semi_sync_master_status                | ON   半同步复制开启状态 |
| Rpl_semi_sync_master_timefunc_failures     | 0     |
| Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
| Rpl_semi_sync_master_tx_wait_time          | 0     |
| Rpl_semi_sync_master_tx_waits              | 0     |
| Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
| Rpl_semi_sync_master_wait_sessions         | 0     |
| Rpl_semi_sync_master_yes_tx                | 0  主库在半同步复制下得到从库的响应的事件数   |
| Rpl_semi_sync_slave_status                 | OFF   |
+--------------------------------------------+-------+
15 rows in set (0.02 sec)
~~~


**来做个实验，观察半同步状态参数的变化。**

1、在主库上insert一条记录，观察下变化；
~~~
mysql> INSERT INTO `test`.`test`(`id`) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> show status like '%semi_sync%';
+--------------------------------------------+-------+
| Variable_name                              | Value |
+--------------------------------------------+-------+
| Rpl_semi_sync_master_clients               | 1     |
| Rpl_semi_sync_master_net_avg_wait_time     | 0     |
| Rpl_semi_sync_master_net_wait_time         | 0     |
| Rpl_semi_sync_master_net_waits             | 1     |
| Rpl_semi_sync_master_no_times              | 0     |
| Rpl_semi_sync_master_no_tx                 | 0     |
| Rpl_semi_sync_master_status                | ON    |
| Rpl_semi_sync_master_timefunc_failures     | 0     |
| Rpl_semi_sync_master_tx_avg_wait_time      | 995   |
| Rpl_semi_sync_master_tx_wait_time          | 995   |
| Rpl_semi_sync_master_tx_waits              | 1     |
| Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
| Rpl_semi_sync_master_wait_sessions         | 0     |
| Rpl_semi_sync_master_yes_tx                | 1     |
| Rpl_semi_sync_slave_status                 | OFF   |
+--------------------------------------------+-------+
15 rows in set (0.01 sec)
~~~
 Rpl_semi_sync_master_net_waits加1，说明刚才的insert已经发送到从机并且主机还接收到从机的反馈响应；

2、我们将从机mysql停止，再次在主机上进行insert后查看状态
~~~

mysql> INSERT INTO `test`.`test`(`id`) VALUES (NULL);
Query OK, 1 row affected (10.00 sec)

mysql> show status like '%semi_sync%';
+--------------------------------------------+-------+
| Variable_name                              | Value |
+--------------------------------------------+-------+
| Rpl_semi_sync_master_clients               | 0     |
| Rpl_semi_sync_master_net_avg_wait_time     | 0     |
| Rpl_semi_sync_master_net_wait_time         | 0     |
| Rpl_semi_sync_master_net_waits             | 2     |
| Rpl_semi_sync_master_no_times              | 1     |
| Rpl_semi_sync_master_no_tx                 | 1     |
| Rpl_semi_sync_master_status                | OFF   |
| Rpl_semi_sync_master_timefunc_failures     | 0     |
| Rpl_semi_sync_master_tx_avg_wait_time      | 497   |
| Rpl_semi_sync_master_tx_wait_time          | 995   |
| Rpl_semi_sync_master_tx_waits              | 2     |
| Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
| Rpl_semi_sync_master_wait_sessions         | 0     |
| Rpl_semi_sync_master_yes_tx                | 2     |
| Rpl_semi_sync_slave_status                 | OFF   |
+--------------------------------------------+-------+
15 rows in set (0.02 sec)

mysql> INSERT INTO `test`.`test`(`id`) VALUES (NULL);
Query OK, 1 row affected (0.00 sec)

mysql> show status like '%semi_sync%';
+--------------------------------------------+-------+
| Variable_name                              | Value |
+--------------------------------------------+-------+
| Rpl_semi_sync_master_clients               | 0     |
| Rpl_semi_sync_master_net_avg_wait_time     | 0     |
| Rpl_semi_sync_master_net_wait_time         | 0     |
| Rpl_semi_sync_master_net_waits             | 2     |
| Rpl_semi_sync_master_no_times              | 1     |
| Rpl_semi_sync_master_no_tx                 | 2     |
| Rpl_semi_sync_master_status                | OFF   |
| Rpl_semi_sync_master_timefunc_failures     | 0     |
| Rpl_semi_sync_master_tx_avg_wait_time      | 497   |
| Rpl_semi_sync_master_tx_wait_time          | 995   |
| Rpl_semi_sync_master_tx_waits              | 2     |
| Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
| Rpl_semi_sync_master_wait_sessions         | 0     |
| Rpl_semi_sync_master_yes_tx                | 2     |
| Rpl_semi_sync_slave_status                 | OFF   |
+--------------------------------------------+-------+
15 rows in set (0.03 sec)

~~~

可以看到，主机进行insert阻塞了10秒才返回结果。Rpl_semi_sync_master_status变为OFF，Rpl_semi_sync_master_no_tx加1，说明这条insert没有同步到从机。后面再一次执行了insert立马返回了结果，说明此时已经降级为异步复制；Rpl_semi_sync_master_no_tx也是增加了1；

3、现在恢复启动从机，再次在主机上进行insert后查看状态
~~~

mysql> INSERT INTO `test`.`test`(`id`) VALUES (NULL);
Query OK, 1 row affected (0.00 sec)

mysql> show status like '%semi_sync%';
+--------------------------------------------+-------+
| Variable_name                              | Value |
+--------------------------------------------+-------+
| Rpl_semi_sync_master_clients               | 0     |
| Rpl_semi_sync_master_net_avg_wait_time     | 0     |
| Rpl_semi_sync_master_net_wait_time         | 0     |
| Rpl_semi_sync_master_net_waits             | 2     |
| Rpl_semi_sync_master_no_times              | 1     |
| Rpl_semi_sync_master_no_tx                 | 3     |
| Rpl_semi_sync_master_status                | OFF   |
| Rpl_semi_sync_master_timefunc_failures     | 0     |
| Rpl_semi_sync_master_tx_avg_wait_time      | 497   |
| Rpl_semi_sync_master_tx_wait_time          | 995   |
| Rpl_semi_sync_master_tx_waits              | 2     |
| Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
| Rpl_semi_sync_master_wait_sessions         | 0     |
| Rpl_semi_sync_master_yes_tx                | 2     |
| Rpl_semi_sync_slave_status                 | OFF   |
+--------------------------------------------+-------+
15 rows in set (0.03 sec)
~~~


Rpl_semi_sync_master_status还是OFF，Rpl_semi_sync_master_no_tx又增加了1。说明从库重启并不会自动恢复为原来的半同步复制，需要手动操作：
主 SET GLOBAL rpl_semi_sync_master_enabled = 1;
从 SET GLOBAL rpl_semi_sync_slave_enabled = 1; STOP SLAVE IO_THREAD; START SLAVE IO_THREAD;

上面是从机重启后的变化，那么主到从之间的网络问题呢，我们可以利用防火墙来模拟。


###全同步复制

对于全同步复制，当主库提交事务之后，所有的从库节点必须收到，APPLY并且提交这些事务，然后主库线程才能继续做后续操作。这里面有一个很明显的缺点就是，主库完成一个事务的时间被拉长，性能降低。

>全同步复制下主库会等待所有从库均同步完数据
