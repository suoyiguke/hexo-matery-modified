---
title: mysql-导入数据优化和关于insert-into-select语句不得不说的问题.md
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
title: mysql-导入数据优化和关于insert-into-select语句不得不说的问题.md
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
>或为渡江楫，慷慨吞胡羯。 


###数据导入的一些技巧优化，提高导入速度
在恢复数据时，可能会导入大量的数据。此时为了快速导入，需要掌握一些技巧：


1、待数据导入完成之后，再开启索引和约束，一次性创建索引

关闭索引
~~~
alter table table-name disable keys
~~~
导入完毕后，开启索引
~~~
alter table table-name enable keys
~~~

2、数据库如果使用的引擎是Innodb，那么它`默认会给每条写指令加上事务`（这也会消耗一定的时间），因此建议先手动开启事务，再执行一定量的批量导入，最后手动提交事务。
~~~
SET @@autocommit = 0;
xxx 导入sql  xxx
commit;
~~~

3、如果批量导入的SQL指令格式相同只是数据不同，那么你应该先prepare`预编译`一下，这样也能节省很多重复编译的时间。
关于mysql提供的sql预编译可以看看这篇https://www.jianshu.com/p/1b242d3f2395

4、可以暂时将表的存储引擎改为myisam，这样导入速度会非常的快。



###采用insert into select 语句进行表数据迁移不得不说的问题

insert into select可以用来实现表之间的数据迁移，这样就可以避免使用网络I/O，直接使用SQL依靠数据库I/O完成。所以效率会非常高。

~~~
DROP TABLE IF EXISTS B;
CREATE TABLE B LIKE A;
INSERT INTO B SELECT * FROM A;
~~~



但是这种方式存在一个致命的问题：在某些情况下会阻塞其他事务的增删改查，导致线上业务崩溃。很可怕的。



> "insert into tb select * from tbx" 的导入操作是会锁定原表，但是锁是有2种情况：“逐步锁”，“全锁”。


###实验

######准备数据,创建box表
~~~
CREATE TABLE `test`.`box`  (
  `id` bigint(36) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `create_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  `update_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `sys_org_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属部门',
  `status` int(10) NULL DEFAULT 0 COMMENT '状态',
  `number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '编号',
  `zi_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '自编号',
  `house_address` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '仓库地址',
  `sb_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备id',
  `point_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '投放点id',
  `point` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '投放点',
  `confirm` int(32) NULL DEFAULT 0 COMMENT '商户/企业用户确认入库，默认为0（未确认）1是已确认',
  `last_point` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最近一次投放点名',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1000002 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~
### 使用查询验证
执行数据迁移sql
~~~
insert into box select * from tb_box;
~~~

然后立即执行以下查询。
查询1:  普通查询，快照读。并不会引发阻塞
~~~
SELECT id FROM tb_box  WHERE id = 10 
~~~


查询2: 加上排他锁
~~~
SELECT id FROM tb_box  WHERE id = 10 FOR UPDATE
~~~
阻塞，我们可以看看当前事务和锁的情况，执行
>SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS w INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.lock_trx_id;
~~~
443027:1792:4:10	443027	X	RECORD	`test`.`tb_box`	PRIMARY	1792	4	10	10	443027	LOCK WAIT	2020-04-26 13:54:46	443027:1792:4:10	2020-04-26 13:54:46	2	24	SELECT id FROM tb_box  WHERE id = 10 for UPDATE	starting index read	1	1	2	1136	1	0	0	REPEATABLE READ	1	1		0	0	0	0

443022:1792:4:10	443022	S	RECORD	`test`.`tb_box`	PRIMARY	1792	4	10	10	443022	RUNNING	2020-04-26 13:54:44			177633	25	insert into box select * from tb_box	inserting	2	2	1508	155856	177631	176125	0	REPEATABLE READ	1	1		0	0	0	0
~~~
查询3: 加上共享锁，并不会引发阻塞
~~~
SELECT id FROM tb_box  WHERE id = 10 lock in SHARE MODE 
~~~



> 得出结论： insert into table1 ...select * from table2； 使用的是共享锁，而非排他锁。

###使用insert测试
>模拟一个事务做数据迁移，另外多个事务做插入数据操作。看看会不会阻塞insert 

1、先执行
~~~
insert into box select * from tb_box
~~~
2、同时在其他事务中并发插入tb_box。看看情况如何

编写插入box表的存储过程
> 为了让每个insert单独一个事务，这里将set autocommit= 0和commit注释
~~~
CREATE DEFINER=`root`@`%` PROCEDURE `insert_tb_box`(in start int(10),in max_num int(10))
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 -- set autocommit= 0;
 repeat
 set i=i+1;
 INSERT INTO `test`.`tb_box`(`create_by`, `create_time`, `update_by`, `update_time`, `sys_org_code`, `status`, `number`, `zi_number`, `house_address`, `sb_number`, `point_id`, `point`, `confirm`, `last_point`) VALUES (rand_string(6), now(), rand_string(6), now(), 'A03', 0, rand_string(20), 'A001', '仓库1', rand_string(20), rand_string(20), NULL, 1, rand_string(30));
 until i=max_num end repeat;
-- commit;
SELECT MAX(id) FROM tb_box;
end
~~~

在执行数据迁移的同时这个存储过程往tb_box表中插入数据
~~~
SET @maxid := 0;
SELECT @maxid := max(id) FROM tb_box;
call insert_tb_box(@maxid,1000);
~~~

>实验结果：数据迁移的速度追上了insert的速度，在某个时刻迁移停止。而insert的存储过程仍然在继续执行。这个是一个存储过程产生多个事务做insert的情况。那么一个存储过程批量的进行insert会怎么样呢？






###使用update来测试
先执行数据迁移sql，将时间小于2020-04-25 20:33:08的数据拷贝到box中 `insert into box SELECT * FROM tb_box WHERE create_time < '2020-04-25 20:33:08'`

再执行业务sql，将2020-04-26 17:07:56的create_by 字段批量修改  `update tb_box set create_by = 'yinkai' WHERE  create_time = '2020-04-26 17:07:56'`

查看当前持有锁的事务
~~~
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS w
INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.lock_trx_id;
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7071ffbe75451dcb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


此时update业务操作发生了锁等待超时，因为排他锁和共享锁冲突。这里就有个疑问了： update语句作用的是2020-04-26 17:07:56，它明明不在< '2020-04-25 20:33:08'的范围内啊，为什么也阻塞了？

我们知道mysql的行锁是基于索引来实现的,我们对数据迁移语句进行执行计划分析：
~~~
EXPLAIN insert into box SELECT * FROM tb_box WHERE create_time < '2020-04-25 20:33:08'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-18dd41be72a23c7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
数据源表tb_box 是全表扫描的，没有用到索引。也就是说明会将所有行锁定，类似于表锁但和表锁之间是有区别的：它是扫描一行即便上一行锁、表锁是立马锁定所有行。那么，我们可以在tb_box.create_time 上建立索引，让它只扫描、只锁定指定范围内的行。

添加索引 `idx_cre_time`
~~~
ALTER TABLE `test`.`tb_box`  ADD INDEX `idx_cre_time`(`create_time`)
~~~

再次执行执行计划，此时的范围查询已经走索引了
~~~
EXPLAIN insert into box SELECT * FROM tb_box  FORCE INDEX(idx_cre_time) WHERE create_time < '2020-04-25 20:33:08'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e19790bb90c7f3a6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后，将box表删除，重新建立。执行迁移sql后立即执行业务sql。这一次没有发生阻塞！修改顺利执行
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8b7979ff97d4804d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###order by 字段不走索引会锁表
order by 字段不走索引会瞬间将整张表的所有记录锁住，而不是之间的扫描一条锁一条。

先执行
~~~
insert into box select * from tb_box ORDER BY create_time
~~~

得到记录数量
~~~
SELECT count(*) FROM tb_box
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0eb680fa2687b3c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后，我们可以通过查询 information_schema.INNODB_TRX 的trx_rows_locked 事务锁主的记录数量来验证。可以看到，这个字段的值瞬瞬间就有一百万多了。而且再不会增加。但是可以发现这个值是大于tb_box表的总数量的。原因是tb_box的id主键列中间有一些被我删除了，留下了“间隙"，这些间隙被加上了间隙锁！
~~~
SELECT trx_rows_locked FROM information_schema.INNODB_TRX 
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-dbfa7239086d021b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###总结

INSERT INTO SELECT * FROM  方式的迁移数据风险非常高，一定要慎用，尽量不要使用。否则线上级易出现锁等待，阻塞业务功能。 INSERT INTO SELECT * FROM 其实就是扫描一条复制一条同时锁定一条，直到表的全部记录被复制完，全部记录被锁定



1、insert into tablA select * from tableB语句，会添加共享锁，会逐渐对表内的所有记录加锁。若已经扫描过指定id，此时有其它事务过来 update了这个id，insert指定id（这个id可能不存在），delete指定id 的时候会阻塞。当然在表的最后面insert是不会阻塞的。这个我实验有验证。

可以查看information_schema.INNODB_TRX 的trx_rows_locked 字段，这个字段表示某个事务中被锁住的行。这个字段值会随着INSERT INTO SELECT * FROM  语句的执行一直增加！直到执行完毕行锁才被释放。
~~~
SELECT (SELECT trx_rows_locked FROM information_schema.INNODB_TRX limit 1) / (SELECT count(*)FROM tb_box) '%'
~~~


2、使用insert into tablA select * from tableB语句时，一定要确保tableB后面的where需要有对应的索引，来避免出现tableB数据源表中我们不需要复制的记录也被扫描也被锁定的情况。此时特别是要注意它是不是进行了全表的扫描。

3、确保order by 字段也要走索引，否则瞬间将整张表中的所有记录加锁！

4、备份操作更好的方式是dump出sql,改个表名，然后source，这个方式就不存在这种锁表问题。只是性能赶不上insert into select；关于dump方式，可以看看这篇文章
https://www.jianshu.com/p/f34dc0a3c5ce
