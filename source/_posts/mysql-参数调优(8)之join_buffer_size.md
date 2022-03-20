---
title: mysql-参数调优(8)之join_buffer_size.md
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
title: mysql-参数调优(8)之join_buffer_size.md
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


当无法保证被驱动表的 Join 条件字段被索引且内存资源充足的前提下，不要太吝惜 Join
Buffer 的设置；当在某些特殊的环境中，我们的 Join 必须是 All， Index， range或者是 index_merge类型的
时候， Join Buffer就会派上用场了。在这种情况下， Join Buffer的大小将对整个 Join 语句的消
耗起到非常关键的作用

###join buffer
Join Buffer 可被用于联接是ALL、index、和range的类型;每次联接使用一个Join Buffer，因此多表的联接可以使用多个Join Buffer；Join Buffer在联接发生之前进行分配，在SQL语句执行完后进行释放；Join Buffer只存储要进行查询操作的相关列数据，而不是整行的记录。

1、Using join buffer (Block Nested Loop) mysql5.7
join buffer 使用在 BNLJ中
我们可以增加join buffer的值来优化join查询，因为增加的join buffer可以容纳下更多的外表join字段记录。这样就可以批让内部表批量的匹配更多个外部表字段，相对来说就减少了匹配次数，提高了join查询效率。


2、Using join buffer (hash join) mysql 8.0
join buffer使用在 HASH JOIN中，用作缓存外表的关联字段hash值



###调整Join_buffer_size变量

####1、配置默认值
推荐设置：16M

系统默认大小为：512k，mac下默认大小为：256k，针对128GB，1万并发的mysql我推荐给到的值为：8~16M。对于JOIN KEY 有索引和二级索引，JOIN KEY 无索引mysql会使用到join_buffer_size，一般建议设置一个很小的 GLOBAL 值，完了在 SESSION 或者 QUERY 的基础上来做一个合适的调整。适当的去改变它确实可以带来一定的提速，但并不是说很多值越大越好，为什么我们设置成4m呢？我们假设我们的mysql所在的vm是128gb，一根这样的join（如果被用到）是4M，1万个也不过用掉40G,而根据官方说法，total加在一起产生的join_buffer_size不要超过你所在系统的50%.默认512k肯定是小了点，我们可以适当放宽，比如说：2M，在实际使用场景时我们发觉有这样的高频操作（要看高频出现的有意义的sql的执行计划，并确认该计划的：执行cost如："query_cost": "1003179606.87"，它产生的cost为：0.93个G,如果它真的很高频出现在调优sql到无法调优的程度，我们会去做set session join_buffer_size = 1024 * 1024 * 1024;这样的操作。而不是在一开始的my.cnf中去分配一个暴大的值，我们这边基于128gb，1万connection的并发来说，你给个16M不算小也不算多，我推荐给到8~16M间（这是指在一开始）。

如果不配的后果：默认的为256k

配置实例：
~~~
[mysqld]
join_buffer_size = 16M
~~~



####2、配置语句或会话级别的值
变量join_buffer_size用来控制Join Buffer的大小，调大后可以避免多次的内表扫描，从而提高性能。也就是说，当MySQL的Join有使用到Block Nested-Loop Join，那么调大变量join_buffer_size才是有意义的。而前面的Index Nested-Loop Join如果仅使用索引进行Join，那么调大这个变量则毫无意义。变量join_buffer_size的默认值是256K，显然对于稍复杂的SQL是不够用的。好在这个是会话级别的变量，可以在执行前进行扩展。建议在会话级别进行设置，而不是全局设置，因为很难给一个通用值去衡量。另外，这个内存是会话级别分配的，如果设置不好容易导致因无法分配内存而导致的宕机问题。

一般建议设置一个很小的 GLOBAL 值，完了在 SESSION 或者 QUERY 的基础上来做一个合适的调整。比如 默认的值为 512K， 想要临时调整为 1G应该如下操作：
~~~
set session join_buffer_size = 1024 * 1024 * 1024; 
select * from ...;	
set session join_buffer_size=default;	
或者
mysql>select /*+  set_var(join_buffer_size=1G) */ * from ...;

~~~


~~~
SHOW VARIABLES LIKE '%join_buffer_size%'  --默认262144(0.25M)
~~~

###关于调整Join_buffer_size的测试

通过我的测试join_buffer_size参数对hash join查询性能的帮助比较少。一帮默认的0.25M就够用了。我的实验中user表640000条数据，book 762474条数据。进行left join 查询：
~~~
EXPLAIN SELECT *  FROM `user` a LEFT JOIN book  b IGNORE index(index_user_id)  ON a.id=b.user_id; 
~~~
user.id 是bigint类型的，那就是640000*8 字节 4.8MB超过了0.25MB 。实验结果是如下，每次查询都是重启数据库的，防止缓存影响。
join_buffer_size = 1 字节，13秒
join_buffer_size = 0.25M 默认 6.3秒
join_buffer_size = 1G   5.7秒

>join_buffer_size设置过小会让hash join变慢很多，但是设置过大也没多大性能提升！同时我还做了使用索引的INLJ 关联查询对比，第一次查询竟然耗费了33秒的时间，没重启mysql查询第二次变成了8秒。看来这种时候HASH JOIN的性能要优于通过索引的BNLJ，mysql8还是相当给力的！


###Join Buffer缓存对象有哪些？
> join buffer 缓存外表的在sql查询中设计的字段

另外，Join Buffer缓存的对象是什么，这个问题相当关键和重要。然在MySQL的官方手册中是这样记录的：Only columns of interest to the join are stored in the join buffer, not whole rows.

可以发现Join Buffer不是缓存外表的整行记录，而是缓存“columns of interest”，具体指所有参与查询的列都会保存到Join Buffer，而不是只有Join的列。比如下面的SQL语句，假设没有索引，需要使用到Join Buffer进行链接：
~~~
SELECT a.col3
FROM a,
     b
WHERE a.col1 = b.col2
  AND a.col2 > ….
  AND b.col2 = …
~~~
假设上述SQL语句的外表是a，内表是b，那么存放在Join Buffer中的列是所有参与查询的列，在这里就是（a.col1，a.col2，a.col3）。

>通过上面的介绍，我们现在可以得到内表的扫描次数为：Scaninner_table = (RN * used_column_size) / join_buffer_size + 1

对于有经验的DBA就可以预估需要分配的Join Buffer大小，然后尽量使得内表的扫描次数尽可能的少，最优的情况是只扫描内表一次。
