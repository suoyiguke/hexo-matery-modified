---
title: mysql-联接查询算法之Batched-key-access-(BKA)-四.md
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
title: mysql-联接查询算法之Batched-key-access-(BKA)-四.md
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
Batched key access (BKA)

>BKA算法集结了 INLJ、BNLJ、MRR 算法的特性。它用到了INLJ的内部表索引减少关联匹配的次数；又使用到了BNLJ的join buffer，用以暂存外表连接数据减少访问内部表；还用到了MRR的收集主键rowid后排序再回表查询，随机IO转顺序IO；可以把BKA看做是INLJ算法的加强版！


我们知道INLJ使用内部表索引进行关联能够大幅提升查询效率，但是当查询中涉及到其它字段时需要回表查询。通过辅助索引进行联接后需要回表，这里需要大量的随机I/O操作。若能优化随机I/O，那么就能极大的提升Join的性能。为此，MySQL 5.6（MariaDB 5.3）开始支持Batched Key Access Join算法（简称BKA），该算法通过常见的空间换时间，随机I/O转顺序I/O，以此来极大的提升Join的性能。

在说明Batched Key Access Join前，首先介绍下MySQL 5.6的新特性mrr——multi range read。
这篇有对MRR进行说明 https://www.jianshu.com/p/3d9b9b4ea186


理解了 MRR 性能提升的原理，我们就能理解 MySQL 在 5.6 版本后开始引入的 Batched Key Acess(BKA) 算法了。我们知道 INLJ 算法执行的逻辑是：从驱动表一行行地取出 join 条件值，再到被驱动表去做 join。也就是说，对于被驱动表来说，每次都是匹配一个值。这时，MRR 的优势就用不上了。那怎么才能一次性地多传些值给被驱动表呢？方法就是，从驱动表里一次性地多拿些行出来，一起传给被驱动表。既然如此，我们就把驱动表的数据取出来一部分，先放到一个临时内存。这个临时内存不是别人，就是 join_buffer。

我们知道 join_buffer 在 BNL 算法里的作用，是暂存驱动表的数据。但是在 NLJ 算法里并没有用。那么，我们刚好就可以复用 join_buffer 到 BKA 算法中。NLJ 算法优化后的 BKA 算法的流程，整个过程如下所示：

[![MySQL联接查询算法（NLJ、BNL、BKA、HashJoin）](https://upload-images.jianshu.io/upload_images/13965490-95180c75716738f8?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)](http://www.ywnds.com/wp-content/uploads/2018/07/2018080202505519.jpg) 

>外表-->外表join buffer --> 内表index-->收集主键进行排序（mrr）--> 内表



对于多表join语句，当MySQL使用索引访问第二个join表的时候，使用一个join buffer来收集第一个操作对象生成的相关列值。BKA构建好key后，批量传给引擎层做索引查找。key是通过MRR接口提交给引擎的，这样，MRR使得查询更有效率。

如果外部表扫描的是主键，那么表中的记录访问都是比较有序的，但是如果联接的列是非主键索引，那么对于表中记录的访问可能就是非常离散的。因此对于非主键索引的联接，Batched Key Access Join算法将能极大提高SQL的执行效率。BKA算法支持内联接，外联接和半联接操作，包括嵌套外联接。

>Batched Key Access Join算法的工作步骤如下：
1、 将外部表中相关的列放入Join Buffer中。
2、
3、批量的将Key（索引键值）发送到Multi-Range Read（MRR）接口。
4、Multi-Range Read（MRR）通过收到的Key，根据其对应的ROWID进行排序，然后再进行数据的读取操作（随机IO转顺序IO）。
5、返回结果集给客户端。




在MySQL 5.6中默认关闭BKA（MySQL 5.7默认打开），必须将optimizer_switch系统变量的batched_key_access标志设置为on。BKA使用MRR，因此mrr标志也必须打开。目前，MRR的成本估算过于悲观。因此，mrr_cost_based也必须关闭才能使用BKA。
~~~
SHOW VARIABLES LIKE '%optimizer_switch%'
~~~
>index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,`batched_key_access=off`,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on

以下设置启用BKA：

~~~
SET optimizer_switch='mrr=on,mrr_cost_based=off,batched_key_access=on';
~~~

官方给出的BKA和MRR性能基准测试
![image.png](https://upload-images.jianshu.io/upload_images/13965490-38be9c4a25d9ac60.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###如何确保使用到BKA并达到了优化目的？

Batched Key Access Join算法的本质上来说还是Simple Nested-Loops Join算法，**其发生的条件为内部表上有索引，并且该索引为非主键，并且联接需要访问内部表主键上的索引**。这时Batched Key Access Join算法会调用Multi-Range Read（MRR）接口，批量的进行索引键的匹配和主键索引上获取数据的操作，以此来提高联接的执行效率，因为读取数据是以顺序磁盘IO而不是随机磁盘IO进行的。

因为BKA算法的本质是通过MRR接口将非主键索引对于记录的访问，转化为根据ROWID排序的较为有序的记录获取，所以要想通过BKA算法来提高性能，不但需要确保联接的列参与match的操作（联接的列可以是唯一索引或者普通索引，但不能是主键），还要有对非主键列的search操作。例如下列SQL语句：
~~~
explain select a.gender, b.dept_no from employees a, dept_emp b where a.birth_date=b.from_date;
+----+-------------+-------+------------+------+----------------+----------------+---------+-----------------------+--------+----------+----------------------------------------+
| id | select_type | table | partitions | type | possible_keys  | key            | key_len | ref                   | rows   | filtered | Extra                                  |
+----+-------------+-------+------------+------+----------------+----------------+---------+-----------------------+--------+----------+----------------------------------------+
|  1 | SIMPLE      | b     | NULL       | ALL  | NULL           | NULL           | NULL    | NULL                  | 331570 |   100.00 | NULL                                   |
|  1 | SIMPLE      | a     | NULL       | ref  | idx_birth_date | idx_birth_date | 3       | employees.b.from_date |     62 |   100.00 | Using join buffer (Batched Key Access) |
+----+-------------+-------+------------+------+----------------+----------------+---------+-----------------------+--------+----------+----------------------------------------+
2 rows in set, 1 warning (0.00 sec)
~~~
列a.gender是表employees的数据，但不是通过搜索idx_birth_date索引就能得到数据，还需要回表访问主键来获取数据。因此这时可以使用BKA算法。但是如果联接不涉及针对主键进一步获取数据，内部表只参与联接判断，那么就不会启用BKA算法，因为没有必要去调用MRR接口。比如search的主键（a.emp_no），那么肯定就不需要BKA算法了，直接覆盖索引就可以返回数据了（二级索引有主键值）。
~~~
explain select a.emp_no, b.dept_no from employees a, dept_emp b where a.birth_date=b.from_date;
+----+-------------+-------+------------+------+----------------+----------------+---------+-----------------------+--------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys  | key            | key_len | ref                   | rows   | filtered | Extra       |
+----+-------------+-------+------------+------+----------------+----------------+---------+-----------------------+--------+----------+-------------+
|  1 | SIMPLE      | b     | NULL       | ALL  | NULL           | NULL           | NULL    | NULL                  | 331570 |   100.00 | NULL        |
|  1 | SIMPLE      | a     | NULL       | ref  | idx_birth_date | idx_birth_date | 3       | employees.b.from_date |     62 |   100.00 | Using index |
+----+-------------+-------+------------+------+----------------+----------------+---------+-----------------------+--------+----------+-------------+
2 rows in set, 1 warning (0.00 sec)
~~~

在EXPLAIN输出中，当Extra值包含Using join buffer（Batched Key Access）且类型值为ref或eq_ref时，表示使用BKA。


####什么样的场景适合使用BKA join？
加了辅助索引的字段所在表作为join的内表，索引无法覆盖，select需要回表

###使用hint

~~~
mysql> EXPLAIN  SELECT /*+ BKA(b)*/ 
	a.gender,
	b.* 
FROM
	employees a,
	dept_emp b 
WHERE
	a.birth_date = b.from_date;
+----+-------------+-------+------------+------+-----------------------+-----------------------+---------+------------------------+--------+----------+----------------------------------------+
| id | select_type | table | partitions | type | possible_keys         | key                   | key_len | ref                    | rows   | filtered | Extra                                  |
+----+-------------+-------+------------+------+-----------------------+-----------------------+---------+------------------------+--------+----------+----------------------------------------+
|  1 | SIMPLE      | a     | NULL       | ALL  | NULL                  | NULL                  | NULL    | NULL                   | 300043 |   100.00 | NULL                                   |
|  1 | SIMPLE      | b     | NULL       | ref  | `from_date`,`dept_no` | `from_date`,`dept_no` | 3       | employees.a.birth_date |     47 |   100.00 | Using join buffer (Batched Key Access) |
+----+-------------+-------+------------+------+-----------------------+-----------------------+---------+------------------------+--------+----------+----------------------------------------+
2 rows in set (0.03 sec)

~~~
