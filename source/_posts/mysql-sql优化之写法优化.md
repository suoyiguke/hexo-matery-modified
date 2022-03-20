---
title: mysql-sql优化之写法优化.md
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
title: mysql-sql优化之写法优化.md
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
###1、sql语句各个部分执行顺序
~~~
FROM
<left_table>

ON
<join_condition>

<join_type>
 JOIN
<right_table>

WHERE
<where_condition>

GROUP BY
<group_by_list>

HAVING
<having_condition>

SELECT

DISTINCT
<select_list>

ORDER BY
<order_by_condition>

LIMIT
<limit_number>
~~~


###2、混合排序
MySQL 不能利用索引进行混合排序，若有两个字段作为排序条件，一个升一个降那么排序时就用不到索引了。但在某些场景，还是有机会使用特殊方法提升性能的。如下：
~~~
SELECT
	* 
FROM
	my_order o
	INNER JOIN my_appraise a ON a.orderid = o.id 
ORDER BY
	a.is_reply ASC,
	a.appraise_time DESC 
	LIMIT 0,
	20
~~~

is_reply 字段值是确定的0或者1，那么上面的sql就根据is_reply使用 UNION ALL 拆开来：

~~~
SELECT *
FROM   ((SELECT *
         FROM   my_order o
                INNER JOIN my_appraise a
                        ON a.orderid = o.id
                           AND is_reply = 0
         ORDER  BY appraise_time DESC
         LIMIT  0, 20)
        UNION ALL
        (SELECT *
         FROM   my_order o
                INNER JOIN my_appraise a
                        ON a.orderid = o.id
                           AND is_reply = 1
         ORDER  BY appraise_time DESC
         LIMIT  0, 20)) t
ORDER  BY  is_reply ASC,
          appraisetime DESC
LIMIT  20;

~~~

###3、提前缩小范围
~~~
SELECT *
FROM   my_order o
       LEFT JOIN my_userinfo u
              ON o.uid = u.uid
       LEFT JOIN my_productinfo p
              ON o.pid = p.pid
WHERE  ( o.display = 0 )
       AND ( o.ostaus = 1 )
ORDER  BY o.selltime DESC
LIMIT  0, 15
~~~



该SQL语句原意是：先做一系列的左连接，然后排序取前15条记录。从执行计划也可以看出，最后一步估算排序记录数为90万，时间消耗为12秒。
~~~
+----+-------------+-------+--------+---------------+---------+---------+-----------------+--------+----------------------------------------------------+
| id | select_type | table | type   | possible_keys | key     | key_len | ref             | rows   | Extra                                              |
+----+-------------+-------+--------+---------------+---------+---------+-----------------+--------+----------------------------------------------------+
|  1 | SIMPLE      | o     | ALL    | NULL          | NULL    | NULL    | NULL            | 909119 | Using where; Using temporary; Using filesort       |
|  1 | SIMPLE      | u     | eq_ref | PRIMARY       | PRIMARY | 4       | o.uid |      1 | NULL                                               |
|  1 | SIMPLE      | p     | ALL    | PRIMARY       | NULL    | NULL    | NULL            |      6 | Using where; Using join buffer (Block Nested Loop) |
+----+-------------+-------+--------+---------------+---------+---------+-----------------+--------+----------------------------------------------------+
~~~
由于最后 WHERE 条件以及排序均针对最左主表，因此可以先对 my_order 排序提前缩小数据量再做左连接。SQL 重写后如下，执行时间缩小为1毫秒左右。


~~~
SELECT *
FROM (
SELECT *
FROM   my_order o
WHERE  ( o.display = 0 )
       AND ( o.ostaus = 1 )
ORDER  BY o.selltime DESC
LIMIT  0, 15
) o
     LEFT JOIN my_userinfo u
              ON o.uid = u.uid
     LEFT JOIN my_productinfo p
              ON o.pid = p.pid
ORDER BY  o.selltime DESC
limit 0, 15

~~~

再检查执行计划：子查询物化后（select_type=DERIVED)参与 JOIN。虽然估算行扫描仍然为90万，但是利用了索引以及 LIMIT 子句后，实际执行时间变得很小。
~~~
+----+-------------+------------+--------+---------------+---------+---------+-------+--------+----------------------------------------------------+
| id | select_type | table      | type   | possible_keys | key     | key_len | ref   | rows   | Extra                                              |
+----+-------------+------------+--------+---------------+---------+---------+-------+--------+----------------------------------------------------+
|  1 | PRIMARY     | <derived2> | ALL    | NULL          | NULL    | NULL    | NULL  |     15 | Using temporary; Using filesort                    |
|  1 | PRIMARY     | u          | eq_ref | PRIMARY       | PRIMARY | 4       | o.uid |      1 | NULL                                               |
|  1 | PRIMARY     | p          | ALL    | PRIMARY       | NULL    | NULL    | NULL  |      6 | Using where; Using join buffer (Block Nested Loop) |
|  2 | DERIVED     | o          | index  | NULL          | idx_1   | 5       | NULL  | 909112 | Using where                                        |
+----+-------------+------------+--------+---------------+---------+---------+-------+--------+----------------------------------------------------+

~~~


###4、中间结果集下推

再来看下面这个已经初步优化过的例子(左连接中的主表优先作用查询条件)：
~~~
SELECT
	a.*,
	c.allocated 
FROM
	( 
	  SELECT resourceid FROM my_distribute d WHERE isdelete = 0 AND cusmanagercode = '1234567' ORDER BY salecode LIMIT 20 
	) a
	
	LEFT JOIN (
	
	SELECT resourcesid,sum( ifnull( allocation, 0 ) * 12345 ) allocated FROM my_resources GROUP BY  resourcesid 
	
	) c ON a.resourceid = c.resourcesid
~~~
那么该语句还存在其它问题吗？不难看出子查询 c 是全表聚合查询，在表数量特别大的情况下会导致整个语句的性能下降。


其实对于子查询 c，左连接最后结果集只关心能和主表 resourceid 能匹配的数据。因此我们可以重写语句如下，执行时间从原来的2秒下降到2毫秒。我们可以将a表中的条件放一份到b表中，提前进行过滤和筛选。这样b表只会统计符合r.resourcesid = a.resourcesid条件的 sum(ifnull(allocation, 0) * 12345) allocated 值，这样就避免统计一些我们不需要的冗余数据了。当然这个优化的前提是LEFT JOIN，a表是小表。若是inner join 就没什么区别了。

~~~
SELECT
	a.*,
	c.allocated 
FROM
	( 
	SELECT resourceid FROM my_distribute d WHERE isdelete = 0 AND cusmanagercode = '1234567' ORDER BY salecode LIMIT 20 
	) a
	LEFT JOIN (
	SELECT
		resourcesid,sum( ifnull( allocation, 0 ) * 12345 ) allocated 
	FROM
		my_resources r,
		( 
		SELECT resourceid FROM my_distribute d WHERE isdelete = 0 AND cusmanagercode = '1234567' ORDER BY salecode LIMIT 20 
		) a 
	WHERE r.resourcesid = a.resourcesid  GROUP BY resourcesid 
	) c ON a.resourceid = c.resourcesid
~~~
这个语句我们还可以进一步优化。子查询 a 在我们的SQL语句中出现了多次。这种写法不仅存在额外的开销，还使得整个语句显的繁杂。使用 WITH 语句再次重写：
~~~
WITH a AS ( 
SELECT resourceid FROM my_distribute d WHERE isdelete = 0 AND cusmanagercode = '1234567' ORDER BY salecode LIMIT 20 
) SELECT
a.*,
c.allocated 
FROM
	a
	LEFT JOIN (
	SELECT resourcesid, sum( ifnull( allocation, 0 ) * 12345 ) allocated FROM my_resources r, a WHERE r.resourcesid = a.resourcesid GROUP BY resourcesid 
	) c ON a.resourceid = c.resourcesid
~~~


当然在mysql中不能使用 SQLServer 中的 WITH a AS 语句来提出公共部分的查询，但也可利用视图实现

