---
title: mysql-sql优化之-优化GROUP-BY-和-DISTINCT.md
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
title: mysql-sql优化之-优化GROUP-BY-和-DISTINCT.md
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
> 为严将军头，为嵇侍中血

###数据准备

创建表tb_point 表

~~~

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_point
-- ----------------------------
DROP TABLE IF EXISTS `tb_point`;
CREATE TABLE `tb_point`  (
  `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
  `create_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建日期',
  `update_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新日期',
  `sys_org_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属部门',
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '投放点',
  `address` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地址',
  `contacts` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系人',
  `phone_number` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系方式',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_point`(`name`, `create_time`, `address`, `contacts`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_point
-- ----------------------------
INSERT INTO `tb_point` VALUES ('1249603071806279681', 'qiyeuser', '2020-04-13 15:39:23', NULL, NULL, 'A03', '东风东路小学', '东风东路756号', '李科', '13688889999');
INSERT INTO `tb_point` VALUES ('1249603416783589378', 'qiyeuser', '2020-04-13 15:40:46', 'qiyeuser', '2020-04-15 12:02:01', 'A03', '广交会展馆', '天河区琶洲广交会展馆', '刘经理', '13467891234');
INSERT INTO `tb_point` VALUES ('1249881947077873666', 'qiyeuser', '2020-04-14 10:07:33', 'qiyeuser', '2020-04-14 11:03:45', 'A03', '414钟ll创建的投放点', '深圳市盐田区', '张恒', '15578464565');
INSERT INTO `tb_point` VALUES ('1249899261022179329', 'qiyeuser', '2020-04-14 11:16:20', NULL, NULL, 'A03', 'zll创建的投放点', '广州市天河区', 'zll', '15512345678');
INSERT INTO `tb_point` VALUES ('1249992791816146945', 'qiyeuser', '2020-04-14 17:28:00', NULL, NULL, 'A03', '2020创建1号投放点', '厦门市', 'Zhang', '1234567899');
INSERT INTO `tb_point` VALUES ('1249996228356214785', 'qiyeuser', '2020-04-14 17:41:39', NULL, NULL, 'A03', '17:42测试', '深圳市宝安区', 'Zhang', '12345678');
INSERT INTO `tb_point` VALUES ('1249996578001784834', 'qiyeuser', '2020-04-14 17:43:03', NULL, NULL, 'A03', '17:43测试', '深圳市宝安区', 'Zhang', '15579487');
INSERT INTO `tb_point` VALUES ('1249997067632250882', 'qiyeuser', '2020-04-14 17:44:59', NULL, NULL, 'A03', '17:45测试', '宝安区', 'zhong', '12345678');

SET FOREIGN_KEY_CHECKS = 1;
~~~
准备空的tb_box表
~~~

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_box
-- ----------------------------
DROP TABLE IF EXISTS `tb_box`;
CREATE TABLE `tb_box`  (
  `id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
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
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_sb_number`(`sb_number`) USING BTREE,
  INDEX `index_number`(`number`) USING BTREE,
  INDEX `index_point_id`(`point_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

~~~

函数

~~~
CREATE DEFINER=`root`@`%` PROCEDURE `insert_tb_box`(in start int(10),in max_num int(10))
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 set autocommit= 0;
 repeat
 set i=i+1;
 INSERT INTO `test`.`tb_box`(`id`, `create_by`, `create_time`, `update_by`, `update_time`, `sys_org_code`, `status`, `number`, `zi_number`, `house_address`, `sb_number`, `point_id`, `point`, `confirm`, `last_point`) VALUES ((start+i), rand_string(6), now(), rand_string(6), now(), 'A03', 0, rand_string(20), 'A001', '仓库1', rand_string(20), rand_string(20), NULL, 1, rand_string(30));
 until i=max_num end repeat;
commit;
end



CREATE DEFINER=`root`@`localhost` FUNCTION `rand_num`() RETURNS int(5)
begin
   declare i int default 0;
   set i=floor(100+rand()*10);
 return i;
 end



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
~~~

编写存储过程，给tb_box表添加100万条数据
~~~

delimiter $$
create procedure insert_tb_box(in start int(10),in max_num int(10))
begin
 declare i int default 0;
 /*把autocommit设置成0*/
 set autocommit= 0;
 repeat
 set i=i+1;
 INSERT INTO `test`.`tb_box`(`id`, `create_by`, `create_time`, `update_by`, `update_time`, `sys_org_code`, `status`, `number`, `zi_number`, `house_address`, `sb_number`, `point_id`, `point`, `confirm`, `last_point`) VALUES ((start+i), rand_string(6), now(), rand_string(6), now(), 'A03', 0, rand_string(20), 'A001', '仓库1', rand_string(20), rand_string(20), NULL, 1, rand_string(30));
 until i=max_num end repeat;
commit;
end $$

-- 生成 一百万条数据
call insert_tb_box(1,1000000);
~~~

修改关联数据
~~~
update tb_box SET point_id = '1249603071806279681'  WHERE MOD(id,4) = 0
update tb_box SET point_id = '1249603416783589378'  WHERE MOD(id,4) = 1
update tb_box SET point_id = '1249881947077873666'  WHERE MOD(id,4) = 2
update tb_box SET point_id = '1249899261022179329'  WHERE MOD(id,4) = 3

~~~

###GROUP BY 优化

######通常采用标识符做GROUP BY字段性能好于使用其他字段

> 这是使用 a.id分组优于使用a.name分组
~~~
SELECT
	a.id,
	a.NAME,
	count( b.id ) boxCount 
FROM
	tb_point a
	LEFT JOIN tb_box b ON a.id = b.point_id 
GROUP BY
	a.id
ORDER BY
	boxCount DESC
~~~
好于
~~~
SELECT
	a.id,
	a.NAME,
	count( b.id ) boxCount 
FROM
	tb_point a
	LEFT JOIN tb_box b ON a.id = b.point_id 
GROUP BY
	a.NAME
ORDER BY
	boxCount DESC
~~~

######使用数据量小表的id作为GRUOPBY字段性能优于使用数据量大表id

>尽管这里使用a.id 和b.id 当做分组字段，两个查询查出的数据不同

~~~
SELECT
	a.id,
	a.NAME,
	count( b.id ) boxCount 
FROM
	tb_point a
	LEFT JOIN tb_box b ON a.id = b.point_id 
GROUP BY
	a.id
ORDER BY
	boxCount DESC
~~~
优于

~~~
SELECT
	a.id,
	a.NAME,
	count( b.id ) boxCount 
FROM
	tb_point a
	LEFT JOIN tb_box b ON a.id = b.point_id 
GROUP BY
	b.id
ORDER BY
	boxCount DESC
~~~

######GRUOPBY和sql_mode的 ONLY_FULL_GROUP_BY冲突
在执行以下语句时会报错：
> 1055 - Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'test.a.id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by

~~~
  SELECT
    a.id,
    a.NAME,
    a.contacts,
    count( b.id ) boxCount 
FROM
    tb_point a
    LEFT JOIN tb_box b ON a.id = b.point_id 
    GROUP BY
    a.NAME
    
~~~

前面在https://www.jianshu.com/p/95e50fd017ea文章中有提到这个问题，是直接修改sql_mode将 ONLY_FULL_GROUP_BY直接干掉。但是在《高性能mysql》中有一段话是这样的：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7325064a5e91a795.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
作者并不提倡这么干，理由是： 当索引改变，或者优化器选择使用不同的优化策略时都可能导致结果不一样。并指出了不要因为偷懒而导致最后查询出现故障。要求始终使用含义明确的语法。这句话有点无法理解，文中提到的“故障”是什么呢？可能要到我遇到之后才会知道吧。。

那么既然指出不要直接修改 sql_mode，那么我们应该如何让冲突的GRUOPBY语句正确执行呢？

文中有提到，可以使用max()和min()函数来实现；但是这种方式使用max和min函数较真的人可能会说这样写的分组查询有问题，确实如此。但是如果更加在乎查询效率，这样做也无可厚非。
~~~
  SELECT
    max(a.id),
    a.NAME,
    max(a.contacts),
    count( b.id ) boxCount 
FROM
    tb_point a
    LEFT JOIN tb_box b ON a.id = b.point_id 
    GROUP BY
    a.NAME
    
~~~

如果，实在无法接受使用上面那种方式的话，可以这样使用子查询的方式来进行查询：
~~~	
SELECT
	a.id,
	a.NAME,
	a.contacts,
	IFNULL(b.ct ,0) ct
FROM
	tb_point a
	LEFT JOIN ( SELECT point_id, count( id ) AS ct FROM tb_box GROUP BY point_id ) b ON a.id = b.point_id
~~~

书上对于这种方式有描述如下：
这样写更满足关系理论，但是成本有点高，因为子查询需要填充临时表，而子查询中创建的临时表是没有任何索引的。
作者认为这样写对性能有影响。

但是从我测得结果来看，子查询的耗时反而更少。性能反而更佳。这个子查询耗时0.4秒。而使用max方式耗时0.8秒。几乎一倍。我的mysql版本是 `5.7.22-log`

> 最终的方案选择还是要以自己测试结果为准。如果理论和实践冲突，我选择相信自己的实践

为了解其中的原因，我们查看它的执行计划：
可见，因为子查询而产生了一层 DERIVED 临时表，但是这个临时表的Extra字段有显示 Using index、key里面显示自建索引。说明用到了索引。这是查询性能可观的一个重要原因吧；
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1683775afd272ac6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
另外我分别使用 SHOW PROFILE命令查看各部分耗时，对比之下。没看到有哪部分耗时差别特别大，使用JOIN、MAX 耗时比上子查询耗时都差不多是1倍

######GRUOP BY的排序优化

有些时候对一没有建立索引的字段，进行GRUOP BY时。会产生Using filesort 文件内排序。因为GRUOP BY是在排序的基础上进行分组的。

如下面sql：
~~~
	EXPLAIN
	 SELECT
    a.id,
    a.NAME,
    a.contacts,
    count( b.id ) boxCount 
FROM
    tb_point a
    LEFT JOIN tb_box b ON a.id = b.point_id 
    GROUP BY
    a.contacts
 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1651f7716070d733.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果业务上不对排序有要求。那么就可以禁止GRUOP BY的排序：

> 指定 ORDER BY NULL
~~~
	
	EXPLAIN
	 SELECT
    a.id,
    a.NAME,
    a.contacts,
    count( b.id ) boxCount 
FROM
    tb_point a
    LEFT JOIN tb_box b ON a.id = b.point_id 
    GROUP BY
    a.contacts
ORDER BY NULL
~~~
这样就把Using filesort给干掉了！ 执行时间 1.237
![image.png](https://upload-images.jianshu.io/upload_images/13965490-61b3dcee8cc3ad5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


当然，多数情况是多排序有要求的。此时也可以在GRUOP BY后面使用DESC和ASC关键字，使分组的结果集按需要的方向排序。如下：
~~~
	EXPLAIN
	 SELECT
    a.id,
    a.NAME,
    a.contacts,
    count( b.id ) boxCount 
FROM
    tb_point a
    LEFT JOIN tb_box b ON a.id = b.point_id 
    GROUP BY
    a.contacts DESC
~~~

######GROUP BY WITH ROLLUP  优化

分组查询的一个变种就是要求mysql对分组结果再进行一次超级聚合。可以使用GROUP BY WITH ROLLUP 来实现这种逻辑，但可能性能不佳。因为通过查询计划分析出它是使用 Using temporary; Using filesort 来实现的。

~~~
EXPLAIN
SELECT
    a.id,
    a.NAME,
    count( b.id ) boxCount 
FROM
    tb_point a
    LEFT JOIN tb_box b ON a.id = b.point_id 
GROUP BY
    a.id  WITH ROLLUP  
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5878dd997e1a674c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用WITH ROLLUP，查询时间2.531秒。不使用0.774 秒。

1、所以，很多时候。我们在应用程序中做超级聚合是最好的！

2、当然也可使用UNION ALL 来实现：

~~~
SELECT
    a.id,
    a.NAME,
    count( b.id ) boxCount 
FROM
    tb_point a
    LEFT JOIN tb_box b ON a.id = b.point_id 
GROUP BY
    a.id   
UNION ALL
 SELECT NULL id, null name ,COUNT(point_id) boxCount FROM tb_box 
		
~~~
> 时间 0.951秒

![image.png](https://upload-images.jianshu.io/upload_images/13965490-76ba5559db17eead.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、还可以通过FROM子句嵌套使用子查询：
~~~
SELECT
	a.id,
	a.NAME,
	count( b.id ) boxCount, 
	boxCounts
FROM
	tb_point a
	LEFT JOIN tb_box b ON a.id = b.point_id  JOIN ( SELECT NULL id, null name ,COUNT(point_id) boxCounts FROM tb_box ) tb 
GROUP BY
	a.id

~~~
> 时间0.944秒

![image.png](https://upload-images.jianshu.io/upload_images/13965490-361c932063211a69.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**4、 Using index for group-by  松散索引扫描**
