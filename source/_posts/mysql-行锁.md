---
title: mysql-行锁.md
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
title: mysql-行锁.md
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
###InnoDB的行锁按锁的互斥程度来划分


####Shared Lock 共享锁（s）：又称读锁。
- 允许一个事务去读一行，阻止其他事务获得相同数据集的排他锁。–读锁
- 显式加锁
~~~
select * from test lock in share mode;
~~~

####Exclusive Lock 排他锁（Ｘ）：又称写锁。
- 允许获取排他锁的事务更新数据，阻止其他事务取得相同的数据集共享读锁和排他写锁。–写锁

- 对于UPDATE、DELETE和INSERT语句，InnoDB会自动给涉及及数据集加排他锁（Ｘ）；对于普通SELECT语句，InnoDB不会加任务锁；


- 显式加锁
~~~
select * from test for update;
~~~
#### 无锁、S锁、X锁的互斥情况试验


锁类型|lock in share mode| for update |   
-|-|-
select | 兼容 | 兼容| 
lock in share mode|  兼容 | 互斥 | 
for update| 互斥 | 互斥 | 


为了节省时间，x锁我统一使用select … for update的方式

#####S锁的互斥情况
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f4a400d1802131da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####X锁的互斥情况
![image.png](https://upload-images.jianshu.io/upload_images/13965490-70e9fa83b46781df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###S锁和X锁的注意事项
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b2cfa67fe8bcd005.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 如果事务A使用select ... lock in share mode 的话，之后事务B也使用select ... lock in share mode。这样事务B持锁，然后在事务A里执行update语句会造成死锁；对于锁定记录后需要进行更新操作的应用，应该使用select ... for update 的方式获得排它锁。

###InnoDB行锁实现方式

- 在不通过索引条件查询时，InnoDB会锁定表中的所有记录！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a219c586d0156eca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- mysql的行锁是针对索引加锁，不是针对记录加锁，所以虽然是访问到不同的记录，但是使用相同的索引键（使用普通索引而非唯一索引），是会出现锁冲突的
在这里id是普通的索引
![image.png](https://upload-images.jianshu.io/upload_images/13965490-531d03a79f68e9a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 当表有多个索引的时候，不同的事务可以使用的索引锁定不同的行，不论是使用主键索引、唯一索引或普通索引，InnoDB都会使用行锁来对数据加锁。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1f1254ec7c449812.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 - 在查询中索引不一定会被用到，这个时候就会进行全表扫描，形成表锁
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ad4b07d0189980f2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)









####InnoDB行锁按实现方案可以分3种：
- 默认情况下，InnoDB工作在RR隔离级别下，并且以Next-Key Lock的方式对数据行进行加锁。
- Next-Key Lock是行锁与间隙锁的组合，这样，当InnoDB扫描索引记录的时候，会首先对选中的索引记录加上行锁（Record Lock），再对索引记录两边的间隙（向左扫描扫到第一个比给定参数小的值， 向右扫描扫描到第一个比给定参数大的值， 然后以此为界，构建一个区间）加上间隙锁（Gap Lock）。

- 如果一个间隙被事务A加了锁，其它事务是不能在这个间隙插入记录的。


**Record lock:**
- `记录锁`，对索引项加锁


**Gap lock:**
- `间隙锁`，锁加在不存在的空闲空间，可以是两个索引记录之间，也可能是第一个索引记录之前或最后一个索引之后的空间。
- 关闭间隙锁：可以通过修改隔离级别为 READ COMMITTED 或者配置 innodb_locks_unsafe_for_binlog 参数为 ON。
mysql5.6中不能通过命令直接设置，表示这个参数是只读的。只能通过修改my.cnf文件后重启
~~~
set @@innodb_locks_unsafe_for_binlog = ON
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aa62bb4889204a67.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 间隙锁在RR级别下开启
- 间隙锁会对 在`不存在的记录`上做`insert`操作 加锁
- 间隙锁验证
![image.png](https://upload-images.jianshu.io/upload_images/13965490-944d69fb13f30b0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1733c9228a4db151.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 当操作作用于 `不存在的一条记录` 时也会出现间隙锁，验证如下：
以update为主
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e2d5816d7284ef7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

以select .. for update为主
![image.png](https://upload-images.jianshu.io/upload_images/13965490-863dc64976e5898a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

以insert为主
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a94e75b0460d41cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
以delete为主
![image.png](https://upload-images.jianshu.io/upload_images/13965490-12b6c1235547fb43.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

id=15的记录并不存在
锁类型|select * from test where id = 15 for update;| delete from test where id = 15; |   update test set a='fff' where id =15; |   INSERT INTO `test`(`id`, `a`, `b`, `c`) VALUES (15, 'new !!!!', 'bbb', 'ccc');
-|-|-|-|-
select * from test where id = 15 for update; | 兼容 | 兼容|  兼容|  互斥
delete from test where id = 15;	|  兼容 | 兼容 | 兼容|   互斥
update test set a='fff' where id =15;	| 兼容 | 兼容 | 兼容|  互斥
INSERT INTO `test`(`id`, `a`, `b`, `c`) VALUES (15, 'new !!!!', 'bbb', 'ccc');| 互斥 | 互斥| 互斥|  互斥
- 在RC下验证间隙锁关闭情况
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7c6e182f07cf2d84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
RC下间隙锁的确是关闭的。如果事务B提交后。事务A继续执行一个查询操作。可以发现多处了一条记录。出现了`幻读`！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-523461cde9ac07fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 我在这里有两个问题很不解：
1、《高性能mysql》说MVCC机制在RC和RR下生效，那为什么不能杜绝RC下的幻读？
答：因为RC下和RR下MVCC机制不同，RC下每次select都会生成readview，而RR下只在第一次select生成readview
2、RC下因为没有间隙锁机制而出现了幻读。那MVCC机制解决幻读和间隙锁解决的幻读是不是一个概念？
答：RR下的MVCC能解决幻读是：普通select快照读；RR下间隙锁解决的幻读是：select ... lock in share mode、select .. for update的加锁读
- 间隙锁的危害
![image.png](https://upload-images.jianshu.io/upload_images/13965490-83624e8f690c87dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**Next-key lock:**
- `临键锁`，该锁就是 Record Locks 和 Gap Locks 的组合，即锁定一个范围并且锁定该记录本身
- 举个例子，如果一个索引有 1, 3, 5 三个值，则该索引锁定的区间为 (-∞,1], (1,3], (3,5], (5,+ ∞) `前开后闭区间`

###查看行锁情况
~~~
show status like 'InnoDB_row_lock%';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f160bd135a72da3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对于各个字段说明如下：

- Innodb_row_lock_current_waits:当前正在等待锁的数量；
- Innodb_row_lock_time:从系统启动到现在锁定总时间长度；
- Innodb_row_lock_time_avg：每次等待所花平均时间；
- Innodb_row_lock_time_max:从系统启动到现在等待最长的一次所花的时间长度；
- Innodb_row_lock_waits:系统启动到现在总共等待的次数；
如果发现锁争用比较严重，还可以通过设置InnoDB Monitors 来进一步观察发生锁冲突的表、数据行等，并分析锁争用的原因。

> 注意，这条sql无法查询到持锁数量和锁类型。只有在引发阻塞后才会记录锁的信息。在mysql5.7中请使用show engine innodb status;来获得这两个信息！

###关于行锁的优化建议
- 尽可能让所有数据检索都通过索引来完成，避免无索引行锁升级为表锁
- 合理设计索引，尽量缩小锁的范围
- 尽可能较少检索条件，避免间隙锁
- 尽量控制事务大小，减少锁定资源量和时间长度
- 尽可能低级别事务隔离

