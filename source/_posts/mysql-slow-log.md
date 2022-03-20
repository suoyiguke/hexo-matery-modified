---
title: mysql-slow-log.md
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
title: mysql-slow-log.md
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
https://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html

slow log是工作中最重要的日志了。mysql启动不了看error log，查询慢就看slow log。

查看slow log 配置
~~~
(root@localhost) [(none)]>show variables like '%slow%';
+---------------------------+----------------+
| Variable_name             | Value          |
+---------------------------+----------------+
| log_slow_admin_statements | ON             |
| log_slow_slave_statements | ON             |
| slow_launch_time          | 2              |
| slow_query_log            | ON             |
| slow_query_log_file       | mysql-slow.log |
+---------------------------+----------------+

~~~

online设置slow log
~~~
set global slow_query_log =ON;
set global slow_query_log_file= 'mysql-slow.log';
set global long_query_time= 2;
set session long_query_time= 2;
~~~


注意long_query_time变量是global/session 级别的。就是说online设置完毕后原来已经存在的连接的session级别long_query_time变量的值还是老值。会碰到明明修改了却不生效的问题。
对比下官网文档的long_query_time和slow_query_log：
~~~
long_query_time
Command-Line Format	--long-query-time=#
System Variable	long_query_time
Scope	Global, Session
Dynamic	Yes
SET_VAR Hint Applies	No
Type	Numeric
Default Value	10
Minimum Value	0
~~~


~~~
slow_query_log
Command-Line Format	--slow-query-log[={OFF|ON}]
System Variable	slow_query_log
Scope	Global
Dynamic	Yes
SET_VAR Hint Applies	No
Type	Boolean
Default Value	OFF
~~~
可见long_query_time的Scope= Global, Session，全局和会话级别；slow_query_log的Scop=Global只是全局级别;我们需要close掉老连接，这样新打开一个连接就是新long_query_time值了。
对于当前连接我们还可以这样，同时设置session 和global 的值，防止出现当前连接不生效。
~~~
(root@localhost) [mysql]>set session long_query_time= 2;
Query OK, 0 rows affected (0.00 sec)
(root@localhost) [mysql]>set global long_query_time= 2;
Query OK, 0 rows affected (0.00 sec)
~~~




###先放出slow_log配置信息
~~~
slow_query_log=1
slow_query_log_file=mysql-slow.log
long_query_time=2
log_queries_not_using_indexes=1
log_throttle_queries_not_using_indexes=10
log_slow_admin_statements=1
log_slow_slave_statements=1
min_examined_row_limit=1000
log_output=FILE
[mysqld-5.7]
log_timestamps=system
~~~


1、slow_query_log：表示是否开启slow log ，此参数与log_slow_queries的作用没有区别，5.6以后的版本使用此参数替代log_slow_queries。

2、 slow_query_log_file：当使用文件存储slow log时(log_output设置为”FILE”或者”FILE,TABLE”时)，slow log存储于指定路径的文件，默认的slow log文件名为”主机名-slow.log”，slow log的位置为datadir参数所对应的目录位置，一般情况下为 /var/lib/mysql。

3、long_query_time：表示”`多长时间的查询`被认定为`慢查询`，此值得默认值为10秒，表示超过10秒的查询被认定为慢查询。大于long_query_time 会被记录，而刚好等于long_query_time 不会记录。

4、log_queries_not_using_indexes：将`没有使用索引`的语句记录到slow log。 有些语句虽然执行很快，没有达到long_query_time阈值，这时也要记录下来。如测试环境下数据量非常少，即使sql写的烂也会很快，但是放到线上环境下就会变的非常慢然后又不会记录到slow.log（就是为了杜绝这种情况）。另外有些语句使用了索引，当时有使用派生表（派生表不会使用索引）也会被记录下来，这点有点讨厌。当然还是看具体情况如何，建议开启。

5、log_throttle_queries_not_using_indexes：5.6.5版本新引入的参数，当log_queries_not_using_inde设置为ON时，没有使用索引的查询语句也会被当做慢查询语句记录到slow log中，使用log_throttle_queries_not_using_indexes可以限制这种语句`每分钟`记录到slow log中的次数，因为在生产环境中，有可能有很多没有使用索引的语句，此类语句频繁地被记录到slow log中，可能会导致slow log快速不断的增长，管理员可以通过此参数进行控制。设置10，每分钟最多记录10条同样的没有使用索引的慢查询。

6、min_examined_row_limit： `扫描记录数`少于设定值的语句不会被记录到slow log。比如sleep(5) 就不会记录下来，因为它扫描记录数是0小于min_examined_row_limit 。设置1000，超过1000时才会记录。防止slow.log过大。

7、log_slow_admin_statements：记录执行缓慢的`DDL`语句，如alter table,analyze table, check table, create index, drop index, optimize table, repair table等。  

8、log_slow_slave_statements：记录`从库`上执行的慢查询语句。

9、log_timestamps：5.7版本新增时间戳所属时区参数，默认记录UTC时区的时间戳到slow log；应修改为记录系统时区(这是5.7的一个坑，建议设置为system。若不设置则会`慢8小时 `)。因为log_timestamps在mysql5.6下无效，因此我们可以这样配置：
~~~
[mysqld-5.7]
log_timestamps=system 
~~~
  
10、log_output：指定慢查询日志的输出方式，从5.5版本开始可以记录到日志文件(FILE，慢查询日志)和数据库表(TABLE，mysql.slow_log)中 。建议设置为FILE，不建议记录到表中。
- 记录到TABLE性能开销更大。
- 如果数据进行备份的话，可能把这个表也备份了；当然这是没有意义的。

当然记录到TABLE中也有好处：
- 可以直观展示slow log信息。
最终选择啥，具体情况具体分析吧~

~~~
(root@localhost) [mysql]>desc mysql.slow_log;
+----------------+---------------------+------+-----+----------------------+--------------------------------+
| Field          | Type                | Null | Key | Default              | Extra                          |
+----------------+---------------------+------+-----+----------------------+--------------------------------+
| start_time     | timestamp(6)        | NO   |     | CURRENT_TIMESTAMP(6) | on update CURRENT_TIMESTAMP(6) |
| user_host      | mediumtext          | NO   |     | NULL                 |                                |
| query_time     | time(6)             | NO   |     | NULL                 |                                |
| lock_time      | time(6)             | NO   |     | NULL                 |                                |
| rows_sent      | int(11)             | NO   |     | NULL                 |                                |
| rows_examined  | int(11)             | NO   |     | NULL                 |                                |
| db             | varchar(512)        | NO   |     | NULL                 |                                |
| last_insert_id | int(11)             | NO   |     | NULL                 |                                |
| insert_id      | int(11)             | NO   |     | NULL                 |                                |
| server_id      | int(10) unsigned    | NO   |     | NULL                 |                                |
| sql_text       | mediumblob          | NO   |     | NULL                 |                                |
| thread_id      | bigint(21) unsigned | NO   |     | NULL                 |                                |
+----------------+---------------------+------+-----+----------------------+--------------------------------+
12 rows in set (0.00 sec)
~~~



###问题
**1、怎么在线清理slow log？**
不要直接>slow.log ，这样做空间不会释放的。

step1、先备份一下；此时文件句柄已经打开，备份之后其实日志还是输出到 mysql-slow.2020.05.16
~~~
mv mysql-slow.log mysql-slow.2020.05.16
~~~
step2、在客户端执行flush slow logs;关闭原来的slow log 文件句柄，打开新的 slow.log 文件句柄。这样才会输出到新的slow.log 
~~~
(root@localhost) [(none)]>flush slow logs;
Query OK, 0 rows affected (0.00 sec)
~~~

**2、因为锁等待时间过长的语句不会被记录到slow.log**
slow log 只会按run time真正运行的时间来算，而不把lock_time锁等待的时间计算在内。也就是说因为lock而执行过久的语句不会被记录到slow log。slow log只会以run time时间为准！
~~~
run time = Query_time - lock_time
~~~

举个例子，如下：
Q1
~~~
(root@localhost) [test]>begin;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [test]>select * from test1 for update;
+------+------+
| id   | name |
+------+------+
|    1 | abcd |
+------+------+
1 row in set (0.00 sec)
~~~
Q2
~~~
(root@localhost) [(none)]>begin;
Query OK, 0 rows affected (0.00 sec)
(root@localhost) [(none)]>use test;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
(root@localhost) [test]>update test1 set name='efg' where id=1;
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction

~~~
观察slow log文件内容：
update test1 set name='efg' where id=1;语句即使执行了那么久然而没有记录到slow log。
~~~
[root@localhost ~]# tail -f /mdata/mysql57/mysql-slow.log
ALTER TABLE test1 ADD PRIMARY KEY(id);
/home/mysql5.7/mysql-5.7.33-linux-glibc2.12-x86_64/bin/mysqld, Version: 5.7.33-log (MySQL Community Server (GPL)). started with:
Tcp port: 3305  Unix socket: /tmp/mysql.sock3305
Time                 Id Command    Argument
# Time: 2021-05-16T18:17:37.303914+08:00
# User@Host: root[root] @ localhost []  Id:     4
# Query_time: 0.000134  Lock_time: 0.000066 Rows_sent: 1  Rows_examined: 1
use test;
SET timestamp=1621160257;
select * from test1 for update;
~~~


**那对于slow log记录不了lock waiting 的语句有其它方法抓取吗？**
使用 show processlist;
~~~
(root@localhost) [(none)]>show processlist;
+----+------+-----------+------+---------+------+----------+----------------------------------------+
| Id | User | Host      | db   | Command | Time | State    | Info                                   |
+----+------+-----------+------+---------+------+----------+----------------------------------------+
|  2 | root | localhost | test | Query   |   21 | updating | update test1 set name='efg' where id=1 |
|  3 | root | localhost | test | Sleep   |   24 |          | NULL                                   |
|  4 | root | localhost | NULL | Query   |    0 | starting | show processlist                       |
+----+------+-----------+------+---------+------+----------+----------------------------------------+
3 rows in set (0.00 sec)

~~~
难的是有些语句是Command 是sleep状态，Time又非常长。Info又是空的。
因为应用开发的代码写错了，没有commit。导致被锁住。




**3、slow log几个字段的含义**

Query_time: *`duration`*`
    The statement execution time in seconds.

*   `Lock_time: *`duration`*`
    The time to acquire locks in seconds.
*   `Rows_sent: *`N`*`
    The number of rows sent to the client.

*   `Rows_examined: `

    The number of rows examined by the server layer (not counting any processing internal to storage engines).

Each statement written to the slow query log file is preceded by a [`SET`]
 statement that includes a timestamp indicating when the slow statement was logged (which occurs after the statement finishes executing).

Passwords in statements written to the slow query log are rewritten by the server not to occur literally in plain text. See [Section 6.1.2.3, “Passwords and Logging”]

