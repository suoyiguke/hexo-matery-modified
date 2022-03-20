---
title: mysql-查询缓存-query_cache.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-查询缓存-query_cache.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
###mysql开启查询缓存

在`[mysqld]`段中配置`query_cache_type`：

~~~
[mysqld]
query_cache_type = 2
~~~
-   0：不开启
-   1：开启，默认缓存所有，需要在SQL语句中增加`select sql-no-cache`提示来放弃缓存
-   2：开启，默认都不缓存，需要在SQL语句中增加`select sql-cache`来主动缓存（`常用`）


更改配置后需要重启以使配置生效，重启后可通过show variables来查看，显示DEMAND就是已开启

~~~
show variables like 'query_cache_type';
query_cache_type	DEMAND
~~~

##在客户端设置缓存大小

通过配置项`query_cache_size`来设置：
mysql5.7默认query_cache_size为 1048576 字节 也就是1M
~~~
show variables like 'query_cache_size';
query_cache_size	1048576
~~~

将查询缓存的大小设置为 64M
~~~
set global query_cache_size=64*1024*1024;
show variables like 'query_cache_size';
query_cache_size	67108864
~~~

也可以修改配置文件，重启自动生效
~~~
[mysqld]
query_cache_type = 2
query_cache_size = 67108864
~~~

######查询缓存使用示例，将查询结果缓存
~~~
select sql_cache * from user;
~~~
######整理缓存和重置缓存
可以使用下列语句来清理查询缓存碎片以提高内存使用性能。该语句不从缓存中移出任何查询。
~~~
FLUSH QUERY CACHE;
~~~

从查询缓存中移出所有查询。FLUSH TABLES语句也执行同样的工作。
~~~
reset query cache;
FLUSH TABLES;
~~~






###注意事项

1.  应用程序，不应该关心`query cache`的使用情况。可以尝试使用，但不能由`query cache`决定业务逻辑，因为`query cache`由DBA来管理。
2.  缓存是以SQL语句为key存储的，因此即使SQL语句功能相同，但如果多了一个空格或者大小写有差异都会导致匹配不到缓存。



###查询缓存配置参数总结
~~~
show variables like 'query_cache%';
~~~
`query_cache_limit`
（单位：byte）：查询缓存中可存放的单条查询最大结果集，默认为 1 MB；超过该大小的结果集不被缓存。
`query_cache_min_res_unit`	
4.1版本以后引入的，它指定分配缓冲区空间的最小单位，缺省为4K。检查状态值Qcache_free_blocks，如果该值非常大，则表明缓冲区中碎片很多，这就表明查询结果都比较小，此时需要减小 query_cache_min_res_unit。

`query_cache_size`
设置缓存大小，单位字节。缺省1M
`query_cache_type`	
查询缓存开启情况。缺省 OFF 不开启；
`query_cache_wlock_invalidate`	
  如果某个数据表被其他的连接锁住，是否仍然从查询缓存中返回结果。缺省OFF

###查询缓存性能监控参数
~~~
show status like '%Qcache%';
~~~

`Qcache_free_blocks`
缓存中相邻内存块的个数。数目大说明可能有碎片。
`Qcache_free_memory`   
 缓存中的空闲内存
`Qcache_hits`	
每次查询在缓存中命中时就增大。
`Qcache_inserts`	
将查询和结果集写入到查询缓存中的次数。
`Qcache_lowmem_prunes	`
 缓存出现内存不足并且必须要进行清理以便为更多查询提供空 间的次数。这个数字最好长时间来看；如果这个数字在不断增长，就 表示可能碎片非常严重，或者内存很少。（上面的 free_blocks 和 free_memory 可以告诉您属于哪种情况）。
`Qcache_not_cached`
不可以缓存的查询次数。
`Qcache_queries_in_cache`
 查询缓存中缓存的查询量。
`Qcache_total_blocks`
缓存中块的数量。



###查询缓存在这些情况下不会生效
1、查询必须严格一致（大小写、空格、使用的数据库、协议版本、字符集等必须一致）才可以命中，否则视为不同查询。
2、不缓存查询中的子查询结果集，仅缓存查询最终结果集。
3、不缓存存储函数（Stored Function）、存储过程（Stored Procedure）、触发器（Trigger）、事件（Event）中的查询。
4、不缓存含有每次执行结果变化的函数的查询，比如now()、curdate()、last_insert_id()、rand()等。
5、不缓存对mysql、information_schema、performance_schema系统数据库表的查询。
6、不缓存使用临时表的查询。
7、不缓存产生告警（Warnings）的查询。
8、不缓存Select … lock in share mode、Select … for update、 Select * from … where autoincrement_col is NULL类型的查询。
9、不缓存使用用户定义变量的查询。
10、不缓存使用Hint - SQL_NO_CACHE的查询。
11、分区表不能使用查询缓存

###数据变更导致的缓存失效问题

当数据表改动时，基于该数据表的任何缓存都会被删除。（表层面的管理，不是记录层面的管理，因此失效率较高）；
这里`数据表更改`包括:  INSERT, UPDATE, DELETE, TRUNCATE, ALTER TABLE, DROP TABLE, or DROP DATABASE等。

>举个例子，如果数据表posts访问频繁，那么意味着它的很多数据会被QC缓存起来，但是每一次posts数据表的更新，无论更新是不是影响到了cache的数据，都会将全部和posts表相关的cache清除。如果你的数据表更新频繁的话，那么Query Cache将会成为系统的负担。有实验表明，糟糕时，QC会降低系统13%[1]的处理能力。

###功能和适用范围

1、功能：
降低CPU使用率。
降低IOPS使用率（某些情况下）。
减少查询响应时间，提高系统的吞吐量。
适用范围：

2、表数据修改不频繁、数据较静态。
查询（Select）重复度高。
查询结果集小于 1 MB。
说明 查询缓存并不一定带来性能上的提升，在某些情况下（比如查询数量大，但重复的查询很少）开启查询缓存会带来性能的下降。

>官方在特定环境测试结果（官方文档中有详细说明）：
1、如果对某表进行简单查询，但每次查询条件都不一样时，打开查询缓存会导致性能下降13%。
2、如对一个只有一行数据的表进行查询，则可以提升238%。

所以查询缓存特别适用于更新频率非常低、查询频率非常高的场景。




>query_cache在mysql8.0时被移除4
