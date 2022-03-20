---
title: mysql-索引优化特性之MRR.md
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
title: mysql-索引优化特性之MRR.md
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
https://dev.mysql.com/doc/refman/8.0/en/mrr-optimization.html


> MRR针对于辅助索引上的范围查询进行优化,收集辅助索引对应主键rowid。进行排序后回表查询，随机IO转顺序IO


当我们需要对大表(基于辅助索引)进行范围扫描时,会导致产生许多随机/O。而对于普通磁盘来说,随机的性能很差,会遇到瓶颈,在 MySQL 5.6/5.7和MariaDB5.3/5.5/10.0/10.1版本里对这种情况进行了优化,一个新的名词 Multi Range Read(MRR)出现了,优化器会先扫描辅助索引,然后收集每行的主键（rowid ）,并对主键进行排序（排序结果存储到read_rnd_buffer),此时就可以用主键顺序访问基表,即用顺序IO代替随机IO。

而MRR的优化在于，并不是每次通过辅助索引读取到数据就回表去取记录，范围扫描（range access）中MySQL将扫描到的数据存入由 read_rnd_buffer_size 变量定义的内存大小中，默认256K。然后对其按照Primary Key（RowID）排序，然后使用排序好的数据进行顺序回表，因为我们知道InnoDB中叶子节点数据是按照PRIMARY KEY（ROWID）进行顺序排列的，所以我们可以认为，如果按照主键的递增顺序查询的话，对磁盘的读比较接近顺序读，能够提升读性能。这对于IO-bound类型的SQL查询语句带来性能极大的提升。

MRR 能够提升性能的核心在于，这条查询语句在索引上做的是一个范围查询（也就是说，这是一个多值查询），可以得到足够多的主键id。这样通过排序以后，再去主键索引查数据，才能体现出“顺序性”的优势。所以MRR优化可用于range，ref，eq_ref类型的查询，工作方式如下图：

[![MySQL联接查询算法（NLJ、BNL、BKA、HashJoin）](https://upload-images.jianshu.io/upload_images/13965490-14f698a15350a45e?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)](http://www.ywnds.com/wp-content/uploads/2016/12/2016120912190540.png) 



>简单说：使用辅助索引进行范围查询时，MRR会收集并排序好符合范围查询条件的rowid。然后通过顺序的rowid去回表查询数据记录。 MRR 通过把「随机磁盘读」，转化为「顺序磁盘读」，从而提高了索引查询的性能。


###mysql中mrr相关操作

mysql默认开启MRR优化。但是由优化器决定是否真正使用MRR（mrr=on,mrr_cost_based=on），因为有些时候优化器认为不使用MRR性能会更好！查询MRR的开启状态如下：
~~~
SHOW VARIABLES LIKE '%optimizer_switch%'
~~~
>index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,`mrr=on,mrr_cost_based=on`,block_nested_loop=off,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on



关闭MRR优化，不强制使用MRR
~~~
 set optimizer_switch='mrr=off,mrr_cost_based=on';
~~~

k_1是sbtest1 表的一个辅助索引，执行计划如下：
~~~
EXPLAIN SELECT * from sbtest1 force index(k_1)  where k BETWEEN 1000 and 55555
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-55d46199255a63ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-d36ac4c22c8ce5df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


再来看开启MRR，并强制使用。可以看到执行计划的Extra列多了Using MRR
~~~
 set optimizer_switch='mrr=on,mrr_cost_based=off';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a68d6597d41d2895.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f2383d6d6898db5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


mrr=on会开启MRR优化功能，mrr_cost_based 则是用来告诉优化器，要不要基于使用 MRR 的成本，考虑使用 MRR 是否值得（cost-based choice），来决定具体的 sql 语句里要不要使用 MRR。很明显，对于只返回一行数据的查询，是没有必要 MRR 的，而如果你把 mrr_cost_based 设为 off，那优化器就会通通使用 MRR。`建议这个配置还是设为 on`，毕竟优化器在绝大多数情况下都是正确的。另外还有一个配置 read_rnd_buffer_size ，是用来设置用于给 rowid 排序的内存的大小。显然，MRR 在本质上是一种用`空间换时间的算法`。MySQL 不可能给你无限的内存来进行排序，如果 read_rnd_buffer 满了，就会先把满了的 rowid 排好序去磁盘读取，接着清空，然后再往里面继续放 rowid，直到 read_rnd_buffer 又达到 read_rnd_buffe 配置的上限，如此循环。

>另外 MySQL 的其中一个分支 Mariadb 对 MySQL 的 MRR 做了很多优化。

~~~
SHOW VARIABLES LIKE '%read_rnd_buffer%' -- 262144 字节 0.25M
~~~


>注意：MRR 只是针对优化回表查询的速度，当不需要回表访问的时候，MRR就失去意义了（比如覆盖索引）



optimizer_switch可以是全局的，也可以是会话级的。当然，除了调整参数外，数据库也提供了语句级别的开启或关闭MRR，使用方法如下：
~~~
EXPLAIN SELECT /*+ MRR(sbtest1)*/ *  from sbtest1 force index(k_1)  where k BETWEEN 1000 and 55555
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ad5d510d1a8b8435.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###什么时候使用MRR
- 基于辅助索引的范围查询
- 由于select查询的字段过多，无法做到索引覆盖

想普通的分页查询，在where条件中有基于时间的范围查询。这个是使用mrr的

###MRR优化


read_rnd_buffer_size参数

Command-Line Format	--read-rnd-buffer-size=#
System Variable	read_rnd_buffer_size
Scope	Global, Session
Dynamic	Yes
SET_VAR Hint Applies	Yes
Type	Integer
Default Value	262144
Minimum Value	1
Maximum Value	2147483647
This variable is used for reads from MyISAM tables, and, for any storage engine, for Multi-Range Read optimization.

When reading rows from a MyISAM table in sorted order following a key-sorting operation, the rows are read through this buffer to avoid disk seeks. See Section 8.2.1.16, “ORDER BY Optimization”. Setting the variable to a large value can improve ORDER BY performance by a lot. However, this is a buffer allocated for each client, so you should not set the global variable to a large value. Instead, change the session variable only from within those clients that need to run large queries.

read_rnd_buffer_size提高mrr的排序冲区，是会话级别的。不应该调非常大；
