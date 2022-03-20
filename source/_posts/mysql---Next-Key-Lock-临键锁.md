---
title: mysql---Next-Key-Lock-临键锁.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql---Next-Key-Lock-临键锁.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
###InnoDB的三种行锁算法介绍
 InnoDB存储引擎有3种行锁的算法,其分别是: 

**1、Record Lock**
单个行记录上的锁
Record Lock  InnoDB总是会去锁住索引记录,如果存储引擎表在建立的时候没有设置任何一个索引,那么这时 InnoDB存储擎会使用隐式的主键来进行锁定。

**2、Gap Lock**
间隙锁,锁定一个范围；我对GAP的认识一直有误解，之前以为只是会出现在 where 范围条件的时候

来看一个删除不存在的记录造成的GAP:
DELETE不存在的记录 + insert ;之间也会出现GAP锁；
test表中只存在1，5 这两条数据；
sessionA执行BEGIN;DELETE FROM test WHERE id =3;
sessionB执行 BEGIN;INSERT INTO test(id) VALUES (2);

阻塞，查看下
~~~
SELECT * from information_schema.INNODB_LOCKS
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3f18314082f9f9c3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看出，当删除的记录不存在时，GAP锁的范围会比较大，很容易造成锁等待。如果表中在id=1与id=5之间还存在值，则会将锁定的范围减小，但是如果删除的记录比id=5 这条记录大，则锁定的范围将是(5,+∞) 这个时候这个表上普通的insert都会阻塞了。


GAP 只在RR级别下存在，有些MYSQL书籍提到为了避免GAP的危害，建议直接将隔离级别设为RC.

**3、Next -Key- Lock =  Gap Lock+Record Lock**

锁定一个范围,并且锁定记录本身。Next- -Key Lock 是结合了 Gap Lock 和 Record Lock 的一种锁定算法,在Next-key Lock算法下, InnoDB对于行的查询都是采用这种锁定算法。例如一个索引有10,11, 13和20这四个值,那么该索引可能被Next--Key Locking的区间（左闭右开）为: 
(-∞,10]
(10,11]
(11,13]
(13,20]
(20+∞) 

采用Next- Key Lock的锁定技术称为 Next-Key Locking.其设计的目的是为了解 决 Phantom Problem（幻影读）,这将在下一小节中介绍。而利用这种锁定技术,锁定的不是单个值,而是一个范围,是谓词锁(predict)的一种改进。

除了next- -key locking,还 有 `previous-key- locking` 技术。同样上述的索引10、11、13和20,若采用 previous--key locking 技术,那么可锁定的区间（左开右闭）为:
 (-∞,10)
 [10,11) 
[11,13)
[13,20)
[20,+∞)
>Next-key Lock算法锁定区间左闭右开， previous-key- locking算法锁定区间左开右闭

若事务T1已经通过next- -key locking锁定了如下范围: (10,11]、(11,13], 当插入新的记录12时,则锁定的范围会变成: (10,11]、(11,12]、(12,13]

###next--key locking的优化
当查询的索引含有唯一属性时, InnoDB存储引擎会对Next- -Key Lock进行优化,将其降级为 Record Lock,即仅锁住索引本身,而不是范围。

看下面的例子,首先根 据如下代码创建测试表t:
~~~
DROP TABLE IF EXISTS t; 
CREATE TABLE t ( a INT PRIMARY KEY )
INSERT INTO t SELECT 1; 
INSERT INTO t SELECT 2; 
INSERT INTO t SELECT 5; 
~~~

接着执行表 6-12中的SQL语句。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-21ee6eb1e105ec23.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
表t共有1、2、5三个值。在上面的例子中,在会话A中首先对a=5进行X锁定。 而由于a是主键且唯一,因此锁定的仅是5这个值,而不是(2,5)这个范围,这样在会 话B中插入值4而不会阻塞,可以立即插入并返回。即锁定由Next- -Key Lock算法降级为了 Record Lock,从而提高应用的并发性。 

>正如前面所介绍的,Next- Key Lock降级为 Record Lock仅在查询的列是唯一索引的 情况若是辅助索引则情况会完全不同。

同样,首先根据如下代码创建测试表z:
~~~
CREATE TABLE z (
  `a` int(11) NOT NULL,
  `b` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`a`) USING BTREE,
  INDEX `b`(`b`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
INSERT INTO `z`(`a`, `b`) VALUES (1, 1);
INSERT INTO `z`(`a`, `b`) VALUES (3, 1);
INSERT INTO `z`(`a`, `b`) VALUES (5, 3);
INSERT INTO `z`(`a`, `b`) VALUES (7, 6);
INSERT INTO `z`(`a`, `b`) VALUES (10, 8);
~~~

表z的列b是辅助索引,若在会话A中执行下面的SQL语句: 
~~~
SELECT * FROM z WHERE b=3 FOR UPDATE;
~~~
很明显,这时SQL语句通过索引列b进行查询,因此其使用传统的Next-key Locking技术加锁,并且由于有两个索引,其需要分别进行锁定。
1、对于聚集索引,其仅 对列a等于5的索引加上 Record Lock。
2、而对于辅助索引,其加上的是Next -Key- Lock, 锁定的范围是[1,3),特别需要注意的是, InnoDB存储引擎还会对辅助索引下一个键值加上 gap lock,即还有一个辅助索引范围为[3,6) 的锁。因此,若在新会话B运行下面的SQL语句,都会被阻塞: 
~~~
SELECT * FROM z WHERE a = 5 LOCK IN SHARE MODE;
INSERT  INTO  z SELECT 4,2;
INSERT  INTO z SELECT 6,5; 
~~~

第一个SQL语句不能执行,因为在会话A中执行的SQL语句已经对聚集索引中列a= 5的值加上X锁,因此执行会被阻塞。
第二个SQL语句,主键插入4,没有问题,但是插人的辅助索引值2在锁定的范围[1,3)中,因此执行同样会被阻塞。第三个SQL语句, 插人的主键6没有被锁定,5也不在范围[1,3)之间。但插入的值5在另一个锁定的范围 [3,6)中,故同样需要等待。
>Next -Key- Lock 作用在辅助索引上时会锁住具体记录的邻近的上下区间！这个例子的邻键锁就将 [1,3)和[3,6)锁住了

可以这样查询具体锁的信息，比较一下三个sql 导致的 lock_mode字段信息 : X、X,GAP、S


第1个sql
~~~
mysql> SELECT * from information_schema.INNODB_LOCKS;
+-------------------------+-----------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
| lock_id                 | lock_trx_id     | lock_mode | lock_type | lock_table | lock_index | lock_space | lock_page | lock_rec | lock_data |
+-------------------------+-----------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
| 283710356088624:754:3:4 | 283710356088624 | S         | RECORD    | `iam`.`z`  | PRIMARY    |        754 |         3 |        4 | 5         |
| 113269:754:3:4          | 113269          | X         | RECORD    | `iam`.`z`  | PRIMARY    |        754 |         3 |        4 | 5         |
+-------------------------+-----------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
2 rows in set (0.06 sec)
~~~

第2个sql
~~~
mysql> SELECT * from information_schema.INNODB_LOCKS;
+----------------+-------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
| lock_id        | lock_trx_id | lock_mode | lock_type | lock_table | lock_index | lock_space | lock_page | lock_rec | lock_data |
+----------------+-------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
| 113292:754:4:4 | 113292      | X,GAP     | RECORD    | `iam`.`z`  | b          |        754 |         4 |        4 | 3, 5      |
| 113269:754:4:4 | 113269      | X         | RECORD    | `iam`.`z`  | b          |        754 |         4 |        4 | 3, 5      |
+----------------+-------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
2 rows in set (0.06 sec)
~~~


第3个sql
~~~
mysql> SELECT * from information_schema.INNODB_LOCKS;
+----------------+-------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
| lock_id        | lock_trx_id | lock_mode | lock_type | lock_table | lock_index | lock_space | lock_page | lock_rec | lock_data |
+----------------+-------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
| 113270:754:4:5 | 113270      | X,GAP     | RECORD    | `iam`.`z`  | b          |        754 |         4 |        5 | 6, 7      |
| 113269:754:4:5 | 113269      | X,GAP     | RECORD    | `iam`.`z`  | b          |        754 |         4 |        5 | 6, 7      |
+----------------+-------------+-----------+-----------+------------+------------+------------+-----------+----------+-----------+
2 rows in set (0.05 sec)
~~~

而下面的SQL语句,不会被阻塞,可以立即执行:
~~~
INSERT INTO z SELECT 8,6;
INSERT INTO z SELECT 2,0; 
INSERT INTO z SELECT 6,7; 
~~~




###关闭GAP锁
从上面的例子中可以看到, Gap Lock的作用是为了阻止多个事务将记录插入到同一范围内,而这会导致Phantom Problem（幻影读）问题的产生。

例如在上面的例子中,会话A中用户已经锁定了b=3的记录。若此时没有 Gap Lock锁定(3,6),那么用户可以插入索引b列为3的记录,这会导致会话A中的用户再次执行同样查询时会返回不同的记录, 即导致 Phantom Problem 问题的产生。

用户可以通过以下两种方式来显式地关闭 Gap Lock: 
1、将事务的隔离级别设置为 READ COMMITTED 
2、将参数 innodb_locks_unsafe_for_binlog 设置为1 
~~~
SHOW VARIABLES LIKE '%innodb_locks_unsafe_for_binlog%'
~~~

在上述的配置下,除了外键约束和唯一性检查依然需要的 Gap Lock,其余情况仅使 用 Record Lock进行锁定。但需要牢记的是,上述设置破坏了事务的隔离性,并且对于 replication,可能会导致主从数据的不一致。此外,从性能上来看, READ COMMITTED 也不会优于默认的事务隔离级别 READ REPEATABLE 在 InnoDB存储引擎中,对于 INSERT的操作,其会检查插入记录的下一条记录是否被锁定,若已经被锁定,则不允许查询。对于上面的例子,会话A已经锁定了表z中 b=3的记录,即已经锁定了(1,3)的范围,这时若在其他会话中进行如下的插入同样会导致阻塞: 
~~~
 INSERT INTO z SELECT 2,2; 
~~~


因为在辅助索引列 b上插入值为2的记录时,会监测到下一个记录3已经被索引，而将插入修改为如下的值,可以立即执行: 
~~~
INSERT INTO z SELECT 2,0; 
~~~

>最后需再次提醒的是,对于唯一键值的锁定,Next- Key Lock降级为 Record Lock 仅存在于查询所有的唯一索引列。若唯一索引由多个列组成,而查询仅是查找多个唯 一索引列中的其中一个,那么查询其实是 range类型查询,而不是 point类型查询,故 InnoDB存储引擎依然使用Next- -Key Lock进行锁定。这个也可以使用实验的方式验证。
