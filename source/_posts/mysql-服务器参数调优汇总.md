---
title: mysql-服务器参数调优汇总.md
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
title: mysql-服务器参数调优汇总.md
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
######1、innodb_buffer_pool_size，Innodb存储引擎缓存池大小
innodb_buffer_pool_siz是`对于Innodb来说最重要的一个配置`，如果所有的表用的都是Innodb，那么甚至建议将该值设置到物理内存的80%，Innodb的很多性能提升如索引都是依靠这个；

表示缓冲池字节大小， InnoDB 缓存表和索引数据的内存区域。 默认是128MB也就是134217728字节。

如果设定的缓冲池的大小大于 1G，设置 innodb_buffer_pool_instances 的值 > 1，则数据读写在内存中非常快， innodb_buffer_pool_size 减少了对磁盘的读写。 当数据提交或满足检查点条件后才一次性将内存数据刷新到磁盘中。

然而内存还有操作系统或数据库其他进程使用， 一般设置innodb_buffer_pool_size大小为总内存的 3/4 至 4/5。 若设置不当，内存使用可能浪费或者使用过多。 对于繁忙的服务器， innodb_buffer_pool_size将划分为多个实例以提高系统并发性， 减少线程间读写缓存的争用。

设置为1G
~~~
 SET GLOBAL innodb_buffer_pool_size = 1073741824
~~~

> table_open_cache_instances  这个参数也是mysql  5.6 新增的特性。设置多个缓冲池，能将请求分散处理，用以减少线程间表锁争用，这对性能优化有很大提升。建议设置 8-16，在多线程多核心CPU上尤为有效; 当 innodb_buffer_pool_size 设置的 大于 1GB  以后，那么此参数设置就尤为重要了， MySQL 5.6.6开始 此参数默认为 8,   主要目的是为了解决 互斥锁， 每个缓冲池管理其自己的空闲列表,提高查询并发性, 对于互斥锁, 如innodb_buffer_pool_size大于1.3GB，则innodb_buffer_pool_instances的默认值为innodb_buffer_pool_size / 128MB   即大致为 10 左右，每个实例具有独立的缓存区块




######2、max_connections，最大客户端连接数

 show variables like 'max_connections';
 默认 151，在爬虫系统中这个值通常会飙升


######3、table_open_cache，表文件句柄缓存（表数据是存储在磁盘上的，缓存磁盘文件的句柄方便打开文件读取数据）

 show variables like 'table_open_cache';
默认 2000

######4、key_buffer_size，索引缓存大小（将从磁盘上读取的索引缓存到内存，可以设置大一些，有利于快速检索）

show variables like 'key_buffer_size';
默认 8388608




######5、innodb_file_per_table（innodb中，表数据存放在.ibd文件中，如果将该配置项设置为ON，那么一个表对应一个ibd文件，否则所有innodb共享表空间）

show variables like 'innodb_file_per_table';

######6、read_buffer_size 是 MySQL 读入缓冲区大小。
对表进行顺序扫描的请求将分配一个读入缓冲区， MySQL 会为它分配一段内存缓冲区。readbuffersize 变量控制这一缓冲区的大小。如果对表的顺序扫描请求非常频繁，并且你认为频繁扫描进行得太慢，可以通过增加该变量值以及内存缓冲区大小提高其性能
SHOW VARIABLES LIKE 'read_buffer_size'

######7、innodb_read_io_threads和innodb_write_io_threads IO读写线程数

 SHOW VARIABLES LIKE 'innodb_read_io_threads'
 SHOW VARIABLES LIKE 'innodb_write_io_threads'
