---
title: mysql-联接查询算法之实践篇（六）和优化join总结.md
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
title: mysql-联接查询算法之实践篇（六）和优化join总结.md
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
**mysql选择使用连接算法的优先级**
在选择Join算法时，会有优先级，理论上会优先判断能否使用INLJ、BNLJ：
内部表关联字段上有索引 Index Nested-LoopJoin > 5.7 Block Nested-Loop Join、8.0  Hash Join > Simple Nested-Loop Join
**示例**
1、数据准备

表结构
~~~
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
~~~

~~~
CREATE TABLE `book`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `book_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
~~~

编写存储过程创建数据

~~~

-- 随机字符串函数
CREATE DEFINER=`root`@`localhost` FUNCTION `rand_string`(n int) RETURNS varchar(255) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci
begin
   declare chars_str varchar(100) default 'qwertyuiopasdfghjklzxcvbnm';
   declare return_str varchar(255) default '';
   declare i int default 0;
   while i<n do
   set return_str=concat(return_str,substring(chars_str,floor(1+rand()*52),1));
   set i=i+1;
   end while;
   return return_str;
 end

-- addUser 添加用户信息存储过程
CREATE DEFINER=`root`@`%` PROCEDURE `addUser`(in max_num int(10))
begin
 declare i int default 0;
 repeat
 set i=i+1;
 INSERT INTO `test`.`user`(`name`) VALUES (rand_string(16));
 until i=max_num end repeat;

end

-- addUser 添加书籍信息存储过程
CREATE DEFINER=`root`@`%` PROCEDURE `addBook`(in max_num int(10))
begin
 declare i int default 0;
 repeat
 set i=i+1;
INSERT INTO `test`.`book`(`user_id`, `book_name`) VALUES (FLOOR( 1 + RAND() * (1000 - 1)), rand_string(20));

 until i=max_num end repeat;

end
~~~

2、给 user表添加1000条，book表添加10万条。1：100


3、看看执行计划

~~~
EXPLAIN SELECT * FROM `user` a LEFT JOIN book  b IGNORE index(index_user_id)  ON a.id=b.user_id
~~~
A、强制不走内表的索引的join，使用了BNL。查询时间7.298秒。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d403318fd4b7d708.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

B、相反，强制走索引。使用了INLJ，查询时间0.210秒！
~~~
EXPLAIN SELECT a.name,b.book_name FROM `user` a LEFT JOIN book  b force index(index_user_id)  ON a.id=b.user_id
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e5cb3c89a64b07fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> 不能在Extra字段中看到是否使用INLJ算法，但是可以通过key观察有没有用到索引

C、再来看看，将BNLJ关闭。查询会变得多慢。。先看执行计划
~~~
SET optimizer_switch = 'block_nested_loop=off'; 
EXPLAIN SELECT *  FROM `user` a LEFT JOIN book  b force index(index_user_id)  ON a.id=b.user_id
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d6f978fcbf9f4d75.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


果然，连BNLJ都不使用的话会变成30秒！这时候应该使用的是SNLJ连接算法。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2b97aa120c022222.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>使用SNLJ也不会体现在Extra，但是我们观察到key字段是空的。


D、开启BKA算法，看看情况
~~~
SET optimizer_switch='mrr=on,mrr_cost_based=off,batched_key_access=on';
EXPLAIN SELECT *  FROM `user` a LEFT JOIN book  b force index(index_user_id)  ON a.id=b.user_id
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a2836d54a7602468.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
耗时 0.276秒。从我这里的实验结果来看BKA相对于INLJ来说并没有很明显的优化，可能是我的实验姿势不对吧。



**总结下**

BKA  > INLJ  （可能成立）0.22s
        > BNLJ   （成立）    8s       
        > SNLJ      （成立） 30s


mysql5.7对于join查询总是默认先使用 INLJ，内部表关联字段没加索引得话就去使用BNLJ   。若block_nested_loop=off 那么就回去使用SNLJ了。

而BKA默认是关闭的，这方面mysql比较保守。想要在二者BKA和INLJ之间做出抉择可以自行测试对比二者性能。


**再看看mysql8中的hash join 性能测试**

![image.png](https://upload-images.jianshu.io/upload_images/13965490-87c5c35eaa883439.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


~~~
EXPLAIN  SELECT *  FROM `user` a LEFT JOIN book  b IGNORE index(index_user_id)  ON a.id=b.user_id
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-05474d2dae871a31.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意，这里为什么要IGNORE 忽略使用索引呢？ mysql优先会使用INLJ而不是 hash join。而hash join 是不需要索引支持的，hashjoin在mysql8中是一种代替 BNLJ的一种更高效的join算法。

查询时间0.497秒，相对于上面mysql 5.7中使用BNLJ 的8秒可是快了很多。



**最后总结下如何优化Join速度**

由于连接的成本比较高，因此对于高并发的应用，应该尽量减少有连接的查询，连接的表的个数不能太多，连接的表建议 控制在4个以内。互联网应用比较常见的一种情况是，在数据量比较小的时候，连接的开销不大，这个时候一般不会有性能问 题，但当数据量变大之后，连接的低效率问题就暴露出来了，成为整个系统的瓶颈所在。所以对于数据库应用的设计，最好在 早期就确定未来可能会影响性能的一些查询，进行反范式设计减少连接的表，或者考虑在应用层进行连接。 优化连接的一些要点如下。 

1、使用EXPLAIN检查连接，留意EXPLAIN输出的rows列，如果rows列太高，比如几千，上万，那么就需要考虑是否索引不佳或连接表的顺序不当。用小结果集驱动大结果集，减少外层循环的数据量，从而减少内层循环次数：如果小结果集和大结果集连接的列都是索引列，mysql在内连接时也会选择用小结果集驱动大结果集，因为索引查询的成本是比较固定的，这时候外层的循环越少，join的速度便越快。

2、为内部表的关联字段上增加索引：争取使用INLJ，减少内层表的循环次数；ON、USING子句中的列确认有索引。如果优化器选择了连接的顺序为B、A，那么我们只需要在A表的列上创建索引即可。例如，对于查询“SELECT B.*,A.*FROM B JOIN A ON B.col1=A.col2;”语句MySQL会全表扫描B表，对B表的每一行记录探测 A表的记录（利用A表col2列上的索引）。

3、增大join buffer size的大小：当使用BNLJ/Hash Join时，一次缓存的数据越多，那么内层表循环的次数就越少

4、减少不必要的字段查询：
（1）当用到BNLJ时，字段越少，join buffer 所缓存的数据就越多，内层表的循环次数就越少；
（2）当用到INLJ时，如果可以不回表查询，即利用到覆盖索引，则可能可以提升速度。（未经验证，只是一个推论）


5、最好是能转化为INNER JOIN，LEFT JOIN的成本比INNERJOIN高很多。

6、反范式设计，增加冗余字段。这样可以减少连接表的个数，加快存取数据的速度。

7、考虑在应用层实现连接。 对于一些复杂的连接查询，更值得推荐的做法是将它分解为几个简单的查询，可以先执行查询以获得一个较小的结果集， 然后再遍历此结果集，最后根据一定的条件去获取完整的数据，这样做往往是更高效的，因为我们把数据分离了，更不容易发 生变化，更方便缓存数据，数据也可以按照设计的需要从缓存或数据库中进行获取。例如，对于如下的查询： SELECT a.* FROM a WHERE a.id IN (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17); 如果id=1~15的记录已经被存储在缓存（如Memcached）中了，那么我们只需要到数据库查询“SELECT a.*FROMa WHERE a.id=16”和“SELECT a.*FROMa WHERE a.id=17”了。而且，把IN列表分解为等值查找，往往可以提高性能。

8、一些应用可能需要访问不同的数据库实例，这种情况下，在应用层实现连接将是更好的选择。
