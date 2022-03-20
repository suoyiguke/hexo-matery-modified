---
title: mysql-索引优化特性之Semijoin-半连接.md
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
title: mysql-索引优化特性之Semijoin-半连接.md
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
###什么是semi-join？
所谓的semi-join是指semi-join子查询。 当一张表在另一张表找到匹配的记录之后，半连接（semi-jion）返回第一张表中的记录。

与条件连接相反，即使在右节点中找到几条匹配的记录，左节点 的表也只会返回一条记录。另外，右节点的表一条记录也不会返回。半连接通常使用IN  或 EXISTS 作为连接条件。 该子查询具有如下结构：

SELECT ... FROM outer_tables WHERE expr IN (SELECT ... FROM inner_tables ...) AND ...


>即在where条件的“IN”中的那个子查询就是semi-join

这种查询的特点是我们只关心outer_table中与semi-join相匹配的记录。
换句话说，最后的结果集是在outer_tables中的，而semi-join的作用只是对outer_tables中的记录进行筛选。这也是我们进行 semi-join优化的基础，即我们只需要从semi-join中获取到最少量的足以对outer_tables记录进行筛选的信息就足够了。

**所谓的最少量，体现到优化策略上就是如何去重。**
以如下语句为例：
~~~
select * from Country 
where 
  Country.Code in 
(select City.country 
                   from City 
                   where City.Population>1*1000*1000);

当中的semi-join： 
select City.country 
                   from City 
                   where City.Population>1*1000*1000
~~~
可能返回的结果集如下： China(Beijin), China(Shanghai), France(Paris)...
我们可以看到这里有2个China，分别来至2条城市记录Beijin和Shanghai, 但实际上我们只需要1个China就足够对outer_table 

Country进行筛选了。所以我们需要去重。

###Mysql支持的Semi-join策略

Mysql支持的semi-join策略主要有5个，它们分别为：








####Convert the subquery to a join
直接转为join
Convert the subquery to a join, or use table pullout and run the query as an inner join between subquery tables and outer tables. Table pullout pulls a table out from the subquery to the outer query.

####FirstMatch
 只选用内部表的第1条与外表匹配的记录。
FirstMatch: When scanning the inner tables for row combinations and there are multiple instances of a given value group, choose one rather than returning them all. This "shortcuts" scanning and eliminates production of unnecessary rows.
####LooseScan
把inner-table数据基于索引进行分组，取每组第一条数据进行匹配。
LooseScan: Scan a subquery table using an index that enables a single value to be chosen from each subquery's value group.

####Duplicate Weedout
使用临时表对semi-join产生的结果集去重。
Duplicate Weedout: Run the semijoin as if it was a join and remove duplicate records using a temporary table.

Using index; Start temporary
Using where
Using index; End temporary

Start temporary, End temporary
表示半连接中使用了DuplicateWeedout策略的临时表


####MaterializeScan
 将inner-table去重固化成临时表，遍历固化表，然后在outer-table上寻找匹配。


Materialize the subquery into an indexed temporary table that is used to perform a join, where the index is used to remove duplicates. The index might also be used later for lookups when joining the temporary table with the outer tables; if not, the table is scanned. For more information about materialization, see Section 8.2.2.2, “Optimizing Subqueries with Materialization”.


###开启半连接
mysql> SELECT @@optimizer_switch\G
*************************** 1\. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,
                    index_merge_sort_union=on,
                    index_merge_intersection=on,
                    engine_condition_pushdown=on,
                    index_condition_pushdown=on,
                    mrr=on,mrr_cost_based=on,
                    block_nested_loop=on,batched_key_access=off,
                    materialization=on,semijoin=on,loosescan=on,
                    firstmatch=on,
                    subquery_materialization_cost_based=on,
                    use_index_extensions=on


###Semijoin优化实战

下列join查询可能出现重复
~~~
SELECT class.class_num, class.class_name
    FROM class
    INNER JOIN roster
    WHERE class.class_num = roster.class_num;
~~~
However, the result lists each class once for each enrolled student. For the question being asked, this is unnecessary duplication of information.
但是，结果会为每个注册的学生列出一次每个班级。对于正在问的问题，这是不必要的信息重复。


Assuming that class_num is a primary key in the class table, duplicate suppression is possible by using SELECT DISTINCT, but it is inefficient to generate all matching rows first only to eliminate duplicates later.
The same duplicate-free result can be obtained by using a subquery:
**假设class_num是class表中的主键，通过使用SELECT DISTINCT可以抑制重复，但是先生成所有匹配的行，然后再消除重复是低效的。**

使用子查询可以获得相同的无重复结果:
~~~
SELECT class_num, class_name
    FROM class
    WHERE class_num IN
        (SELECT class_num FROM roster);
~~~
在这里，优化器可以认识到IN子句要求子查询只从花名册表中返回每个类号的一个实例。在这种情况下，查询可以使用半连接；也就是说，只返回类中与花名册中的行匹配的每一行的一个实例的操作。
包含EXISTS子查询谓词的以下语句相当于包含IN子查询谓词的前一条语句:
~~~
SELECT class_num, class_name
    FROM class
    WHERE EXISTS
        (SELECT * FROM roster WHERE class.class_num = roster.class_num);
~~~


###结论
有些join会出现重复，我们第一时间想到的是使用DISTINCT去重。但是这里是先join后去重，效率低。
我们完全可以先去重后join。
so，使用in或EXISTS子查询的Semijoin的方式可以优化之

###执行计划分析
1、使用join distinct
~~~
mysql> EXPLAIN SELECT DISTINCT
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code,
	b.bar_code,
	b.model 
FROM
	jg_gift_rule d
	JOIN jg_gift_rel_product c ON d.id = c.gift_rule_id
	JOIN stock_product_detail b ON c.sku = b.sku
	JOIN stock_product a ON a.spu = b.spu 
WHERE
	d.del_status = 0 
	AND now( ) BETWEEN d.gift_start_time 
	AND d.gift_end_time;
+----+--------------------+------------------+------------+-------+----------------------------+----------------------+---------+------------------+------+----------+-------------------------------------------+
| id | select_type        | table            | partitions | type  | possible_keys              | key                  | key_len | ref              | rows | filtered | Extra                                     |
+----+--------------------+------------------+------------+-------+----------------------------+----------------------+---------+------------------+------+----------+-------------------------------------------+
|  1 | PRIMARY            | d                | NULL       | index | PRIMARY,index3             | index3               | 22      | NULL             |    1 |   100.00 | Using where; Using index; Using temporary |
|  1 | PRIMARY            | c                | NULL       | ref   | idx_sku_gift_rule_id,index | idx_sku_gift_rule_id | 8       | my.d.id          |    1 |   100.00 | Using index                               |
|  1 | PRIMARY            | b                | NULL       | ref   | idx_sku_spu,index          | idx_sku_spu          | 302     | my.c.sku         |    1 |   100.00 | Using index                               |
|  1 | PRIMARY            | a                | NULL       | ref   | sp_idx_spu                 | sp_idx_spu           | 302     | my.b.spu         |    1 |   100.00 | Using index                               |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | idx_cat_no                 | idx_cat_no           | 768     | my.a.cat_root_no |    1 |   100.00 | Using where; Using index                  |
+----+--------------------+------------------+------------+-------+----------------------------+----------------------+---------+------------------+------+----------+-------------------------------------------+
5 rows in set (0.03 sec)


       "table": {
            "table_name": "d",
            "access_type": "index",
            "possible_keys": [
              "PRIMARY",
              "index3"
            ],
            "key": "index3",
            "used_key_parts": [
              "id",
              "del_status",
              "gift_start_time",
              "gift_end_time"
 
            ],
            "key_length": "22",
            "rows_examined_per_scan": 1,
            "rows_produced_per_join": 1,
            "filtered": "100.00",
            "using_index": true,
            "cost_info": {
              "read_cost": "1.00",
              "eval_cost": "0.20",
              "prefix_cost": "1.20",
              "data_read_per_join": "1K"
            },
            "used_columns": [
              "id",
              "gift_start_time",
              "gift_end_time",
              "del_status"
            ],
            "attached_condition": "((`my`.`d`.`del_status` = 0) and (<cache>(now()) between `my`.`d`.`gift_start_time` and `my`.`d`.`gift_end_time`))"
          }
        },
mysql> 
~~~

2、使用Semijoin ，d表出现 FirstMatch(a)
~~~
mysql> EXPLAIN SELECT
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code,
	b.bar_code,
	b.model 
FROM
	stock_product_detail b
	JOIN stock_product a ON a.spu = b.spu 
WHERE
	b.sku IN (
	SELECT
		c.sku 
	FROM
		jg_gift_rule d FORCE INDEX ( index3 )
		JOIN jg_gift_rel_product c ON d.id = c.gift_rule_id 
	WHERE
		d.del_status = 0 
		AND now( ) BETWEEN d.gift_start_time 
		AND d.gift_end_time 
	);
+----+--------------------+------------------+------------+-------+----------------------------+-------------+---------+-------------------------+------+----------+-----------------------------------------+
| id | select_type        | table            | partitions | type  | possible_keys              | key         | key_len | ref                     | rows | filtered | Extra                                   |
+----+--------------------+------------------+------------+-------+----------------------------+-------------+---------+-------------------------+------+----------+-----------------------------------------+
|  1 | PRIMARY            | b                | NULL       | index | idx_sku_spu,index          | idx_sku_spu | 1513    | NULL                    |    1 |   100.00 | Using index                             |
|  1 | PRIMARY            | a                | NULL       | ref   | sp_idx_spu                 | sp_idx_spu  | 302     | my.b.spu                |    1 |   100.00 | Using index                             |
|  1 | PRIMARY            | c                | NULL       | ref   | idx_sku_gift_rule_id,index | index       | 302     | my.b.sku                |    1 |   100.00 | Using index                             |
|  1 | PRIMARY            | d                | NULL       | ref   | index3                     | index3      | 10      | my.c.gift_rule_id,const |    1 |   100.00 | Using where; Using index; FirstMatch(a) |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | idx_cat_no                 | idx_cat_no  | 768     | my.a.cat_root_no        |    1 |   100.00 | Using where; Using index                |
+----+--------------------+------------------+------------+-------+----------------------------+-------------+---------+-------------------------+------+----------+-----------------------------------------+
5 rows in set (0.04 sec)

"table": {
          "table_name": "d",
          "access_type": "ref",
          "possible_keys": [
            "index3"
          ],
          "key": "index3",
          "used_key_parts": [
            "id",
            "del_status"
          ],
          "key_length": "10",
          "ref": [
            "my.c.gift_rule_id",
            "const"
          ],
          "rows_examined_per_scan": 1,
          "rows_produced_per_join": 1,
          "filtered": "100.00",
          "using_index": true,
          "first_match": "a",
          "cost_info": {
            "read_cost": "1.00",
            "eval_cost": "0.20",
            "prefix_cost": "4.80",
            "data_read_per_join": "1K"
          },
          "used_columns": [
            "id",
            "gift_start_time",
            "gift_end_time",
            "del_status"
          ],
          "attached_condition": "(<cache>(now()) between `my`.`d`.`gift_start_time` and `my`.`d`.`gift_end_time`)"
        }
      }
    ],
~~~

###出现半连接的例子

~~~
CREATE TABLE `jg_gift_rel_product`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `gift_rule_id` bigint(20) NOT NULL COMMENT '赠品规则id',
  `sku` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '触发赠品商品sku',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_sku_gift_rule_id`(`sku`, `gift_rule_id`) USING BTREE,
  INDEX `idx_gift_rule_id_sku`(`gift_rule_id`, `sku`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '触发赠品商品中间表' ROW_FORMAT = Dynamic;


CREATE TABLE `jg_gift_rule`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `platform_code` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '平台编号',
  `rule_type` tinyint(4) DEFAULT NULL COMMENT '赠品规则类型(0:买赠类A+B,1:买赠类AorB,2:满赠类)',
  `gift_rule_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '赠品规则名称',
  `trigger_type` tinyint(4) DEFAULT NULL COMMENT '触发类型',
  `gift_type` tinyint(4) DEFAULT NULL COMMENT '赠送类型(0:买x送x,1:买满x送1,2:买x送1,3:满即赠)',
  `gift_start_time` datetime(0) DEFAULT NULL COMMENT '赠品活动开始时间',
  `gift_end_time` datetime(0) DEFAULT NULL COMMENT '赠品活动结束时间',
  `gift_method` tinyint(4) DEFAULT NULL COMMENT '赠送方式(0:无,1:整个活动周期内,2:单个活动周期内，以工作日为界)',
  `satisfy_count` int(10) DEFAULT NULL COMMENT '满件数赠',
  `gift_count` int(10) DEFAULT NULL COMMENT '赠送件数',
  `gift_total_count` int(10) DEFAULT NULL COMMENT '赠送总件数',
  `gift_surplus_count` int(10) DEFAULT NULL COMMENT '剩余可赠送数量',
  `use_type` tinyint(4) DEFAULT NULL COMMENT '使用方式(仅满即赠使用0:无,1:结算金额,2:客户实付金额下拉选择)',
  `is_fold` tinyint(4) DEFAULT NULL COMMENT '是否叠加赠品(仅满即赠使用0:无,1:是,2:否)',
  `disabled_status` tinyint(4) UNSIGNED DEFAULT 0 COMMENT '禁用状态（0：启用 1：禁用）',
  `create_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '创建人编号',
  `create_time` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '创建人时间',
  `update_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '修改人编号',
  `update_time` datetime(0) DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  `del_status` tinyint(4) DEFAULT 0 COMMENT '删除状态（0：启用 1：禁用）',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_gift_start_time_gift_end_time_del_status`(`gift_start_time`, `gift_end_time`, `del_status`) USING BTREE
) ENGINE = InnoDB  CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '赠品规则表' ROW_FORMAT = Dynamic;

~~~



~~~
mysql> EXPLAIN
 SELECT a.id, a.gift_rule_id giftRuleId, a.sku
 FROM jg_gift_rel_product a
 WHERE a.gift_rule_id in (
 SELECT b.gift_rule_id
 FROM jg_gift_rel_product b
 LEFT JOIN jg_gift_rule a
 ON a.id = b.gift_rule_id
 WHERE DATE_FORMAT( a.gift_end_time, '%Y-%m-%d %H:%i:%s' )>= DATE_FORMAT( '2022-02-12 15:20:00.0', '%Y-%m-%d %H:%i:%s' ) AND DATE_FORMAT( '2022-02-12 15:20:00.0', '%Y-%m-%d %H:%i:%s' )>= DATE_FORMAT( a.gift_start_time, '%Y-%m-%d %H:%i:%s' ) AND b.sku = 'K.33.11231.202201170002' );
+----+-------------+-------+------------+--------+---------------------------------------------------------+----------------------+---------+------------------------------------+------+----------+------------------------------+
| id | select_type | table | partitions | type   | possible_keys                                           | key                  | key_len | ref                                | rows | filtered | Extra                        |
+----+-------------+-------+------------+--------+---------------------------------------------------------+----------------------+---------+------------------------------------+------+----------+------------------------------+
|  1 | SIMPLE      | b     | NULL       | ref    | idx_sku_gift_rule_id,idx_gift_rule_id_sku               | idx_sku_gift_rule_id | 302     | const                              |    1 |   100.00 | Using index; Start temporary |
|  1 | SIMPLE      | a     | NULL       | eq_ref | PRIMARY,idx_id_gift_start_time_gift_end_time_del_status | PRIMARY              | 8       | mgb_treasure_system.b.gift_rule_id |    1 |   100.00 | Using where                  |
|  1 | SIMPLE      | a     | NULL       | ref    | idx_gift_rule_id_sku                                    | idx_gift_rule_id_sku | 8       | mgb_treasure_system.b.gift_rule_id |    1 |   100.00 | Using index; End temporary   |
+----+-------------+-------+------------+--------+---------------------------------------------------------+----------------------+---------+------------------------------------+------+----------+------------------------------+
3 rows in set (0.03 sec)
~~~
