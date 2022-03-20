---
title: mysql-触发器使用笔记.md
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
title: mysql-触发器使用笔记.md
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
触发器可以用来监视某种情况，并触发某种操作，它是提供给程序员和数据分析员来保证数据完整性的一种方法，它是与表事件相关的特殊的存储过程，它的执行不是由程序调用，也不是手工启动，`而是由事件来触发`，例如当对一个表进行操作（ insert，delete， update）时就会激活它执行。

触发器经常用于加强数据的完整性约束和业务规则等。 触发器创建语法四要素：
> 1.监视地点(table)
2.监视事件(insert/update/delete) 
3.触发时间(after/before) 
4.触发事件(insert/update/delete)

> ps: 触发器内部sql语句和触发条件sql处于同一个事务当中，是具有原子性的。若触发器sql执行失败那么触发条件sql不会得到执行或者回滚！同样触发条件sql执行失败，触发器sql不会得到执行或者回滚。



######使用触发器来完成统计innodb表的统计行数
对于innodb表的count(*)优化，我们可以使用汇总表的方式。其实就可以使用两个触发器实现，一个触发器监听insert后，一个触发器监听delete后。给汇总表分别增加数量和删除数量。最终使用sum()聚合函数即可快速得到数量。

1、after insert
~~~
CREATE DEFINER = `root`@`%` TRIGGER `tgr_box_insert` AFTER INSERT ON `box_fenqu` FOR EACH ROW begin
  set @slot = FLOOR( 1 + RAND() * (101 - 1));
  UPDATE tablecount SET cnt = cnt +1  WHERE id = @slot;
end;

~~~

2、after delete
~~~
CREATE DEFINER = `root`@`%` TRIGGER `tgr_box_delete` AFTER DELETE ON `box_fenqu` FOR EACH ROW begin
  set @slot = FLOOR( 1 + RAND() * (101 - 1));
  UPDATE tablecount SET cnt = cnt -1  WHERE id = @slot;
end;
~~~
具体实现可以看看这篇 https://www.jianshu.com/p/240efe0570e9

###触发器中引用数据

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f78db11464b9145b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、insert_before和insert_after

①、insert_before能读 new、改new
②、insert_after 能读 new、不能改new(报错 `updating of NEW row is not allowed in after trigger`)
③、均不能读 old 和 改old 


2、delete_before 和 delete_after
 ①、delete_before 能读old、不能改old（`updating of OLD row is not allowed in after trigger`）
②、delete_after 能读old、不能改old（`updating of OLD row is not allowed in after trigger`）

③、均不能读 new和 改 new （`There is no NEW row in on DELETE trigger`）

3、update_before和update_after
①、update_before能读new能写new。能读old不能写old
②、update_after能读new不能写new。能读old不能写old

那么我们来实验下，创建一个商品表和一个订单表，使用触发器实现当插入一条订单，具体商品的库存减去购买数量、撤销一个订单库存增加取消的购物数量、修改订单中购买的数量。

~~~

DROP TABLE IF EXISTS `goods`;
CREATE TABLE `goods`  (
  `gid` int(11) NOT NULL COMMENT '主键',
  `name` char(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '商品',
  `num` int(11) NULL DEFAULT NULL COMMENT '库存',
  PRIMARY KEY (`gid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
INSERT INTO `goods` VALUES (1, 'cat', 34);
INSERT INTO `goods` VALUES (2, 'dog', 40);
INSERT INTO `goods` VALUES (3, 'pig', 12);

DROP TABLE IF EXISTS `ord`;
CREATE TABLE `ord`  (
  `oid` int(11) NOT NULL COMMENT '订单号订单主键',
  `gid` int(11) NULL DEFAULT NULL COMMENT '动物编号',
  `much` int(11) NULL DEFAULT NULL COMMENT '购买数量',
  PRIMARY KEY (`oid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

INSERT INTO `ord` VALUES (1, 2, 5);

~~~

######引用insert中产生的数据
这个是插入订单的触发器，引用了new
~~~
CREATE TRIGGER `下订单减库存` AFTER INSERT ON `ord` FOR EACH ROW BEGIN
# 这个new来于触发insert的表ord
UPDATE goods SET num = num - new.much  WHERE gid = new.gid;
END
~~~

######引用delete之前的数据
这个是撤销订单的触发器，引用了old
~~~
DROP TRIGGER IF EXISTS `撤销订单加库存`;
delimiter ;;
CREATE TRIGGER `撤销订单加库存` BEFORE DELETE ON `ord` FOR EACH ROW BEGIN
# 这个old来于触发delete的表ord
UPDATE goods SET num = num + old.much  WHERE gid = old.gid;
END
~~~

#####update中的引用数据
若需要修改订单中的购买数量，则可以使用update类型的触发器。
还是要注意一下： update类型的触发器在before和after之后都可以使用old、new
~~~
CREATE DEFINER = `root`@`%` TRIGGER `撤销订单加库存` BEFORE DELETE ON `ord` FOR EACH ROW BEGIN
# 这个new来于触发insert的表ord
UPDATE goods SET num = num + old.much  WHERE gid = old.gid;
END;
~~~

###before和after的功能区别
实现一个功能，在订单需要5只，而库存只有2只的情况。自动将数量设置为2防止爆仓。我们需要在insert的触发器中，先判断下订单中购买数量是否大于库存，大于库存则将购买数量赋值为库存数量，不允许库存为负数。

那么这个时候，before的作用就体现出来了。insert的before可以修改new，而after无法修改new，若在after中修改new则报错 `updating of NEW row is not allowed in after trigger`。原因是 insert之后，new行已经插入到表中，成为事实无法再去修改了。


所以在在这种情况下只能使用before。

>1、先根据new.gid查出goods商品表中的商品库存，将库存使用`select .. into ..` 语法赋值给rnum 变量。
2、判断if new.much > rnum ，为true。使用 set语句对 new.much进行赋值：  SET new.much = rnum;
3、最后进行update库存
~~~
CREATE DEFINER = `root`@`%` TRIGGER `下订单减库存` BEFORE INSERT ON `Untitled` FOR EACH ROW BEGIN

DECLARE rnum int;
# INTO 和 :=的 区别
SELECT  num INTO rnum FROM goods WHERE gid = new.gid;

if new.much > rnum then
    # 可以使用set语句 对new/old进行赋值
    SET new.much = rnum;
end if;
UPDATE goods SET num = num - new.much  WHERE gid = new.gid;

END;
~~~


######在navicat中配置触发器
navicat中触发器处于`设计表`中的一项功能，就行配置索引一样。可以直接勾选触发条件，往下面填写触发执行的sql即可。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-79eba837630b893c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######查看mysql中的所有触发器
~~~
SHOW TRIGGERS;
SHOW CREATE TRIGGER tgr_box_insert;
~~~

######FOR EACH ROW 的意思
FOR EACH ROW 表示行级触发器，每一行受到触发都会导致执行触发器中begin 。。 end之间的语句。
oracle中若不写FOR EACH ROW 则表示语句级别的触发器，语句级别的触发器无论影响多少行都只会执行一次。
mysql中目前不支持语句级别的触发器。所以在mysql中请一定加上FOR EACH ROW 。
