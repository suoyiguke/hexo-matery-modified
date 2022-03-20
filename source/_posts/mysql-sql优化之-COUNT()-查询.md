---
title: mysql-sql优化之-COUNT()-查询.md
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
title: mysql-sql优化之-COUNT()-查询.md
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
>为张睢阳齿，为颜常山舌。


###关于COUNT()函数的几个谬误的纠正


1、COUNT(*) 其实不存在性能问题!

当我们使用COUNT(*)来统计返回结果集的行数的时候，这种情况下通配符 * 并不会像我们猜想的那样扩展所有的列，实际上，他会忽略所有的列而直接统计所有的行数。 -- 出自《高性能mysql》

那么就请放心大胆的使用count(*)吧！！

而且，就算使用的是COUNT(非空字段)。当mysql知道这个字段不为空时，底层也会将COUNT(非空字段)优化为COUNT(*)

2、请正确的统计行数
在括号里指定一个列，希望统计结果集的行数。如果希望得到结果集函数最好使用COUNT(*)，这样写意义清晰，性能也会很好。若不小心指定了一个可为NULL的列，那么统计结果就不正确了。

###MyISAM引擎表中count(*)为什么那么快？
在没有任何where条件下的COUNT(*)性能才是最棒的。如果缺失这个条件，性能也和INNODB相同

MyISAM引擎表中，在没有任何where条件时，mysql会利用MyISAM引擎的特性直接获取这个值；

相反，在有where条件时MyISAM引擎照样要和其它引擎一样要去执行扫描查询。这样速度就差不多了；

对于这个结论我们可以做一个实验，使用我之前写的文章https://www.jianshu.com/p/cec4a720e1b3中的tb_box表，它是INNODB的，所以我将之数据复制到另一张MYSIAM类型的tb_box_cp表。然后分别对两个表进行COUNT(*)对比下：

tb_box_cp 时间为 0.034秒
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4458e2c819c8a5c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

tb_box时间为 0.483秒，不是一个数量级的~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7af8616f5cc4eba5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


然后对tb_box、tb_box_cp 表的查询添加where条件，查询如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-79e73e326541c228.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以发现两者耗时差不多，验证了上面的结论是正确的！

我们可以使用执行计划分析下tb_box_cp查询为什么这么快：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e76b7f069f9180f0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> extra字段一段文字： Select tables optimized away；在MySQL官方站点翻到两段相关的描述，原文如下：
For explains on simple count queries (i.e. explain select count(*) from people) the extra section will read "Select tables optimized away." This is due to the fact that MySQL can read the result directly from the table internals and therefore does not need to perform the select. 意思是 ：
对于简单计数查询的解释(即从人员中解释选择计数(*))，额外部分将显示为“选择优化后的表”。这是因为`mysql可以直接从表内部读取结果，因此不需要执行select`。MyISAM表的COUNT(*) 就是一个常量。



###COUNT()的优化

#####1、存在范围条件，取反

之前说明了在MyISAM引擎表中，不是用where条件。那么COUNT(*)的速度非常快。那么如果我们一定要使用where条件呢？
如下：

~~~
SELECT
	count( * ) 
FROM
	tb_box_cp WHERE id >5
	
~~~

> 0.773秒

那么就可以使用速度非常快的COUNT(*)总数 -  id <=5数量
~~~
SELECT
	(SELECT count(*) from tb_box_cp ) - count( * ) 
FROM
	tb_box_cp WHERE id <=5
~~~

> 0.747秒，这速度也没差多少呀？而且要注意，这个方式只能用在MyISAM引擎表中喔！如果在INNODB中多使用一个COUNT(*) 想想性能是不是南辕北辙了呢？

#####2、在一个sql中统计字段的几种情况值数量
> 需求： 分别统计tb_box.point_id字段取值为1249603071806279681、1249603416783589378、1249881947077873666、1249899261022179329 的数量

1、我们可以使用SUM()配合IF()来实现
~~~
-- 0.773
SELECT
	SUM(IF(point_id='1249603071806279681',1,0)) AS a,SUM(IF(point_id='1249603416783589378',1,0)) AS b ,SUM(IF(point_id='1249881947077873666',1,0)) AS c,SUM(IF(point_id='1249899261022179329',1,0)) AS d 
FROM
	`tb_box`
~~~
> 查询时间  0.773秒

2、也可以使用COUNT()来实现
~~~
-- 0.682
	SELECT
	COUNT(point_id='1249603071806279681' OR NULL) AS a,COUNT(point_id='1249603416783589378'  OR NULL ) AS b ,COUNT(point_id='1249881947077873666'  OR NULL ) AS c,COUNT(point_id='1249899261022179329' OR NULL) AS d 
FROM
	`tb_box`
~~~
> 时间 0.682秒，COUNT()比SUM()稍微快点; 思考一下为什么要加上 OR NULL。因为只需要将满足条件的设置为真，不满足条件的设置为NULL，COUNT()不统计NULL。若不使用OR NULL，则每个数量都相同，统计的是整个tb_box的行数（point_id='1249603071806279681' 返回0或者1）。


#####3、使用近似值

有些业务场景并不需要完全精确的COUNT值。此时可以使用近似值来代替。EXPLAIN的ROWS字段就是一个不错的近似值。EXPLAIN并不需要真正的去执行查询，所以成本很低。

~~~
EXPLAIN SELECT
	COUNT( * ) 
FROM
	`tb_box`
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c3c6e9ddc8c6a3c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> 精确数量是100万，近似值90万

但是若加上where条件，这近似值离谱了
~~~
-- 451963 和 250005
EXPLAIN SELECT
	COUNT( * ) 
FROM
	`tb_box` WHERE point_id='1249603071806279681'  
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-984a1fed0136e69d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
> 精确数量20万，近似值40万；所以有where条件的时候还需斟酌使用

###比较FOUND_ROWS()和COUNT(*)性能

使用SELECT FOUND_ROWS();函数获得总行数需要现在之前limit语句中加上`SQL_CALC_FOUND_ROWS`。加了这个关键字后limit查询总是会扫描满足条件的行，然后抛弃掉不需要的行，而不是在满足limit行数之后就终止扫描。所以该提示的代价可能非常高。


~~~
SELECT SQL_CALC_FOUND_ROWS * FROM tb_box LIMIT   1000,10 
SELECT FOUND_ROWS();
~~~
> 因为每次LIMIT都需要扫描所有行。所以FOUND_ROWS()这个函数性能并不被看好。推荐使用COUNT(*)

###另外维护一个count数值，以空间换时间
#####1、使用汇总表，分散热点的方式
另外创建一个统计表，通过触发器来实现维护目表的数量。
1、添加汇总表
~~~
CREATE TABLE `test`.`tablecount`  (
  `id` tinyint(100) UNSIGNED NOT NULL COMMENT '槽',
  `cnt` bigint(255) NOT NULL COMMENT '数量',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~
然后插入100条数据，具体数目可以根据并发量调整

2、编写触发器，insert和delete之后都去维护这个表的数据
insert after
~~~
CREATE DEFINER = `root`@`%` TRIGGER `tgr_box_insert` AFTER INSERT ON `box_fenqu` FOR EACH ROW begin
  set @slot = FLOOR( 1 + RAND() * (101 - 1));
  UPDATE tablecount SET cnt = cnt +1  WHERE id = @slot;
end;
~~~

delete after
~~~
CREATE DEFINER = `root`@`%` TRIGGER `tgr_box_delete` AFTER DELETE ON `box_fenqu` FOR EACH ROW begin
  set @slot = FLOOR( 1 + RAND() * (101 - 1));
  UPDATE tablecount SET cnt = cnt -1  WHERE id = @slot;
end;
~~~
然后可以直接这样查询，只需0.02秒
~~~
SELECT SUM(cnt) from tablecount
~~~
> 汇总表的具体实现和思想可以看看这篇 https://www.jianshu.com/p/153e052765c0

#####2、使用外部缓存系统Memcached、redis



###分页时为什么要禁用count(*) 查询？

在分页查询中，我们需要查询count(*)得到总记录数进而算出总页数。这样就能实现`当前页`和`跳页`功能；但是当表数据量过于庞大时，就不推荐使用count(\*)了。我们只需要有上一页和下一页的分页功能即可！
