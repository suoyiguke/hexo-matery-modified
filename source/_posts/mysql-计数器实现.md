---
title: mysql-计数器实现.md
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
title: mysql-计数器实现.md
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
> 或为辽东帽，清操厉冰雪。

如果应用在表中保存计数器，则在更新计数器时可能，碰到并发问题。计数器表在web应用中很常见。可以用这种表缓存一个用户的朋友数、文件下载次数等。

> 问题在于，若只有一条记录保存计数器数量，那么在并发修改事务下因为需要杜绝线程安全问题，INNODB行锁在起作用。这样导致修改的事务引发阻塞、串行执行，进而性能下降。为了解决这个问题我们使用一种`以空间换时间` 的思想。

我们创建一张计数器表，包含 slot 槽标识、cnt 数量字段
~~~
CREATE TABLE `test`.`hit_counter`  (
  `slot` tinyint(100) NOT NULL COMMENT '槽',
  `cnt` int(255) UNSIGNED NOT NULL COMMENT '数量',
  PRIMARY KEY (`slot`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~

然后预先在这张表中插入100行数据作为槽(slot)。编写存储过程，插入100条数据。

~~~
CREATE DEFINER=`root`@`%` PROCEDURE `insert_hit_counter`(in start int(10),in max_num int(10))
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 set autocommit= 0;
 repeat
 set i=i+1;
 INSERT INTO `test`.`hit_counter`(`slot`, `cnt`) VALUES ((start+i), 0);
 until i=max_num end repeat;
commit;
end

CALL insert_hit_counter(0,100);
~~~

现在选择一个随机的槽(slot)进行更新，在应用程序中。即是出现并发修改，这样可不会引发阻塞了。

~~~
set @slot = FLOOR( 1 + RAND() * (101 - 1));
UPDATE hit_counter SET cnt = cnt +1  WHERE slot = @slot;
~~~

> 被本来我是直接使用 `UPDATE hit_counter SET cnt = cnt +1  WHERE slot = FLOOR( 1 + RAND() * (101 - 1));` 语句的，但是存在问题。有时候影响行数0，有时影响函数为2。很奇怪;所以这里使用用户变量来存储随机数。


使用下面SUM聚合查询即可获得统计结果
~~~
SELECT SUM(cnt) FROM hit_counter;
~~~

###### 每天重新开始一个新的计数器

设计表如下
~~~
CREATE TABLE `test`.`hit_counter`  (
  `slot` tinyint(100) NOT NULL COMMENT '槽',
  `cnt` int(255) UNSIGNED NOT NULL COMMENT '数量',
  `day` date NOT NULL COMMENT '天',
  PRIMARY KEY (`slot`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~


使用 `ON DUPLICATE KEY UPDATE` 插入或更新如下
~~~
set @slot = FLOOR( 1 + RAND() * (101 - 1));
INSERT INTO `test`.`hit_counter`(`slot`, `cnt`, `day`) VALUES (@slot,1, CURRENT_DATE) ON DUPLICATE KEY UPDATE cnt = cnt + 1;
~~~

按照时间过滤统计计数如下
~~~
SELECT SUM(cnt) FROM hit_counter WHERE day = CURRENT_DATE;
~~~

如果希望减少函数，以避免表变得太大，可以写一个周期执行的任务，合并所有的结果到0号槽，并且删除所有其他的槽：
~~~
UPDATE hit_counter AS c
INNER JOIN (
  SELECT day,sum(cnt) AS cnt,MIN(slot) AS MSLOT
	FROM hit_counter
	GROUP BY day
) AS x USING(day)

SET c.cnt = IF(c.slot = x.mslot,x.cnt,0),
c.slot = IF(c.slot = x.mslot,0,c.slot );

DELETE FROM hit_counter WHERE slot!= 0 AND cnt = 0;
~~~

> 事实上，这个计数器功能使用redis实现会很方便。也就是一个命令的事情。。。
