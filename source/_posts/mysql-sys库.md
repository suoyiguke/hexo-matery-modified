---
title: mysql-sys库.md
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
title: mysql-sys库.md
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
Sys库非常方便，5.6没有可以自己安装

###Sys库里的数据来源
Sys库所有的数据源来自：performance_schema。目标是把performance_schema的把复杂度降低，让DBA能更好的阅读这个库里的内容。让DBA更快的了解DB的运行情况。

 

###Sys库下有两种表

- 字母开头： 适合人阅读，显示是格式化的数

- x$开头 ： 适合工具采集数据，原始类数据

 

###每类表大概介绍

sys_开头是库里的配置表：

sys_config用于sys schema库的配置

 

视图：

host : 以IP分组相关的统计信息

innodb : innodb buffer 相关信息

io : 数据内不同维度展的IO相关的信息

memory : 以IP，连接，用户，分配的类型分组及总的占用显示内存的使用

metrics : DB的内部的统计值

processlist : 线程相关的信息(包含内部线程及用户连接）

ps_ : 没有工具统计的一些变量（没看出来存在的价值）

schema : 表结构相关的信息，例如： 自增，索引， 表里的每个字段类型，等待的锁等等

session : 用户连接相关的信息

statement : 基于语句的统计信息（重店）

statements_ : 出错的语句，进行全表扫描， 运行时间超长，排序相等（重点）

user_ : 和host_开头的相似，只是以用户分组统计

wait :  等待事件，比较专业，难看懂。

waits : 以IP，用户分组统计出来的一些延迟事件，有一定的参考价值。

 

###Sys库能做什么，那么我们先来看看以下的问题，对于数据库，你有没有以下的疑问？

1. 谁使用了最多的资源？ 基于IP或是用户？

2. 大部分连接来自哪里及发送的SQL情况？

3. 机器执行多的SQL语句是什么样？

4. 哪个文件产生了最多的IO，它的IO模式是怎么样的？

5. 那个表的IO最多？

6. 哪张表被访问过最多？

7. 哪些语句延迟比较严重？

8. 哪些SQL语句使用了磁盘临时表

9. 哪张表占用了最多的buffer pool

10. 每个库占用多少Buffer pool

11. 每个连接分配多少内存？

12. MySQL内部现在有多个线程在运行？

 

 ####host_summary

mysql> select * from host_summary\G

*************************** 1. row***************************

                  host: localhost #从哪个服务器链接过来的 如果为null 表示内部链接

           statements: 203  这台服务器执行了多少语句

    statement_latency: 105.45 ms 这台服务器发来等待语句执行时间

 statement_avg_latency: 519.45 us 该服务器等待语句执行的平均时间

          table_scans: 7 该服务器扫描表的次数（非全表）

              file_ios: 795 该服务器i/o时间请求的次数

      file_io_latency: 27.43 ms  该服务器请求等待i/o的时间

  current_connections: 1 该服务器当前的连接数

    total_connections: 1 该服务器总db共链接多少次

         unique_users: 1  该服务器上有几个不同用户账户连接过来

       current_memory: 0 bytes 该服务器上当前链接等占用的内存

total_memory_allocated: 0 bytes 该服务器上的请求总共使用内存量


 ####host_summary
 mysql>select host,current_connections from host_summary;

+-----------+---------------------+

| host      |current_connections |

+-----------+---------------------+

| localhost |                   1 |

+-----------+---------------------+

----------------------------------------------------------------------------------------------------

| host_summary 

####主机概要

host: 监听连接过的主机

statements 当前主机执行的语句总数

statement_latency 语句等待时间

statement_avg_latency 执行语句平均延迟时间

table_scans 表扫描次数

file_ios io时间总数

file_io_latency 文件io 延迟

current_connections 当前连接数

total_connections: 总连接数

unique_users: 改主机唯一用户数

current_memory: 当前账户分配的内存

total_memory_allocated: 该主机内存总数

------------------------------------------------------------------------------------------------------

| host_summary_by_file_io

host 主机

ios: io事件总数

io_latency io总的延迟时间

--------------------------------------------------------------------------------------------------------------------

 

| host_summary_by_file_io_type

host: 主机

event_name io事件名称

total: 该主机发生的事件

total_latency: 该主机发生io 时间总延迟时间

max_latency: 该主机io 事务中最大的延迟时间

-----------------------------------------------------------------------------------------------------------------------------

| host_summary_by_stages

host 主机

event_name stage event名称

total: stage event发生的总数

total_latency stage event总的延迟时间

avg_latency stage event 平均延迟时间

----------------------------------------------------------------------------------------------------------------

| host_summary_by_statement_latency

host: 主机

total: 这个主机的语句总数

total_latency: 这个主机总的延迟时间

max_latency: 主机最大的延迟时间

lock_latency: 等待锁的锁延迟时间

rows_sent:  该主机通过语句返回的总行数

rows_examined: 在存储引擎上通过语句返回的行数

rows_affected: 该主机通过语句影响的总行数

full_scans: 全表扫描的语句总数

--------------------------------------------------------------------------------------------------------------------------

| host_summary_by_statement_type

host: 主机

statement: 最后的语句时间名称

total:  sql语句总数

total_latency: sql语句总延迟数

max_latency: 最大的sql语句延迟数

lock_latency: 锁延迟总数

rows_sent: 语句返回的行总数

rows_examined: 通过存储引擎的sql语句的读取总行数

rows_affected: 语句影响的总行数

full_scans:  全表扫描的语句事件总数

----------------------------------------------------------------------------------------------------------------------------------------------------------

| innodb_buffer_stats_by_schema

每个库占用多少 buffer pool

object_schema: 数据库的名称

allocated:分配给当前数据库的总的字节数

data: 分配给当前数据的数据字节

pages: 分配给当前数据库的总页数

pages_hashed: 分配给当前数据库的hash页数

pages_old: 分配给当前数据库的旧页数

rows_cached: 当前数据库缓存的行数

------------------------------------------------------------------------------------------------------------------------

#### innodb_buffer_stats_by_table
那张表 占用最多的 buffer pool
select * from innodb_buffer_stats_by_table order bypages desc limit 10;

object_schema: 数据库的名称

object_name: 表名称

allocated: 分配给表的总字节数

data: 分配该表的数据字节数

pages: 分配给表的页数

pages_hashed: 分配给表的hash页数

pages_old: 分配给表的旧页数

rows_cached: 表的行缓存数

 

####那张表的io最多

select * from io_global_by_file_by_bytes limit 10\G

-----------------------------------------------------------------------------------------------------------------------------------------------

| innodb_lock_waits

显示当前实例的锁情况

wait_started 锁等待发生的实际

wait_age 锁已经等待了多长时间

wait_age_secs 以秒为单位显示已经等待的时间

locked_table 被锁的表

locked_index 被锁住的索引

locked_type 锁类型

waiting_trx_id 正在等待的事务id

waiting_trx_started 等待事务开始的时间

waiting_trx_age 已经等待事务多长时间

waiting_trx_rows_locked 正在等待的事务被锁的行数量

waiting_trx_rows_modified 正在等待行重定义数量

waiting_pid 正在等待事务的线程id

waiting_query 正在等待锁的查询

waiting_lock_id 正在等的锁的id

waiting_lock_mode 等待锁的模式

blocking_trx_id 阻塞等待锁的事务id

blocking_pid 正在锁的线程id

blocking_query 正在锁的查询

blocking_lock_id 正在阻塞等待锁的锁id

blocking_lock_mode 阻塞锁模式

blocking_trx_started 阻塞事务开始的实际

blocking_trx_age 阻塞的事务已经执行的时间

blocking_trx_rows_locked 阻塞事务锁住的行的数量

blocking_trx_rows_modified 阻塞事务重定义行的数量

sql_kill_blocking_query kill语句杀死正在运行的阻塞事务

sql_kill_blocking_connection kill 语句杀死会话中正在运行的阻塞事务

----------------------------------------------------------------------------------------------------------------------------------------

| io_by_thread_by_latency   

通过io的消耗展示io等待的时间

user:  对于当前线程来说 线程被分配的账户 后台线程线程的名称

total: io事件的总数

total_latency: io事件的总延迟数

min_latency: 单个最小的io事件延迟

avg_latency: 平均io延迟

max_latency: 最大io延迟

thread_id: 线程id

processlist_id: 对于当前线程就是此时的id 对于后台就是null

-----------------------------------------------------------------------------------------------------------------------------------

 

 

| io_global_by_file_by_latency

file: 文件路径名

total:  i/o事务的总数量

total_latency: i/o事务总等待时间

count_read: i/o读文件总数

read_latency: i/o事务读文件总数

count_write: i/o事务写文件总数

write_latency: i/o事务总等待时间写文件

count_misc: i/o事务的总数文件

misc_latency: i/o 事务总等待时间

-----------------------------------------------------------------------------------------------------------------------------------------

| io_global_by_wait_by_bytes

event_name: i/o事件名

total: i/o事件总数

total_latency: i/o时间总等待时间

min_latency: i/o最小等待时间

avg_latency: i/o平均等待时间

max_latency: i/o最大等待时间

count_read: i/o读请求数量

total_read: i/o读取字节数

avg_read: i/o 平均读字节数

count_write: i/o 写请求数量

total_written: i/o 写的字节数

avg_written: i/o 平均写字节数

total_requested: i/o读取和写入的字节总数

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

| io_global_by_wait_by_latency

event_name: i/o事件名称

total: i/o事件总数

total_latency: i/o总等待时间

avg_latency: i/o平均等待时间

max_latency: i/o 最大等待

read_latency: i/o 读等待时间

write_latency: i/o 写等待时间

misc_latency: i/o 总等待时间

count_read: i/o读请求数量

total_read: i/o读取字节数

avg_read: i/o平均读取字节数

count_write: i/o写请求数

total_written:i/o 写的字节数

avg_written: 平均写字节数

-----------------------------------------------------------------------------------------------------------------

| latest_file_io

thread  前台线程 与线程相关联的账户 后台线程  线程的名字和线程id

file  文件路径名

latency  io等待时间文件

operation 操作类型

requested i/o 请求的数据字节的文件

---------------------------------------------------------------------------------------------------------------------------

| memory_by_host_by_current_bytes

host: 客户端连接的主机

current_count_used: 尚未释放内存块的数目

current_allocated: 当前主机内存没有被释放字节

current_avg_alloc: 当前分配的自己数

current_max_alloc: 最大的单一内存分配 字节

total_allocated: 主机的内存分配总数  字节

--------------------------------------------------------------------------------------------------------------------------------------------------------------

| memory_by_thread_by_current_bytes

每个连接分配多少内存

selectb.user,current_count_used,current_allocated,current_avg_alloc,current_max_alloc,total_allocated,current_statementfrom memory_by_thread_by_current_bytes a, session b where a.thread_id=b.thd_id;

 thread_id: 线程id

user: 线程用户或者线程名称

current_count_used: 当前数量尚未释放线程

current_allocated: 尚未释放线程

current_avg_alloc: 线程的内存块

urrent_max_alloc: 最大单一线程内存分配

  total_allocated: 线程的内存分配字节总数

--------------------------------------------------------------------------------------------------------------------

| memory_by_user_by_current_bytes

user: 客户端用户名

current_count_used: 当前用户还没有被释放内存

current_allocated: 用户还没有被释放内存 字节

current_avg_alloc: 当前用户分配每个内存 字节

current_max_alloc: 最大单一用户内存分配 字节

total_allocated: 用户总内存 字节

------------------------------------------------------------------------------------------------------------------------------------

| memory_global_by_current_bytes

event_name: 事件名称

current_count: 事件总数

current_alloc: 事件分配内存没有被释放

current_avg_alloc: 事件内存分配字节数

high_count: 内存的高水位

high_alloc: 内存的高水位 字节

high_avg_alloc: 高水位平均 字节

-------------------------------------------------------------------------------------

| memory_global_total

total_allocated 服务器总内存分配

 

| metrics

 

---------------------------------------------------------------------------------------------

| processlist

mysql 内部的线程类型和数量

mysql> select user,count(*) from processlistgroup by user;

thd_id: 线程id

conn_id: 连接id

user: 线程用户或者线程名称

db: 线程的默认数据库

command: 前台线程 线程正在执行命令

state: 事件或者状态

time: 时间间隔 以秒为单位

current_statement: 正在执行线程

statement_latency: 语句执行多长时间

progress: 工作完成百分比

lock_latency: 所花费时间等待锁

rows_examined: 从存储引擎读取行数

rows_sent: 当前语句所返回的行数

rows_affected: 当前语句受影响的行数

tmp_tables: 内存临时表

tmp_disk_tables: 磁盘上的临时表

full_scan: 执行语句全表扫描

last_statement: 语句执行的线程

last_statement_latency: 语句执行多长时间

current_memory: 线程分配字节数

last_wait: 事件的线程名称

ast_wait_latency: 时间线程等待时间

source: 源文件和行 包含的事件

trx_latency: 线程的当前事务的等待时间

trx_state: 线程当前事务状态

trx_autocommit: 是否自动提交

pid: 客户端进程id

program_name: 客户端程序的名字

-----------------------------------------------------------------------------------------------

 

| ps_check_lost_instrumentation

variable_name: 性能模式状态和名称

variable_value: 数量

--------------------------------------------------------------------------------------------

| schema_auto_increment_columns

table_schema: 表名

table_name: 库名

column_name: id

data_type: 列的数据类型

column_type: 列的列类型

is_signed:

is_unsigned: 0

max_value: 最大允许的值列

auto_increment: 1

auto_increment_ratio: 比率列值

---------------------------------------------------------------------------------------------------------------------

| schema_index_statistics          介绍的是实例下所有库里的索引的信息

table_schema: 库名

table_name: 表名

index_name: 索引名称

rows_selected: 使用索引读取的总行数

select_latency: 读取索引总等待时间

rows_inserted: 插入行总索引数

insert_latency: 插入索引总等待时间

rows_updated: 更新索引总行数

update_latency: 更新索引总等待时间

 rows_deleted: 从索引删除总行数

delete_latency: 删除索引总等待时间

 

mysql> select * from schema_index_statisticswhere table_schema='test' and table_name='test2' \G;

*************************** 1. row***************************

 table_schema: test

   table_name: test2

   index_name: test2_id

 rows_selected: 0

select_latency: 0 ps

 rows_inserted: 0

insert_latency: 0 ps

 rows_updated: 0

update_latency: 0 ps

 rows_deleted: 0

delete_latency: 0 ps

1 row in set (0.00 sec)

 

-----------------------------------------------------------------------------------------------------------

| schema_object_overview  可以知道当前数据库模式下有多少种类型的对象和对象个数                                  

db: 数据名称

object_type: 类型

 count: 数量

 

mysql> select * from schema_object_overviewwhere db='sys';

+-----+---------------+-------+

| db  |object_type   | count |

+-----+---------------+-------+

| sys | BASE TABLE    |    1 |

| sys | INDEX (BTREE) |     1 |

| sys | TRIGGER       |    2 |

| sys | FUNCTION      |   22 |

| sys | PROCEDURE     |   26 |

| sys | VIEW          |  100 |

+-----+---------------+-------+

6 rows in set (0.06 sec)

 

------------------------------------------------------------------------------------------

| schema_redundant_indexes

冗余索引

table_schema

table_name 表名

redundant_index_name 冗余索引名称

redundant_index_columns 冗余索引的列名称

redundant_index_non_unique  冗余索引中的列的数量

dominant_index_name 索引名称

dominant_index_columns 列的名称

dominant_index_non_uniqu

subpart_exists 是否索引一部分

sql_drop_index 要执行的语句 删除冗余索引

------------------------------------------------------------------------------------------------------------

| schema_table_lock_waits

被阻塞等待锁

object_schema 锁定名

object_name 检测名

waiting_thread_id 等待的线程id

waiting_pid processlist id 等待锁

waiting_account 与会话关联的账户 等待锁

waiting_lock_type 等待锁类型

waiting_lock_duration 多长时间锁等待

waiting_query等待锁的声明

waiting_query_secs 一直等待多长时间

waiting_query_rows_affected  影响的行数

waiting_query_rows_examined 从存储引擎读取的行数

blocking_thread_id 线程的线程id阻塞等待锁

blocking_pid processlist id的线程阻塞等待锁

blocking_account 与线程相关联的账户阻塞等待锁

blocking_lock_type 锁阻塞等待的锁类型

blocking_lock_duration 锁阻塞被持有多长时间

sql_kill_blocking_querykiil 语句杀死阻塞语句

sql_kill_blocking_connection kill语句执行运行阻塞会话语句

----------------------------------------------------------------------------------------------------------------------------------------------

| schema_table_statistics

统计表的信息

table_schema: 库名称

table_name: 表名

total_latency: i/o 总等待时间

 rows_fetched: 从表读取行数总数

fetch_latency: i/o总等待时间

rows_inserted: 行插入到表中时间

 insert_latency: i/o总等待插入时间

 rows_updated: 表中总更新行数

update_latency: i/o总等待更新时间

rows_deleted: 表中删除的行数

delete_latency: i/o总等待删除时间

io_read_requests: 表读取请求总数

io_read: 从表读取字节总数

io_read_latency: 从表读取总时间

io_write_requests: 表写请求总数

io_write: 写入的自己总数

io_write_latency: 写的总等待时间

io_misc_requests: i其他/o请求总数

io_misc_latency: i/o总等待时间

----------------------------------------------------------------------------------------------------------------------------------

 

| schema_table_statistics_with_buffer

table_schema: 库名

table_name: 表名

rows_fetched: 从表读取总行数

fetch_latency: 读取总等待时间

rows_inserted: 插入表中总数

insert_latency: 插入等待总时间

rows_updated: 表中更新行数

update_latency: 更新表中i/o总等待时间

rows_deleted: 表中删除的行数

delete_latency: 删除表中i/o总等待时间

io_read_requests: 表中读取总数

io_read: 表中读取字节总数

io_read_latency: 表中读取总等待时间

io_write_requests: 表的写请求总数

io_write: 写的字节总数

io_write_latency: 写的总等待时间

io_misc_requests: 其他i/o请求表

io_misc_latency: i/o请求总等待时间

innodb_buffer_allocated: innodb缓冲区字节

innodb_buffer_data: innodb数据字节分配表

innodb_buffer_free: innodb nondata 字节分配表

innodb_buffer_pages: innodb页面分配表

innodb_buffer_pages_hashed: innodb 页面分配表

innodb_buffer_pages_old: innodb旧页分配表

innodb_buffer_rows_cached: innodb缓存表行

-------------------------------------------------------------------------------------------------------------------

| schema_tables_with_full_table_scans    查看那些表走了全表扫描，性能情况

object_schema 库名

object_name 表名

rows_full_scanned 全表扫描总行数

latency 全表扫描总等待时间

---------------------------------------------------------------------------------------------------------------------

| schema_unused_indexes

使用索引的表

object_schema 库名

object_name 表名

index_name 未使用的索引名称

---------------------------------------------------------------------------------------------------------------------

| session             

  # 当前执行的sql

thd_id: 30

conn_id: 2

user: root@localhost

db: sys

command: Query

state: Sending data

time: 0

current_statement: select * from session

statement_latency: 1.47 ms

progress: NULL

lock_latency: 751.00 us

rows_examined: 0

rows_sent: 0

rows_affected: 0

tmp_tables: 4

tmp_disk_tables: 1

full_scan: YES

last_statement: NULL

last_statement_latency: NULL

current_memory: 0 bytes

ast_wait: NULL

last_wait_latency: NULL

source: NULL

trx_latency: NULL

trx_state: NULL

trx_autocommit: NULL

pid: 2698

program_name: mysql

-----------------------------------------------------------------------------------------------------------------

| session_ssl_status

显示ssl版本和密码

thread_id  连接的线程id

ssl_version 使用ssl的版本

ssl_cipher ssl连接的密码

ssl_sessions_reused 重用ssl会话连接数量

---------------------------------------------------------------------------------------------------------------

| statement_analysis        

  #那张表访问次数最多

query:  语句字符串

db: 默认数据库

full_scan: 执行全表扫描的总数出现的语句

exec_count: 执行语句总数

err_count: 错误的总数

warn_count: 警告的总数

total_latency: 总等待时间

max_latency: 最大单等待时间

avg_latency: 平均等待时间

lock_latency: 等待锁

rows_sent: 语句返回的行数

rows_sent_avg: 平均每个出现语句返回行数

rows_examined: 读取行数总数从存储引擎

rows_examined_avg: 平均读取的行数 从存储引擎

rows_affected: 受时间影响的行数

rows_affected_avg: 平均没出息的语句影响行数

tmp_tables:  内部内存临时表的总数

tmp_disk_tables: 内部磁盘上的临时表的总数

rows_sorted: 行总数

sort_merge_passes: 分类合并总数

digest:

first_seen: 第一次时间

 last_seen: 最近时间

------------------------------------------------------------------------------------------------------------------------------------------

| statements_with_errors_or_warnings

产生的错误或者警告

query    语句字符串  

db 数据库

exec_count 执行语句总数

errors 错误总数

error_pct 比例出现了错误

warnings 警告的总数

warning_pct 警告的比例

first_seen第一次的时间

last_seen最近的时间

digest声明

----------------------------------------------------------------------------------------------------------------------------------------------------------

| statements_with_full_table_scans

全表扫描

query: 语句字符串

db: 数据库

exec_count: 执行语句

total_latency: 总等待时间

no_index_used_count: 没有索引扫描表的总数

no_good_index_used_count: 用于扫描表的总数

no_index_used_pct: 没有索引扫描表的百分比

rows_sent: 表中返回的行数

rows_examined: 读取行的总数 在索引中

rows_sent_avg: 表中平均返回行数

rows_examined_avg: 读取行数平均从表的存储引擎

first_seen: 第一次时间

last_seen: 最近时间

digest: 声明

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

 

| statements_with_runtimes_in_95th_percentile  

query: 语句字符串

db: 数据库

full_scan: 执行全表扫描的总数语句

exec_count: 执行语句

err_count: 错误的总数

warn_count: 警告的总数

total_latency: 总等待时间

max_latency: 最大单等待时间

avg_latency: 平均但等待时间

rows_sent: 总出现的语句返回的行数

rows_sent_avg: 平均每个出现的语句返回行数

rows_examined: 读取行数的总数存储引擎

rows_examined_avg: 平均读取行数 存储引擎

first_seen: 第一次时间

last_seen: 最近时间

digest: 声明

------------------------------------------------------------------------------------------------------------------------------------------

| statements_with_sorting  

sort 排序相关                   

query: 语句字符串

db: 数据库

exec_count: 执行语句

total_latency: 总等待时间

sort_merge_passes: 分类合并经过出现总数

avg_sort_merges: 分类合并平均数量

sorts_using_scans: 使用表扫描语句总数

sort_using_range: 使用范围的访问总数

rows_sorted: 行总数

avg_rows_sorted: 平均每个出现的语句排序

first_seen: 第一次时间

last_seen: 最近时间

digest: 声明

----------------------------------------------------------------------------------------------------------------

| statements_with_temp_tables                  

临时表相关

query: 语句字符串

db: 数据库

exec_count: 执行语句

total_latency: 总等待时间

memory_tmp_tables: 内部l临时表的总数

disk_tmp_tables: 磁盘上的临时表的总数

avg_tmp_tables_per_query: 平均每个出现的临时表

tmp_tables_to_disk_pct: 内部临时表的百分比转换为磁盘临时表

first_seen: 第一次时间

last_seen: 最近时间

digest: 声明

---------------------------------------------------------------------------------------------------------------

| sys_config      

#用于sys schema库的配置

 

-----------------------------------------------------------------------------------------------                              

| user_summary

user: 客户端用户名

statements:  用户总数的语句

 statement_latency: 用户总等待的时间

 statement_avg_latency: 每个时间的平均等待时间

 table_scans:用户的表扫描

file_ios:用户文件i/o总数

 file_io_latency: 用户i/o总等待时间

current_connections: 用户当前连接数

total_connections: 用户的连接总数

unique_hosts: 用户不同主机的连接数

current_memory: 用户当前分配的内存数量

total_memory_allocated: 用户分配内存数量总数

---------------------------------------------------------------------------------------------

| user_summary_by_file_io

user: 客户端用户名

 ios: 用户文件i/o总数

io_latency: 用户文件总等待时间

--------------------------------------------------------------------------------------------------------

| user_summary_by_file_io_type

user: 客户端用户名

event_name: 文件i/o事件名称

total: 用户文件i/o出现总数

latency: 定时出现总等待时间

max_latency: 最大等待时间

--------------------------------------------------------------------------------------------------------------------

| user_summary_by_stages 

user: 客户端用户名

event_name: 文件i/o时间名称

total: 事件总数

total_latency: 总等待时间

 avg_latency:平均等待时间

 

----------------------------------------------------------------------------------------------------------------

| user_summary_by_statement_latency

user: 客户端用户名

total: 为用户总数的语句

total_latency: 总等待时间

max_latency: 最大单一等待时间

lock_latency: 锁等待总时间

rows_sent: 用户通过语句返回的行数

rows_examined: 读取行数为用户存储引擎

rows_affected: 用户影响行数

full_scans: 全表扫描的总数

 

----------------------------------------------------------------------------------------------------------------

| user_summary_by_statement_type

user: 客户端用户名

statement: 最后的语句事件名称

total: 用户出现的总数

total_latency: 用户出现等待时间

max_latency: 用户最大单等待时间

lock_latency: 出现锁等待时间

rows_sent: 返回的行总数

rows_examined: 读取行数 从存储引擎语句发生

rows_affected: 受事件影响的行数

 full_scans: 全表扫描的总行数

 

---------------------------------------------------------------------------------------------------------------- 

| version

 sys_version:sys库版本

mysql_version: mysql版本

 

----------------------------------------------------------------------------------------------------------------

| wait_classes_global_by_avg_latency

event_class: 事件类

total: 总数

total_latency: 总等待时间

min_latency: 最小时间

avg_latency: 平均时间

max_latency: 最大时间

 

----------------------------------------------------------------------------------------------------------------

| wait_classes_global_by_latency

event_class: 事件类

total: 总数

total_latency: 总等待时间

min_latency: 最小时间

avg_latency: 平均时间

max_latency: 最大时间

 

----------------------------------------------------------------------------------------------------------------

| waits_by_host_by_latency

host: 主机名

event_class: 事件类

total: 总数

total_latency: 总等待时间

min_latency: 最小时间

avg_latency: 平均时间

max_latency: 最大时间

 

---------------------------------------------------------------------------------------------------------------- 

| waits_by_user_by_latency

user: 客户端用户名

event_class: 事件类

total: 总数

total_latency: 总等待时间

min_latency: 最小时间

avg_latency: 平均时间

max_latency: 最大时间

 

 

----------------------------------------------------------------------------------------------------------------

| waits_global_by_latency   

event_class: 事件类

total: 总数

total_latency: 总等待时间

min_latency: 最小时间

avg_latency: 平均时间

max_latency: 最大时间

 

----------------------------------------------------------------------------------------------------------------

 

Innodb_buffer_stats_by_table

和innodb_buffer_stats_by_schema基本一致。只是比上面多了个object_name指定表名。

 

1. 谁使用了最多的资源？ 基于IP或是用户？

对于该问题可以从host, user, io三个方面去了解，大概谁的请求最多。对于使用资源问题可以直接从下面四个视图里有一个大概的了解。

   Select*from host_summary limit 1\G

   Select*fromio_global_by_file_by_bytes limit 1\G

   Select*from user_summary limit 1\G

   Select*from memory_global_total;

 

   注意内存部分，不包括innodbbufferpool。只是server 层申请的内存

 

2. 大部分连接来自哪里及发送的SQL情况

查看当前连接情况：

select host, current_connections,statements fromhost_summary;

查看当前正在执行的SQL：

select conn_id, user, current_statement,last_statement from session;

 

3. 机器执行最多的SQL语句是什么样?

例如查一下系统里执行最多的TOP 10 SQL。

SQL如下：

select * from statement_analysis orderbyexec_count desc limit 10\G;

 

4. 哪张表的IO最多？哪张表访问次数最多

select * from io_global_by_file_by_byteslimit10;(参见上面表格说明)

哪张表访问次数最多，可以参考上面先查询执行最多的语句，然后查找对应的表。

SQL如下：

select * from statement_analysis orderbyexec_count desc limit 10\G;

 

5. 哪些语句延迟比较严重

statement_analysis中avg_latency的最高的。(参考上面写法)

SQL语句：

select * from statement_analysis orderbyavg_latency desc limit 10;

 

6. 哪些SQL语句使用了磁盘临时表

利用statement_analysis 中tmp_tables ，tmp_disk_tables 进行计算。(参考上面写法)

参考SQL：

select db, query,tmp_tables,tmp_disk_tables  from statement_analysiswhere tmp_tables>0or tmp_disk_tables >0 order by(tmp_tables+tmp_disk_tables) desc limit 20；

 

7. 哪张表占用了最多的buffer pool

例如查询在buffer pool中占用前10的表。

SQL如下：

select * from innodb_buffer_stats_by_tableorderby pages desc limit 10;

 

8. 每个库占用多少buffer pool

SQL如下：

select * frominnodb_buffer_stats_by_schema;

 

9. 每个连接分配多少内存

利用session表和memory_by_thread_by_current_bytes分配表进行关联查询。

SQL如下：

select b.user, current_count_used,current_allocated,current_avg_alloc, current_max_alloc,total_allocated,current_statement frommemory_by_thread_by_current_bytes a,session b where a.thread_id = b.thd_id;

 

10. MySQL内部现在有多个线程在运行

MySQL内部的线程类型及数量：

select user, count(*) from processlistgroup byuser;
————————————————
版权声明：本文为CSDN博主「jayewu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/jayewu/article/details/80183274
