---
title: mysql-8-新特性三-Hash-Join---联接查询算法之Hash-Join-(五).md
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
title: mysql-8-新特性三-Hash-Join---联接查询算法之Hash-Join-(五).md
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
>Hash Join 算法

mysql8以前 的 join 算法只有 nested loop 这一种，在 MySQL8 中推出了一种新的算法 hash join，比  nested loop 更加高效。mysql8中的部分NLJ算法已经取消，hash join  是它的的替代方案。像属于NLJ的BNLJ、SNLJ都会被Hash join替代！不过基于索引的INLJ算法还是存在的，所以实际使用中可以对比下INLJ和Hash Join的查询性能然后做出选择。



个人觉得mysql8这个hash join也只能算是一个锦上添花的功能，顶多是代替了没有加索引时默认走的BNLJ算法，提高了join的性能下限。说白了就是给不懂加索引的mysql新用户提高下join性能。其实也不绝对，不过我有做 INLJ和Hash Join 对比实验，Hash Join 很有可能比需要在内部表建立索引的INLJ算法性能要好！毕竟当INLJ需要回表查的时候性能会大幅度下降，这时候Hash Join绝对值得一试的，当然具体两者之间的选择还请自己实际测试下。


###下面我就看看hash join 是怎么工作的。
创建user和book表
~~~
CREATE TABLE `test`.`user`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 772360 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

CREATE TABLE `test`.`book`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(0) NULL DEFAULT NULL,
  `book_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compressed;
~~~
可以看看下列语句的执行计划，Extra 出现了  Using join buffer (hash join) 说明该语句使用到了hash join。这里还使用了 IGNORE index(index_user_id)禁用索引，不然使用的是INLJ。
~~~
mysql>  EXPLAIN SELECT *  FROM `user` a LEFT JOIN book  b IGNORE index(index_user_id)  ON a.id=b.user_id;
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+--------------------------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra                                      |
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+--------------------------------------------+
|  1 | SIMPLE      | a     | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 639820 |   100.00 | NULL                                       |
|  1 | SIMPLE      | b     | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 785214 |   100.00 | Using where; Using join buffer (hash join) |
+----+-------------+-------+------------+------+---------------+------+---------+------+--------+----------+--------------------------------------------+
2 rows in set (0.03 sec)
~~~


那么，使用Hash Join会分为下面2个阶段：

1、build  构建阶段：从参与join的2个表中选一个，选择占空间小的那个表，不是行数少的，这里假设选择了 user 表。对 user表中每行的 join 字段值进行 hash(a.id ) 计算后放入内存中 hash table 的相应位置。所有行都存放到 hash table 之后，构建阶段完成。

溢出到磁盘在构建阶段过程中，如果内存满了，会把表中剩余数据写到磁盘上。不会只写入一个文件，会分成多个块文件。

2、probe  探测阶段：对 book 表中每行中的 join 字段的值进行 hash 计算：hash(b.user_id) 拿着计算结果到内存 hash table 中进行查找匹配，找到一行就发给 client。这样就完成了整个 join 操作，每个表只扫描一次就可以了，扫描匹配时间也是恒定的，非常高效。



###hash join 相关参数



散列连接的内存使用可以使用join_buffer_size系统变量来控制；散列连接使用的内存不能超过这个数量。当散列连接所需的内存超过可用的数量时，MySQL通过使用磁盘上的文件来处理这个问题(溢出到磁盘)。

如果发生这种情况，您应该知道，如果散列连接无法容纳在内存中，并且它创建的文件超过了为open_files_limit设置的数量，则连接可能不会成功。

为避免此类问题，请执行以下任一更改:
1、增加join_buffer_size，以便哈希连接不会溢出到磁盘。
在MySQL 8.0.19及更高版本中， 设置 optimizer_switch  变量值 hash_join=on or hash_join=off 的方式已经失效了


2、增加open_files_limit。若数据量实在太大内存无法申请更大的join_buffer，就只能溢出到磁盘上了。我们可以增加open_files_limit，防止创建的文件超过了为open_files_limit设置的数量而join失败。


###查看hash join的执行计划
必须使用format=tree（8.0.16的新特性）才能查看hash join的执行计划：


~~~
EXPLAIN format=tree  SELECT *  FROM `user` a LEFT JOIN book  b IGNORE index(index_user_id)  ON a.id=b.user_id
~~~
>-> Left hash join (b.user_id = a.id)  (cost=10005295.31 rows=100050000)
    -> Table scan on a  (cost=101.00 rows=1000)
    -> Hash
        -> Table scan on b  (cost=10.29 rows=100050)


###对比下INLJ的执行计划：
~~~
EXPLAIN format=tree  SELECT *  FROM `user` a LEFT JOIN book  b force index(index_user_id)  ON a.id=b.user_id
~~~
>-> Nested loop left join  (cost=34806.15 rows=99158)
    -> Table scan on a  (cost=101.00 rows=1000)
    -> Index lookup on b using index_user_id (user_id=a.id)  (cost=24.80 rows=99)



###什么样的sql可以用到Hash Join

创建几张测试表
~~~
CREATE TABLE t1 (c1 INT, c2 INT);
CREATE TABLE t2 (c1 INT, c2 INT);
CREATE TABLE t3 (c1 INT, c2 INT);
~~~
从MySQL 8.0.18开始，MySQL对每个连接都有一个等连接条件的任何查询都使用散列连接，并且没有可应用于任何连接条件的索引，例如:

~~~
mysql> EXPLAIN
SELECT *
    FROM t1
    JOIN t2
        ON t1.c1=t2.c1;
				
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra                                      |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------+
|  1 | SIMPLE      | t1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | NULL                                       |
|  1 | SIMPLE      | t2    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using where; Using join buffer (hash join) |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------+
2 rows in set (0.02 sec)

~~~


在MySQL 8.0.20之前，如果任何一对连接的表没有至少一个等连接条件，就不能使用Hash Join，并且使用了较慢的BNLJ。而`在MySQL 8.0.20和更高版本中，hash join可以用于未包含等值连接条件的查询`
~~~
mysql> explain SELECT * FROM t1
    JOIN t2 ON (t1.c1 < t2.c1 AND t1.c2 < t2.c2)
    JOIN t3 ON (t2.c1 < t3.c1); 
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra                                      |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------+
|  1 | SIMPLE      | t1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | NULL                                       |
|  1 | SIMPLE      | t2    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using where; Using join buffer (hash join) |
|  1 | SIMPLE      | t3    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using where; Using join buffer (hash join) |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------+
3 rows in set (0.05 sec)
~~~

甚至是笛卡尔积的join
~~~
mysql> explain SELECT * FROM t1,t2,t3;
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra                         |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------------------------+
|  1 | SIMPLE      | t1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | NULL                          |
|  1 | SIMPLE      | t2    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using join buffer (hash join) |
|  1 | SIMPLE      | t3    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using join buffer (hash join) |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------------------------+
3 rows in set (0.05 sec)
~~~

Semijoin也行
~~~
mysql> EXPLAIN  SELECT * FROM t1 
       WHERE t1.c1 IN (SELECT t2.c2 FROM t2)
    -> ;
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+------------------------------------------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra                                                      |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+------------------------------------------------------------+
|  1 | SIMPLE      | t1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | NULL                                                       |
|  1 | SIMPLE      | t2    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using where; FirstMatch(t1); Using join buffer (hash join) |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+------------------------------------------------------------+
2 rows in set (0.06 sec)
~~~


还有 antijoin 

~~~
mysql>  EXPLAIN  SELECT * FROM t2 
         WHERE NOT EXISTS (SELECT * FROM t1 WHERE t1.c1 = t2.c1);
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra                                                  |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------------------+
|  1 | SIMPLE      | t2    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | NULL                                                   |
|  1 | SIMPLE      | t1    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using where; Not exists; Using join buffer (hash join) |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+--------------------------------------------------------+
2 rows in set (0.07 sec)
~~~
###Hash join
外表扫描次数=1
内表扫描次数=1
比较次数 = 内表行数
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5325ecdaa4039e2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b9ce46ae6573909a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>单单看这些次数hashjoin和INLJ好像没区别，但是在一种情况下：

join 的字段不是主键，而且select中要回表

###hash join 相对于INLJ优点、缺点
1、hash join 支持多线程并发查询
2、hash join 不需要回表；他是把外边的所有字段都存入 join buffer；在大数据量查询索引未覆盖时效率比较高
3、hash join 不用建立索引
4、hash join 仅仅支持 等值的join
5、hash join 性能受限于 join buffer 大小



