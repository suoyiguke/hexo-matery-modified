---
title: mysql-之-metadata-lock-元数据锁.md
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
title: mysql-之-metadata-lock-元数据锁.md
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
在进行 DDL 操作时，有时会出现Waiting for table metadata lock的等待场景。而且，一旦alter table TableA的操作停滞在Waiting for table metadata lock的状态，后续对TableA的任何操作（包括读）都无法进行，都会在Opening tables的阶段进入Waiting for table metadata lock的队列。如果是产品环境的核心表出现了这样的锁等待队列，就会造成灾难性的后果。

**为嘛需要 metadata lock(MDL)?**

保护一个处于事务中的表的结构不被修改。


**什么时候会出现 metadata lock呢？**

发出DDL操作是引发 metadata lock  的直接原因，很容易就能知道是因为DDL而造成的。但是而根本原因还是另有其它，只有存在以下三种情况之后再发出DDL才会引起 metadata lock 锁等待问题：

1、有长时间运行的DML语句

通过show processlist可以看到TableA上有正在进行的操作（包括读），此时若发出DDL的 alter table语句将无法获取到metadata 独占锁，会进行等待。 metadata lock  并不会因为 mysql 5.6中的online ddl机制而不出。一般alter table的操作过程中（见下图），在after create步骤会获取metadata 独占锁，当进行到altering table的过程时（通常是最花时间的步骤），对该表的读写都可以正常进行，这就是online ddl的表现，并不会像之前在整个alter table过程中阻塞写入。（当然，也并不是所有类型的alter操作都能online的，具体可以参见官方手册：[http://dev.mysql.com/doc/refman/5.6/en/innodb-create-index-overview.html](http://dev.mysql.com/doc/refman/5.6/en/innodb-create-index-overview.html)）

![image](https://upload-images.jianshu.io/upload_images/13965490-d646f1d2e13322bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、有未提交的事务

通过show processlist看不到TableA上有任何操作，但实际上存在有`未提交的事务`，可以在information_schema.innodb_trx中查看到。在事务没有完成之前，TableA上的锁不会释放，alter table 同样获取不到metadata的独占锁。


3、在执行期间失败的语句，不会立即释放metadata lock

通过show processlist看不到TableA上有任何操作，在information_schema.innodb_trx中也没有任何进行中的事务。这很可能是因为在一个显式的事务中，对TableA进行了一个失败的操作（比如查询了一个不存在的字段），这时事务没有开始，但是失败语句获取到的锁依然有效。从performance_schema.events_statements_current 表中可以查到失败的语句。

官方手册上对此的说明如下：
>If the server acquires metadata locks for a statement that is syntactically valid but fails during execution, it does not release the locks early. Lock release is still deferred to the end of the transaction because the failed statement is written to the binary log and the locks protect log consistency.
也就是说除了语法错误，其他错误语句获取到的锁在这个事务提交或回滚之前，仍然不会释放掉。because the failed statement is written to the binary log and the locks protect log consistency 但是解释这一行为的原因很难理解，因为错误的语句根本不会被记录到二进制日志。

总之，alter table（DDL） 的语句是很危险的，在操作之前最好确认对要操作的表没有任何进行中的操作、没有未提交事务、也没有显式事务中的报错语句。如果有alter table的维护任务，在无人监管的时候运行，最好通过lock_wait_timeout设置好超时时间，避免长时间的metedata锁等待。


**验证产生metadata lock的情况**
情景一、长时间执行语句+DDL+DML 
sessionA这边先执行一个大事务，循环做insert操作。将循环次数设置足够大。
sessionB执行DDL，阻塞；
sessionC执行简单查询，阻塞；
sessionD执行 SHOW PROCESSLIST；

即可查到
~~~
mysql> show PROCESSLIST;
+-----+------+-----------------+------+---------+------+---------------------------------+------------------------------------------------------------------------+
| Id  | User | Host            | db   | Command | Time | State                           | Info                                                                   |
+-----+------+-----------------+------+---------+------+---------------------------------+------------------------------------------------------------------------+
| 539 | root | localhost:65496 | test | Sleep   |  611 |                                 | NULL                                                                   |
| 540 | root | localhost:65497 | test | Sleep   |  611 |                                 | NULL                                                                   |
| 542 | root | localhost:65498 | test | Sleep   |  378 |                                 | NULL                                                                   |
| 543 | root | localhost:51872 | test | Sleep   | 9080 |                                 | NULL                                                                   |
| 544 | root | localhost:52221 | NULL | Sleep   | 8420 |                                 | NULL                                                                   |
| 545 | root | localhost:52973 | test | Sleep   |   69 |                                 | NULL                                                                   |
| 547 | root | localhost:53454 | test | Sleep   | 6451 |                                 | NULL                                                                   |
| 548 | root | %:56603         | test | Query   |    0 | update                          | INSERT INTO `test`.`test`(`id`) VALUES (null)                          |
| 550 | root | localhost:56805 | test | Query   |    0 | starting                        | show PROCESSLIST                                                       |
| 552 | root | localhost:56815 | test | Query   |   13 | Waiting for table metadata lock | SELECT * FROM `test`.`test` LIMIT 0, 1000                              |
| 553 | root | localhost:56827 | test | Query   |   48 | Waiting for table metadata lock | ALTER TABLE `test`.`test`
ADD COLUMN `dd` varchar(255) NULL AFTER `id` |
+-----+------+-----------------+------+---------+------+---------------------------------+------------------------------------------------------------------------+
11 rows in set (0.03 sec)
~~~
kill 553 
情景二、DML未提交+DDL+DML 

sessionA 先开启事务做 begin;select * from test;查询，sessionB 后 进行 truncate test;
sessionC中查询下test 表阻塞;sessionD中查询下show PROCESSLIST；可以发现sessionA中没有提交事务直接导致后面的sessionB的DDL语句产生 metadata lock，跟着sessionC的普通查询也是产生了 metadata lock。

~~~
mysql> show PROCESSLIST;
+-----+------+-----------------+------+---------+-------+---------------------------------+--------------------+
| Id  | User | Host            | db   | Command | Time  | State                           | Info               |
+-----+------+-----------------+------+---------+-------+---------------------------------+--------------------+
| 241 | root | localhost:65128 | iam  | Sleep   | 14387 |                                 | NULL               |
| 242 | root | localhost:65129 | iam  | Sleep   | 14387 |                                 | NULL               |
| 243 | root | localhost:65130 | iam  | Sleep   | 14387 |                                 | NULL               |
| 244 | root | localhost:65131 | iam  | Sleep   | 14387 |                                 | NULL               |
| 245 | root | localhost:65132 | iam  | Sleep   | 14387 |                                 | NULL               |
| 246 | root | localhost:65133 | iam  | Sleep   | 14387 |                                 | NULL               |
| 247 | root | localhost:65134 | iam  | Sleep   | 14387 |                                 | NULL               |
| 248 | root | localhost:65135 | iam  | Sleep   | 14387 |                                 | NULL               |
| 249 | root | localhost:65136 | iam  | Sleep   | 14387 |                                 | NULL               |
| 250 | root | localhost:65137 | iam  | Sleep   | 13391 |                                 | NULL               |
| 253 | root | localhost:65443 | test | Sleep   |   367 |                                 | NULL               |
| 255 | root | localhost:50340 | test | Query   |    68 | Waiting for table metadata lock | select * from test |
| 263 | root | localhost:53394 | test | Sleep   |   157 |                                 | NULL               |
| 265 | root | localhost:61229 | test | Query   |   359 | Waiting for table metadata lock | truncate test      |
| 266 | root | localhost:61566 | test | Query   |     0 | starting                        | show PROCESSLIST   |
+-----+------+-----------------+------+---------+-------+---------------------------------+--------------------+
15 rows in set (0.03 sec)
~~~


我们可以通过下面查询得到没有commit的线程id然后kill之；得到的tread_id是253 ；kill 253 即可解决这个metadata lock问题。注意这个语句查询得到的SQL_TEXT不是引发阻塞的语句而是事务最后一次执行的查询。若想得到事务的所有的执行语句可以通过全日志或者binlog来实现。


~~~
mysql> SELECT
    a.SQL_TEXT,
    c.id,
    d.trx_started
FROM
      performance_schema.events_statements_current   a
JOIN performance_schema.threads b ON a.THREAD_ID = b.THREAD_ID
JOIN information_schema.PROCESSLIST c ON b.PROCESSLIST_ID = c.id
JOIN information_schema.innodb_trx d ON c.id = d.trx_mysql_thread_id
ORDER BY
    d.trx_started;
+--------------------+-----+---------------------+
| SQL_TEXT           | id  | trx_started         |
+--------------------+-----+---------------------+
| select * from test | 253 | 2021-02-03 14:19:50 |
+--------------------+-----+---------------------+
1 row in set (0.02 sec)

~~~
>注意若选择kill掉未commit的事务连接则事务会进行回滚需要酌情处理；当然也可以选择kill掉那条DDL查询



情景三、失败的语句+DDL+DML

sessionA 先执行 BEGIN ; SELECT aaa from test; -- aaa字段并不存在
sessionB 后 进行 truncate test;
sessionC中insert 下 test 表添加记录阻塞;
sessionD中查询下show PROCESSLIST；可以发现sessionB的DDL语句产生 metadata lock，跟着sessionC的普通insert 也是产生了 metadata lock。

~~~
mysql> show PROCESSLIST;
+-----+------+-----------------+------+---------+------+---------------------------------+------------------------------------------------------------------------+
| Id  | User | Host            | db   | Command | Time | State                           | Info                                                                   |
+-----+------+-----------------+------+---------+------+---------------------------------+------------------------------------------------------------------------+
| 538 | root | localhost:65494 | test | Sleep   |  273 |                                 | NULL                                                                   |
| 539 | root | localhost:65496 | test | Sleep   |   13 |                                 | NULL                                                                   |
| 540 | root | localhost:65497 | test | Query   |   27 | Waiting for table metadata lock | INSERT INTO `test`.`test`(`id`) VALUES (1)                             |
| 541 | root | localhost:65495 | test | Query   |  230 | Waiting for table metadata lock | ALTER TABLE `test`.`test`
ADD COLUMN `dd` varchar(255) NULL AFTER `id` |
| 542 | root | localhost:65498 | test | Query   |    0 | starting                        | show PROCESSLIST                                                       |
+-----+------+-----------------+------+---------+------+---------------------------------+------------------------------------------------------------------------+
5 rows in set (0.03 sec)

~~~

sessionD再次查询下，可以看到这条语句
~~~
mysql> 
SELECT
	b.conn_id,
	a.* 
FROM
	PERFORMANCE_SCHEMA.events_statements_current a,
	sys.SESSION b 
WHERE
	a.THREAD_ID = b.thd_id;
+---------+-----------+----------+--------------+------------------------+-------------------------+---------------------+---------------------+-----------------+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-------------+---------------+-------------+-----------------------+-------------+-------------------+--------------------------------------+--------+----------+---------------+-----------+---------------+-------------------------+--------------------+------------------+------------------------+--------------+--------------------+-------------+-------------------+------------+-----------+-----------+---------------+--------------------+------------------+--------------------+---------------------+
| conn_id | THREAD_ID | EVENT_ID | END_EVENT_ID | EVENT_NAME             | SOURCE                  | TIMER_START         | TIMER_END           | TIMER_WAIT      | LOCK_TIME | SQL_TEXT                                                                                                                                                                                                              | DIGEST                           | DIGEST_TEXT                                                                                                                                                                                                                                                        | CURRENT_SCHEMA | OBJECT_TYPE | OBJECT_SCHEMA | OBJECT_NAME | OBJECT_INSTANCE_BEGIN | MYSQL_ERRNO | RETURNED_SQLSTATE | MESSAGE_TEXT                         | ERRORS | WARNINGS | ROWS_AFFECTED | ROWS_SENT | ROWS_EXAMINED | CREATED_TMP_DISK_TABLES | CREATED_TMP_TABLES | SELECT_FULL_JOIN | SELECT_FULL_RANGE_JOIN | SELECT_RANGE | SELECT_RANGE_CHECK | SELECT_SCAN | SORT_MERGE_PASSES | SORT_RANGE | SORT_ROWS | SORT_SCAN | NO_INDEX_USED | NO_GOOD_INDEX_USED | NESTING_EVENT_ID | NESTING_EVENT_TYPE | NESTING_EVENT_LEVEL |
+---------+-----------+----------+--------------+------------------------+-------------------------+---------------------+---------------------+-----------------+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------+-------------+---------------+-------------+-----------------------+-------------+-------------------+--------------------------------------+--------+----------+---------------+-----------+---------------+-------------------------+--------------------+------------------+------------------------+--------------+--------------------+-------------+-------------------+------------+-----------+-----------+---------------+--------------------+------------------+--------------------+---------------------+
|     546 |       571 |        7 |            7 | statement/sql/select   | socket_connection.cc:98 | 1475385714148700000 | 1475385717607700000 |      3459000000 |         0 | SELECT aaa from test                                                                                                                                                                                                  | e1f30f66bc41e9be78a5db607512bcd7 | SELECT `aaa` FROM `test`                                                                                                                                                                                                                                           | test           | NULL        | NULL          | NULL        | NULL                  |        1054 | 42S22             | Unknown column 'aaa' in 'field list' |      1 |        0 |             0 |         0 |             0 |                       0 |                  0 |                0 |                      0 |            0 |                  0 |           0 |                 0 |          0 |         0 |         0 |             0 |                  0 | NULL             | NULL               |                   0 |

~~~

kill 546 杀死出错执行语句的连接即可从阻塞中恢复
