---
title: mysql-死锁排查.md
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
title: mysql-死锁排查.md
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
###1、当出现事务执行阻塞时，首先想到查询当前MySQL进程状态：
~~~
SHOW FULL PROCESSLIST;
~~~

###2、查看当前的死锁线程id和导致的sql
~~~
SELECT * FROM PERFORMANCE_SCHEMA.events_statements_current
~~~
###3、条件允许复制可以直接使用这个sql，清晰的打印sql
~~~
SELECT
	a.trx_id,
	d.SQL_TEXT,
	a.trx_state,
	a.trx_started,
	a.trx_query,
	b.ID,
	b.USER,
	b.DB,
	b.COMMAND,
	b.TIME,
	b.STATE,
	b.INFO,
	c.PROCESSLIST_USER,
	c.PROCESSLIST_HOST,
	c.PROCESSLIST_DB 
FROM
	information_schema.INNODB_TRX a
	LEFT JOIN information_schema.PROCESSLIST b ON a.trx_mysql_thread_id = b.id 
	AND b.COMMAND = 'Sleep'
	LEFT JOIN PERFORMANCE_SCHEMA.threads c ON b.id = c.PROCESSLIST_ID
	LEFT JOIN PERFORMANCE_SCHEMA.events_statements_current d ON d.THREAD_ID = c.THREAD_ID;
~~~



###4、information_schema 三剑客

在InnoDB1.0版本之前,用户只能通过命令 SHOW FULL PROCESSLIST,SHOW ENGINE INNODB STATUS等来查看当前数据库中锁的请求,然后再判断事务锁的情 况。从 InnoDB11.0开始,在 INFORMATIONSCHEMA架构下添加了表 INNODB_TRX、 INNODB LOCKS、 INNODB LOCK_WATS。通过这三张表,用户可以更简单地监控当 前事务并分析可能存在的锁问题。

> 只记录行锁和表锁，而因为线上dll修改表结构导致的阻塞问题不会被记录

######1、查询正在活跃的事务 
~~~
SELECT * FROM information_schema.INNODB_TRX
~~~

>1、trx_id   innodb存储引擎内部唯一的事务id
2、trx_state 事务状态，枚举值（RUNNING、LOCK）
3、trx_started 事务开始时间
4、trx_requested_lock_id
5、trx_wait_started
6、trx_weight
7、trx_mysql_thread_id事务线程id（使用kill值即可杀死该事务）
8、trx_query：事务执行的语句
9、trx_operation_state:事务的当前操作如果有的话否则为null
10、trx_tables_in_use:innodb表的数据用于当处理当前的sql语句
11、trx_tables_locked:innodb表的数量当前sql语句有行锁在上面(因为那些是行锁,不是表锁,表仍旧可以读取和写入通过多个事务m尽管一些记录被锁定)
12、trx_lock_structs：事务保留的锁的数量
13、trx_lock_memory_bytes：这个事务在内存中lock结构占据的大小
14、trx_rows_locked:这个事务锁定的记录。使用 `INSERT into SELECT`指定的原表会逐渐对表中所有记录添加共享锁，这个值会从0开始增加到总记录数
15、trx_rows_modified:此事务中修改和插入记录的数目
16、trx_concurrency_tickets
17、trx_isolation_level当前事务的隔离级别
18、trx_unique_checks
19、trx_foreign_key_checks
20、trx_last_foreign_key_error
21、trx_adaptive_hash_latched
22、trx_adaptive_hash_timeout
23、trx_is_read_only 是否为只读事务 0不是 1是
24、trx_autocommit_non_locking



######2、查看持有锁的事务
~~~
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS; 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6d350e58661d111e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>1、lock_id 锁的ID 
2、lock trx_id 事务ID 
3、lock_mode 锁的模式 ，可以取值为 X 、 S、GAP
4、lock_type 锁的类型,表锁还是行锁 
5、lock table 要加锁的表 
6、lock index 锁住的索引 
7、lock_space 锁对象的 space id 
8、lockpage 事务锁定页的数量。若是表锁,则该值为NULL 
9、lock rec 事务锁定行的数量,若是表锁,则该值为NULL 
10、lock data 事务锁定记录的主键值,若是表锁,则该值为NULL


######3、查询等待锁的事务
~~~
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS;
~~~
> 1、requesting trx id 申请锁资源的事务ID
2、 blocking trx id 阻塞的事务ID 
3、requesting_ lock _id 申请的锁的ID
4、 blocking trx id 阻塞的锁的ID 


~~~		
SELECT
	r.trx_id waiting_trx_id,
	r.trx_mysql_thread_id waiting_thread,
	r.trx_query waiting_query,
	b.trx_id blocking_trx_id,
	b.trx_mysql_thread_id blocking_thread,
	b.trx_query blocking_query 
FROM
	information_schema.innodb_lock_waits w
	INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
	INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8fa92b13056a7b07.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>waiting_query 是当前等到锁的事务发出的阻塞sql
blocking_query 则是阻塞sql阻塞等待的未提交的sql

###5、查看事务和mysql连接用户对应关系

~~~
SELECT
	* 
FROM
	information_schema.PROCESSLIST p
	LEFT JOIN information_schema.INNODB_TRX t ON p.id = t.trx_mysql_thread_id
~~~



###6、查看被锁住表

mysql查看被锁住的表，查询是否锁表
show OPEN TABLES where In_use > 0;



###7、查看innodb引擎的运行时信息
show engine innodb status;

查看造成死锁的sql语句，分析索引情况，然后优化sql语句；
查看服务器状态
show status like '%lock%';
查看超时时间：
show variables like '%timeout%';


###8、杀死事务所在线程/活跃mysql连接

kill  trx_tread_id
