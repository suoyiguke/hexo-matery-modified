---
title: mysql-联接查询算法之Block-Nested-Loop-Join（BNL）-二.md
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
title: mysql-联接查询算法之Block-Nested-Loop-Join（BNL）-二.md
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
>Block Nested-Loop Join：BNLJ，缓存块嵌套循环连接; 


扫描一个表的过程其实是先把这个表从磁盘上加载到内存中，然后从内存中比较匹配条件是否满足。但内存里可能并不能完全存放的下表中所有的记录，所以在扫描表前边记录的时候后边的记录可能还在磁盘上，等扫描到后边记录的时候可能内存不足，所以需要把前边的记录从内存中释放掉。我们前边又说过，采用SNLJ 算法的两表联接过程中，`被驱动表可是要被访问好多次的`。被驱动表具体的访问次数就是由驱动表返回结果集记录数决定！如果这个被驱动表中的数据特别多而且不能使用索引进行访问，那就相当于要从磁盘上读好几次这个表，这个I/O代价就非常大了，所以我们得想办法：
>尽量减少访问被驱动表的次数。 可以让被驱动表尽量的小（小表驱动大表思想！）

当被驱动表中的数据非常多时，每次访问被驱动表，被驱动表的记录会被加载到内存中，在内存中的每一条记录只会和驱动表结果集的一条记录做匹配，之后就会被从内存中清除掉。然后再从驱动表结果集中拿出另一条记录，再一次把被驱动表的记录加载到内存中一遍，周而复始，驱动表结果集中有多少条记录，就得把被驱动表从磁盘上加载到内存中多少次。

>所以我们可不可以在把被驱动表的记录加载到内存的时候，一次性和多条驱动表中的记录做匹配，`这样就可以大大减少重复从磁盘上加载被驱动表的代价了`。这也就是Block Nested-Loop Join算法的思想。


也就是说在有索引的情况下，MySQL会尝试去使用Index Nested-Loop Join算法，在有些情况下，可能Join的列就是没有索引，那么这时MySQL的选择绝对不会是最先介绍的Simple Nested-Loop Join算法，SNLJ算法是最慢的join，毕竟是笛卡尔积！

而Block Nested-Loop Join算法较Simple Nested-Loop Join的改进就在于可以减少内表的扫描次数，甚至可以和Hash Join算法一样，仅需扫描内表一次。其使用Join Buffer（联接缓冲）来减少内部循环读取表的次数。
关于 join buffer https://www.jianshu.com/p/3c0816862cc9
~~~
For each tuple r in R do                             -- 扫描外表R
    store used columns as p from R in Join Buffer    -- 将部分或者全部R的记录保存到Join Buffer中，记为p
    For each tuple s in S do                         -- 扫描内表S
        If p and s satisfy the join condition        -- p与s满足join条件
            Then output the tuple                    -- 返回为结果集
~~~
可以看到相比Simple Nested-Loop Join算法，Block Nested-LoopJoin算法仅多了一个所谓的Join Buffer，为什么这样就能减少内表的扫描次数呢？下图相比更好地解释了Block Nested-Loop Join算法的运行过程：
![image](https://upload-images.jianshu.io/upload_images/13965490-3ef4817e146fb618?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看到Join Buffer用以缓存联接需要的列（所以再次提醒我们，最好不要把*作为查询列表，只需要把我们关心的列放到查询列表就好了，这样还可以在join buffer中放置更多的记录呢），然后以Join Buffer批量的形式和内表中的数据进行联接比较。就上图来看，记录r1，r2 … rT的联接仅需扫内表一次，如果join buffer可以缓存所有的外表列，那么联接仅需扫描内外表各一次，从而大幅提升Join的性能。
Block Nested-Loop Join开销

Block Nested-Loop Join极大的避免了内表的扫描次数，如果Join Buffer可以缓存外表的数据，那么内表的扫描仅需一次，这和Hash Join非常类似。但是Block Nested-Loop Join依然没有解决的是Join比较的次数，其仍然通过Join判断式进行比较。综上所述，到目前为止各Join算法的成本比较如下所示：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-72a092f01cf03a99.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



**Block Nested-Loop Join影响**

在使用 Block Nested-Loop Join(BNL) 算法时，还是可能会对被驱动表做多次扫描（尽管可能已经将驱动表中大部分关联字段数据存入join buffer）。如果这个被驱动表是一个大的冷数据表，除了会导致 IO 压力大以外，还会对 buffer pool产生严重的影响！

如果了解 InnoDB 的 LRU 算法就会知道，由于 InnoDB 对 Bufffer Pool 的 LRU 算法做了优化，即：第一次从磁盘读入内存的数据页，会先放在 old 区域。如果 1 秒之后这个数据页不再被访问了，就不会被移动到 LRU 链表头部，这样对 Buffer Pool 的命中率影响就不大。

但是，如果一个使用 BNL 算法的 join 语句，多次扫描一个冷表，而且这个语句执行时间超过 1 秒，就会在再次扫描冷表的时候，把冷表的数据页移到 LRU 链表头部。这种情况对应的，是冷表的数据量小于整个 Buffer Pool 的 3/8，能够完全放入 old 区域的情况。如果这个冷表很大，就会出现另外一种情况：业务正常访问的数据页，没有机会进入 young 区域。(导致正常业务sql查询因为没有剩余buffer pool空间进一步让磁盘IO变多而变得缓慢)

由于优化机制的存在，一个正常访问的数据页，要进入 young 区域，需要隔 1 秒后再次被访问到。但是，由于我们的 join 语句在循环读磁盘和淘汰内存页，进入 old 区域的数据页，很可能在 1 秒之内就被淘汰了。这样，就会导致这个 MySQL 实例的 Buffer Pool 在这段时间内，young 区域的数据页没有被合理地淘汰。

也就是说，这两种情况都会影响 Buffer Pool 的正常运作。 大表 join 操作虽然对 IO 有影响，但是在语句执行结束后，对 IO 的影响也就结束了。但是，对 Buffer Pool 的影响就是持续性的，需要依靠后续的查询请求慢慢恢复内存命中率。

为了减少这种影响，你可以考虑增大 join_buffer_size 的值，减少对被驱动表的扫描次数!
也就是说，BNL 算法对系统的影响主要包括三个方面： 可能会多次扫描被驱动表，占用磁盘 IO 资源； 判断 join 条件需要执行 M*N 次对比（M、N 分别是两张表的行数），如果是大表就会占用非常多的 CPU 资源； 可能会导致 Buffer Pool 的热数据被淘汰，影响内存命中率。

那么假设被驱动表全在内存中，这个时候 SNLJ 和 BNL 算法还有性能差别吗？当然是有的，由于 SNLJ 这个算法天然会对被驱动表的数据做多次访问，所以更容易将这些数据页放到 Buffer Pool 的头部，从而污染 Buffer Pool。另外，即使被驱动表数据都在内存中，但每次查找“下一个记录的操作”，都是类似指针操作。而 BNL 算法中的 join_buffer 是数组，遍历的成本更低，从被驱动表读取一条数据去 join_buffer 中遍历。



**BNL的相关设置**
mysql默认开启BNL
~~~
SHOW VARIABLES LIKE '%optimizer_switch%'
~~~
>index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,`block_nested_loop=on`,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on

开关BNL
~~~
SET optimizer_switch = 'block_nested_loop=on'; 
SET optimizer_switch = 'block_nested_loop=off'; 
~~~


###总结下

1、 缓存块嵌套循环连接通过一次性缓存多条数据，把参与查询的列缓存到Join Buffer 里，然后拿join buffer里的数据批量与内层表的数据进行匹配，从而减少了内层循环的次数、减少了内部表访问次数（遍历一次内层表就可以批量匹配一次Join Buffer里面的外层表数据）。
2、什么时候会使用BNL?  当内表关联字段上没有索引时，不使用Index Nested-Loop Join的时候，默认使用Block Nested-Loop Join。
3、join buffer的相关概念：
待续。。。。。
4、使用Block Nested-Loop Join算法需要开启优化器管理配置的optimizer_switch的设置block_nested_loop为on，默认为开启。



###BNLJ和SNLJ区别
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b52cb792e29e8535.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





###join buffer size 最大调1G

