---
title: mysql-运维操作之连接统计.md
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
title: mysql-运维操作之连接统计.md
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
###用户连接类
1、查看每个客户端IP过来的连接消耗资源情况。

select * from sys.host_summary;

2、查看每个用户消耗资源情况

select * from sys.user_summary;


3、查看当前连接情况（有多少连接就应该有多少行）

select host,current_connections,statements from sys.host_summary;


4、查看当前正在执行的SQL

和执行show full processlist的结果差不多
select conn_id,pid,user,db,command,current_statement,last_statement,time,lock_latency from sys.session

###SQL 和io类
1、查看发生IO请求前5名的文件。

select * from sys.io_global_by_file_by_bytes order by total limit 5;

###buffer pool 、内存
1、查看总共分配了多少内存

select * from sys.memory_global_total;
select * from sys.memory_global_by_current_bytes;


2、每个库（database）占用多少buffer pool

select * from sys.innodb_buffer_stats_by_schema order by allocated desc;

>pages是指在buffer pool中的page数量；pages_old指在LUR 列表中处于后37%位置的page。当出现buffer page不够用时，就会征用这些page所占的空间。37%是默认位置，具体可以自定义。


3、统计每张表具体在InnoDB中具体的情况，比如占多少页？

注意和前面的pages的总数都是相等的，也可以借用sum（pages）运算验证一下。

select * from sys.innodb_buffer_stats_by_table;




4、查询每个连接分配了多少内存

利用session表和memory_by_thread_by_current_bytes分配表进行关联查询。
~~~
SELECT
 b.USER,
 current_count_used,
 current_allocated,
 current_avg_alloc,
 current_max_alloc,
 total_allocated,
 current_statement 
FROM
 sys.memory_by_thread_by_current_bytes a,
 sys.SESSION b 
WHERE
 a.thread_id = b.thd_id;
~~~


###字段、索引、锁
1、查看表自增字段最大值和当前值，有时候做数据增长的监控，可以作为参考。

select * from sys.schema_auto_increment_columns;

2、MySQL索引使用情况统计

select * from sys.schema_index_statistics order by rows_selected desc;



3、MySQL中有哪些冗余索引和无用索引

若库中展示没有冗余索引，则没有数据；当有联合索引idx_abc(a,b,c)和idx_a(a)，那么idx_a就算冗余索引了。

select * from sys.schema_redundant_indexes;



4、查看INNODB 锁信息

在未来的版本将被移除，可以采用其他方式

select * from sys.innodb_lock_waits

5、查看库级别的锁信息，这个需要先打开MDL锁的监控：

--打开MDL锁监控
update performance_schema.setup_instruments set enabled='YES',TIMED='YES' where name='wait/lock/metadata/sql/mdl';
select * from sys.schema_table_lock_waits;

###线程类

1、MySQL内部有多个线程在运行，线程类型及数量

select user,count(*) from sys.`processlist` group by user;


###主键自增

查看MySQL自增id的使用情况
~~~

SELECT
 table_schema,
 table_name,
 ENGINE,
 Auto_increment 
FROM
 information_schema.TABLES 
WHERE
 TABLE_SCHEMA NOT IN ( "INFORMATION_SCHEMA", "PERFORMANCE_SCHEMA", "MYSQL", "SYS" )
ORDER BY Auto_increment DESC
~~~
