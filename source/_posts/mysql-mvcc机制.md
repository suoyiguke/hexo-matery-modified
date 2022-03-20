---
title: mysql-mvcc机制.md
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
title: mysql-mvcc机制.md
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
MVCC并发控制中，读操作可以分成两类：快照读 (snapshot read)与当前读 (current read)。

* 快照读，读取的是记录的可见版本 (有可能是历史版本)，不用加锁。

* 当前读，读取的是记录的最新版本，并且，当前读返回的记录，都会加上锁，保证其他事务不会再并发修改这条记录。

###多版本并发控制（MVCC：multi-version concurrency control ）

MVCC定义：`多版本并发控制系统`。可认为是行级锁的一个变种，它能够避免更多情况下的加锁操作。

作用：避免一些加锁操作，提升并发性能。


### 快照读是哪些

一个正常的select…语句就是快照读。

快照读，使得在RR（repeatable read）级别下一个普通select...语句也能做到可重复读。即前面MVCC里提到的利用可见版本来保证数据的一致性。

###  当前读是哪些

insert语句、update语句、delete语句、显示加锁的select语句（select… LOCK IN SHARE MODE、select… FOR UPDATE）是当前读。

为什么insert、update、delete语句都属于当前读？

这是因为这些语句在执行时，都会执行一个读取当前数据最新版本的过程。

当前读的SQL语句，InnoDB是逐条与MySQL Server交互的。即先对一条满足条件的记录加锁后，再返回给MySQL Server，当MySQL Server做完DML操作后，再对下一条数据加锁并处理。

## **基本特征**

-  每行数据都存在一个版本，每次数据更新时都更新该版本。

- 修改时Copy出当前版本随意修改，各个事务之间无干扰。

-  保存时比较版本号，如果成功（commit），则覆盖原记录；失败则放弃copy（rollback）

### MVCC机制在事务隔离级别下

![image.png](https://upload-images.jianshu.io/upload_images/13965490-678ad3b8f0e2081d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-d25af3cbd44cee62.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`MVCC只在2级和3级（   RC 和 RR）下工作`


###MVCC导致的结果
![image.png](https://upload-images.jianshu.io/upload_images/13965490-34d90974558c046d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 实现了非阻塞读，避免了读加锁
- MVCC下的select是快照读，只是读一个历史版本。因此读到的数据总是一致的
- 在一定程度上避免了幻读发生，但是不能彻底杜绝幻读。之前做过实验，MVCC下的insert是当前读，还是会读到别的事务提交的数据。导致主键冲突报错

### 实验证明MVCC：
~~~
CREATE TABLE `test`  (
  `id` int(11) NOT NULL,
  `a` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `b` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `c` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;
~~~
实验一、在RR下, 以为会查到其他事务提交的数据（幻读），但是在A事务中，B事务提交前后两次查询test表都没有查询到B事务插入的id为2的记录。原因是MVCC机制在起作用， 在MVCC下select是快照读，只读快照版本


![image.png](https://upload-images.jianshu.io/upload_images/13965490-aa2c1e834ffe4630.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b86aebdbe7411933.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

实验二、在RR下，先开启事务A，然后开启事务B先插入一条id为3的记录提交，事务A在B提交后也执行一条id为3的插入操作，发现id重复插入失败，而where id=3执行又返回空集（这也是一种幻影读），`因为insert操作是当前读，select是快照读！`RR隔离级别下MVCC机制一定程度上解决了幻读（select操作），但是无法完全杜绝幻读。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-b87228f93d0e70ba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-a2a60e62d0ed3005.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

实验三、在RC下是否存在MVCC机制？
![image.png](https://upload-images.jianshu.io/upload_images/13965490-daadb3f2becdcb81.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我做的实验证明RC下不存在MVCC机制，这是我非常疑惑的地方

- RR下重复使用第一次select生成的ReadView，相当于重复使用第一次的m_ids列表（当前活跃事务id列表）。因此两次select的结果相同
- RC下每次select都会生成ReadView。因此需要按实际机制去推导，这样两次select结果不同的原因也就清晰了！

###MVCC机制的原理
在一篇文章上解答了我上面的疑惑，在这里需要感谢一下文章作者---`小孩子4919`：
https://mp.weixin.qq.com/s?__biz=MzIwNTc4NTEwOQ==&mid=2247487713&idx=1&sn=96f4fa48b9e3f2802e24e8b839f47c5d&chksm=972ac19ba05d488d57e2989da175e272cfc9e85d6eac844342064d04f1f64fef32a259e928c1&mpshare=1&scene=1&srcid=&sharer_sharetime=1578051176803&sharer_shareid=f4084b479306109ea753fc2eac962dee#rd


- READ COMMITTD、REPEATABLE READ这两个隔离级别的一个很大不同就-是生成ReadView的时机不同
- READ COMMITTD在每一次进行普通SELECT操作前都会生成一个ReadView

- REPEATABLE READ只在第一次进行普通SELECT操作前生成一个ReadView，之后的查询操作都重复这个ReadView就好了。

####版本链
对于使用InnoDB存储引擎的表来说，它的聚簇索引记录中都包含两个必要的隐藏列（row_id并不是必要的，我们创建的表中有主键或者非NULL唯一键时都不会包含row_id列）：


- trx_id：每次对某条聚簇索引记录进行改动时，都会把对应的事务id赋值给trx_id隐藏列。
可以查询当前事务的trx_id
~~~
SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX  WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID();
~~~
- roll_pointer：每次对某条聚簇索引记录进行改动时，都会把旧的版本写入到undo日志中，然后这个隐藏列就相当于一个指针，可以通过它来找到该记录修改前的信息。

比方说我们的表t现在只包含一条记录：

~~~
mysql> SELECT * FROM t;
+----+--------+
| id | c      |
+----+--------+
|  1 | 刘备   |
+----+--------+
1 row in set (0.01 sec)
~~~
假设插入该记录的事务id为`80`，那么此刻该条记录的示意图如下所示：

![image](https://upload-images.jianshu.io/upload_images/13965490-09c0c59af162311c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

假设之后两个`id`分别为`100`、`200`的事务对这条记录进行`UPDATE`操作，操作流程如下：

![image](https://upload-images.jianshu.io/upload_images/13965490-5f0341bdd7e793a9?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


每次对记录进行改动，都会记录一条`undo日志`，每条`undo日志`也都有一个`roll_pointer`属性（`INSERT`操作对应的`undo日志`没有该属性，因为该记录并没有更早的版本），可以将这些`undo日志`都连起来，串成一个链表，所以现在的情况就像下图一样：

![image](https://upload-images.jianshu.io/upload_images/13965490-4c89379b95b4a14a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对该记录每次更新后，都会将旧值放到一条`undo日志`中，就算是该记录的一个旧版本，随着更新次数的增多，所有的版本都会被`roll_pointer`属性连接成一个链表，我们把这个链表称之为`版本链`，版本链的头节点就是当前记录最新的值。另外，每个版本中还包含生成该版本时对应的事务id，这个信息很重要，我们稍后就会用到。


####ReadView


对于使用READ UNCOMMITTED隔离级别的事务来说，直接读取记录的最新版本就好了，对于使用SERIALIZABLE隔离级别的事务来说，使用加锁的方式来访问记录。
对于使用READ COMMITTED和REPEATABLE READ隔离级别的事务来说，就需要用到我们上边所说的版本链了，核心问题就是：`需要判断一下版本链中的哪个版本是当前事务可见的`。

 所以设计InnoDB的大叔提出了一个ReadView的概念，这个ReadView中主要包含当前系统中还有哪些活跃的读写事务，把它们的事务id放到一个列表中，我们把这个列表命名为为m_ids。这样在访问某条记录时，只需要按照下边的步骤判断记录的某个版本是否可见：



- 如果被访问版本的trx_id属性值小于m_ids列表中最小的事务id，表明生成该版本的事务在生成ReadView前已经提交，所以该版本可以被当前事务访问。

- 如果被访问版本的trx_id属性值大于m_ids列表中最大的事务id，表明生成该版本的事务在生成ReadView后才生成，所以该版本不可以被当前事务访问。

- 如果被访问版本的trx_id属性值在m_ids列表中最大的事务id和最小事务id之间，那就需要判断一下trx_id属性值是不是在m_ids列表中，如果在，说明创建ReadView时生成该版本的事务还是活跃的（没有提交），该版本不可以被访问；如果不在，说明创建ReadView时生成该版本的事务已经被提交，该版本可以被访问。


- 如果某个版本的数据对当前事务不可见的话，那就顺着版本链找到下一个版本的数据，继续按照上边的步骤判断可见性，依此类推，直到版本链中的最后一个版本，如果最后一个版本也不可见的话，那么就意味着该条记录对该事务不可见，查询结果就不包含该记录。

####可以自己在RC和RR下分别试验
