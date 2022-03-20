---
title: 关于多表JOIN的优化-猜测.md
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
title: 关于多表JOIN的优化-猜测.md
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
1、`错误` 多表关联中，至少有一张表的join字段上加索引，用不到。呈现 Using join buffer (Block Nested Loop)
因为两表关联字段上总是若都加索引，只是只有一边生效。所以我们尽量要让数据量大的表做为索引表（被驱动表）：

如下，a表的join无论如何都用不到索引。出现了Using join buffer (Block Nested Loop) 
~~~
mysql> 
	EXPLAIN SELECT 
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code k3Code,
	b.bar_code barCode,
	b.model 
FROM
	stock_product a 
	JOIN stock_product_detail b ON a.spu = b.spu
	JOIN jg_gift_rel_product c  ON c.sku = b.sku
	JOIN jg_gift_rule d ON d.id = c.gift_rule_id 
WHERE
	DATE_FORMAT( d.gift_end_time, '%Y-%m-%d %h:%i:%s' ) >= DATE_FORMAT( NOW( ), '%Y-%m-%d %h:%i:%s' ) 
	AND DATE_FORMAT( NOW( ), '%Y-%m-%d %h:%i:%s' ) >= DATE_FORMAT( d.gift_start_time, '%Y-%m-%d %h:%i:%s' ) 
	AND d.del_status = 0
    -> ;
+----+--------------------+------------------+------------+------+-----------------------------------------------+----------------------+---------+----------------------------------------------------+------+----------+---------------------------------------+
| id | select_type        | table            | partitions | type | possible_keys                                 | key                  | key_len | ref                                                | rows | filtered | Extra                                 |
+----+--------------------+------------------+------------+------+-----------------------------------------------+----------------------+---------+----------------------------------------------------+------+----------+---------------------------------------+
|  1 | PRIMARY            | d                | NULL       | ALL  | PRIMARY                                       | NULL                 | NULL    | NULL                                               |    1 |   100.00 | Using where                           |
|  1 | PRIMARY            | a                | NULL       | ALL  | sp_idx_spu                                    | NULL                 | NULL    | NULL                                               | 1125 |   100.00 | Using join buffer (Block Nested Loop) |
|  1 | PRIMARY            | b                | NULL       | ref  | idx_spu_sku                                   | idx_spu_sku          | 302     | mgb_treasure_system.a.spu                          |    1 |   100.00 | NULL                                  |
|  1 | PRIMARY            | c                | NULL       | ref  | idx_sku,idx_gift_rule_id,idx_gift_sku_rule_id  | idx_gift_sku_rule_id | 310     | mgb_treasure_system.d.id,mgb_treasure_system.b.sku |    1 |   100.00 | Using index                           |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref  | INDEX_CAT_NO                                  | INDEX_CAT_NO         | 303     | mgb_treasure_system.a.cat_root_no                  |    1 |   100.00 | NULL                                  |
+----+--------------------+------------------+------------+------+-----------------------------------------------+----------------------+---------+----------------------------------------------------+------+----------+---------------------------------------+
5 rows in set (0.07 sec)

mysql> 
~~~
> 经过我的验证，这个结论是错误的。我们理论上可以完全消除Using join buffer (Block Nested Loop)！
然后这个结论中，把Using join buffer (Block Nested Loop)改为`ALL` 就是正确的了。确实最少需要一个表是ALL全表扫描查询的（只有join的情况，没有where条件）


2、`正确` 按照小表驱动大表原则，上面的查询性能不是最佳！不能让商品表（大表）stock_product 当驱动表！不能让他走ALL全表扫描！我们宁愿让多表join的其它小表做驱动表进行ALL扫描！




3、`正确` 只调整表的关联顺序，没什么卵用
~~~
sql> 
EXPLAIN SELECT
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code k3Code,
	b.bar_code barCode,
	b.model 
FROM
	jg_gift_rule d
	 join  jg_gift_rel_product c ON d.id = c.gift_rule_id
	 join   stock_product_detail b ON c.sku = b.sku
	 join   stock_product a ON a.spu = b.spu
WHERE
	DATE_FORMAT( d.gift_end_time, '%Y-%m-%d %h:%i:%s' ) >= DATE_FORMAT( NOW( ), '%Y-%m-%d %h:%i:%s' ) 
	AND DATE_FORMAT( NOW( ), '%Y-%m-%d %h:%i:%s' ) >= DATE_FORMAT( d.gift_start_time, '%Y-%m-%d %h:%i:%s' ) 
	AND d.del_status = 0;
+----+--------------------+------------------+------------+------+-----------------------------------------------+----------------------+---------+----------------------------------------------------+------+----------+---------------------------------------+
| id | select_type        | table            | partitions | type | possible_keys                                 | key                  | key_len | ref                                                | rows | filtered | Extra                                 |
+----+--------------------+------------------+------------+------+-----------------------------------------------+----------------------+---------+----------------------------------------------------+------+----------+---------------------------------------+
|  1 | PRIMARY            | d                | NULL       | ALL  | PRIMARY                                       | NULL                 | NULL    | NULL                                               |    1 |   100.00 | Using where                           |
|  1 | PRIMARY            | a                | NULL       | ALL  | sp_idx_spu                                    | NULL                 | NULL    | NULL                                               | 1125 |   100.00 | Using join buffer (Block Nested Loop) |
|  1 | PRIMARY            | b                | NULL       | ref  | idx_spu_sku                                   | idx_spu_sku          | 302     | mgb_treasure_system.a.spu                          |    1 |   100.00 | NULL                                  |
|  1 | PRIMARY            | c                | NULL       | ref  | idx_sku,idx_gift_rule_id,idx_gift_sku_rule_id | idx_gift_sku_rule_id | 310     | mgb_treasure_system.d.id,mgb_treasure_system.b.sku |    1 |   100.00 | Using index                           |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref  | INDEX_CAT_NO                                  | INDEX_CAT_NO         | 303     | mgb_treasure_system.a.cat_root_no                  |    1 |   100.00 | NULL                                  |
+----+--------------------+------------------+------------+------+-----------------------------------------------+----------------------+---------+----------------------------------------------------+------+----------+---------------------------------------+
5 rows in set (0.04 sec)

mysql> 
~~~





4、`正确`  all的表就是驱动表
~~~
EXPLAIN SELECT
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code k3Code,
	b.bar_code barCode,
	b.model 
FROM
	stock_product_detail b
	JOIN stock_product a ON a.spu = b.spu
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3e2d23fffc9b4635.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们现在使用straight_join 指定b为驱动表

~~~
EXPLAIN SELECT
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code k3Code,
	b.bar_code barCode,
	b.model 
FROM
	stock_product_detail b
	straight_join stock_product a ON a.spu = b.spu

~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-98fa68a4859eaa34.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###终极方案
- 这样只有小表d是All全表扫描的，之前大表a被全表扫描可真的效率差！
- rows 也减少到了13
- 消除了NLJ (Using join buffer (Block Nested Loop)

~~~
mysql>  EXPLAIN SELECT 
    a.spu,
    a.product_name productName,
    ( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
    b.sku,
    b.k3_code k3Code,
    b.bar_code barCode,
    b.model 
FROM
    stock_product a 
    JOIN stock_product_detail b ON a.spu = b.spu
    JOIN jg_gift_rel_product c  ON c.sku = b.sku
    JOIN jg_gift_rule d ON d.id = c.gift_rule_id 
WHERE
    DATE_FORMAT( d.gift_end_time, '%Y-%m-%d %h:%i:%s' ) >= DATE_FORMAT( NOW( ), '%Y-%m-%d %h:%i:%s' ) 
    AND DATE_FORMAT( NOW( ), '%Y-%m-%d %h:%i:%s' ) >= DATE_FORMAT( d.gift_start_time, '%Y-%m-%d %h:%i:%s' ) 
    AND d.del_status = 0;
	
+----+--------------------+------------------+------------+------+----------------------+----------------------+---------+-----------------------------------+------+----------+-------------+
| id | select_type        | table            | partitions | type | possible_keys        | key                  | key_len | ref                               | rows | filtered | Extra       |
+----+--------------------+------------------+------------+------+----------------------+----------------------+---------+-----------------------------------+------+----------+-------------+
|  1 | PRIMARY            | d                | NULL       | ALL  | PRIMARY              | NULL                 | NULL    | NULL                              |    1 |   100.00 | Using where |
|  1 | PRIMARY            | c                | NULL       | ref  | idx_gift_rule_id_sku | idx_gift_rule_id_sku | 8       | mgb_treasure_system.d.id          |    9 |   100.00 | Using index |
|  1 | PRIMARY            | b                | NULL       | ref  | idx_sku_spu          | idx_sku_spu          | 302     | mgb_treasure_system.c.sku         |    1 |   100.00 | NULL        |
|  1 | PRIMARY            | a                | NULL       | ref  | sp_idx_spu           | sp_idx_spu           | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | NULL        |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref  | INDEX_CAT_NO         | INDEX_CAT_NO         | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | NULL        |
+----+--------------------+------------------+------------+------+----------------------+----------------------+---------+-----------------------------------+------+----------+-------------+
5 rows in set (0.04 sec)

mysql> 
~~~

####方案和之前的区别在于索引结构不同
现在的结构：




###表结构

stock_product（a表）   加上 (`spu`) 索引即可
~~~
CREATE TABLE `stock_product` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `spu` varchar(100) NOT NULL COMMENT '商品编号',
  `supplier_no` varchar(200) DEFAULT NULL COMMENT '供应商编号',
  `cat_root_no` varchar(100) NOT NULL COMMENT '父级品类编号',
  `cat_parent_no` varchar(100) NOT NULL COMMENT '二级品类编号',
  `cat_child_no` varchar(100) NOT NULL COMMENT '三级品类编号',
  `brand_no` varchar(100) NOT NULL COMMENT '品牌编号',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
  `dosc` varchar(255) DEFAULT NULL COMMENT '产品描述',
  `company` varchar(50) DEFAULT NULL COMMENT '单位',
  `shelf_life` varchar(100) DEFAULT NULL COMMENT '保质期周期',
  `replace_send_tag` int(2) NOT NULL DEFAULT '1' COMMENT '是否支持代发(0否1是 2代发集采均可)',
  `replace_send_email` varchar(100) DEFAULT NULL COMMENT '代发邮箱',
  `replace_send_times` varchar(100) DEFAULT NULL COMMENT '代发时效',
  `replace_send_frequency` varchar(100) DEFAULT NULL COMMENT '代发频次',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `terms_no_array` text COMMENT '售后条款(,分割)',
  `state` int(2) NOT NULL COMMENT '状态(0已上架 1已下架 )',
  `logistics_no` varchar(100) DEFAULT NULL COMMENT '发货物流编号(代发为空)',
  `create_time` datetime NOT NULL,
  `create_user` varchar(255) NOT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_user` varchar(255) DEFAULT NULL,
  `specs` json DEFAULT NULL,
  `images` json DEFAULT NULL,
  `cat_data` json DEFAULT NULL,
  `is_combination` tinyint(4) DEFAULT '0' COMMENT '是否组合商品（0：否，1：是）',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `sp_idx_spu` (`spu`)
) ENGINE=InnoDB AUTO_INCREMENT=1441 DEFAULT CHARSET=utf8 COMMENT='商品库'
~~~

stock_product_detail（b表），加上 (`sku`,`spu`)组合索引，sku要在spu之前
~~~
CREATE TABLE `stock_product_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `spu` varchar(100) NOT NULL COMMENT '商品编号',
  `sku` varchar(100) NOT NULL COMMENT 'sku编号',
  `gy_code` varchar(100) DEFAULT NULL COMMENT '管易商品编号',
  `gy_name` varchar(100) DEFAULT NULL COMMENT '管易商品名称',
  `k3_code` varchar(100) DEFAULT NULL COMMENT '金蝶条码',
  `first_tag` int(2) DEFAULT NULL COMMENT '优先发货(0是 1否)',
  `stock` int(10) DEFAULT NULL COMMENT '管易商品库存',
  `bar_code` varchar(100) DEFAULT NULL COMMENT '国际条形码',
  `market_price` decimal(10,2) DEFAULT NULL COMMENT '市场价',
  `vat_rate` int(5) DEFAULT NULL COMMENT '税率',
  `proposal_price` decimal(10,2) DEFAULT NULL COMMENT '建议价',
  `settle_price` decimal(10,2) DEFAULT NULL COMMENT '代发价',
  `settle_profit` decimal(10,2) DEFAULT NULL COMMENT '代发毛利',
  `settle_profit_rate` decimal(10,2) DEFAULT NULL COMMENT '代发毛利率',
  `purchase_price` decimal(10,2) DEFAULT NULL COMMENT '集采价',
  `purchase_num` int(11) DEFAULT NULL COMMENT '起订量',
  `flag_acces_no` varchar(100) DEFAULT NULL COMMENT '辅料编号',
  `create_time` datetime NOT NULL,
  `create_user` varchar(255) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_user` varchar(255) DEFAULT NULL,
  `spec_data` json DEFAULT NULL,
  `size` varchar(100) DEFAULT NULL COMMENT '尺寸',
  `weight` varchar(100) DEFAULT NULL COMMENT '毛重',
  `box_gauge` varchar(100) DEFAULT NULL COMMENT '箱规',
  `model` varchar(100) DEFAULT NULL COMMENT '型号',
  `logistics_price` decimal(10,2) unsigned zerofill DEFAULT NULL COMMENT '运费',
  `sale_price` decimal(10,2) DEFAULT NULL COMMENT '0扣点一件代发常规价',
  `gross_profit` decimal(10,2) DEFAULT NULL COMMENT '代发常规价毛利',
  `gross_profit_rate` double(10,4) DEFAULT NULL COMMENT '代发常规价毛利率(%)',
  `activity_price` decimal(10,2) DEFAULT NULL COMMENT '0扣点一件代发活动价',
  `activity_profit` decimal(10,2) DEFAULT NULL COMMENT '代发活动价毛利',
  `activity_profit_rate` decimal(10,4) DEFAULT NULL COMMENT '代发活动价毛利率(%)',
  `collect_sale_price` decimal(10,2) DEFAULT NULL COMMENT '0扣点集采常规价',
  `collect_gross_profit` decimal(10,2) DEFAULT NULL COMMENT '集采常规价毛利',
  `collect_gross_profit_rate` decimal(10,2) DEFAULT NULL COMMENT '集采常规价毛利率(%)',
  `collect_activity_price` decimal(10,2) DEFAULT NULL COMMENT '0扣点集采活动价',
  `collect_activity_profit` decimal(10,2) DEFAULT NULL COMMENT '集采活动价毛利',
  `collect_activity_profit_rate` decimal(10,2) DEFAULT NULL COMMENT '集采活动价毛利率(%)',
  `flag_price` decimal(10,2) DEFAULT NULL COMMENT '辅料价格',
  `flag_name` varchar(255) DEFAULT NULL COMMENT '辅料名称',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_sku_spu` (`sku`,`spu`)
) ENGINE=InnoDB AUTO_INCREMENT=1700 DEFAULT CHARSET=utf8 COMMENT='商品库商品sku详情'
~~~

jg_gift_rel_product（c表 ），加上(`gift_rule_id`,`sku`)索引，注意组合索引的顺序！别把sku写到前面
~~~
CREATE TABLE `jg_gift_rel_product` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `gift_rule_id` bigint(20) NOT NULL COMMENT '赠品规则id',
  `sku` varchar(100) NOT NULL COMMENT '触发赠品商品sku',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_sku_gift_rule_id` (`gift_rule_id`,`sku`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3239 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='触发赠品商品中间表'
~~~


jg_gift_rule（d表） 关联字段上面不用加索引
~~~
CREATE TABLE `jg_gift_rule` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `platform_code` varchar(100) NOT NULL COMMENT '平台编号',
  `rule_type` tinyint(4) DEFAULT NULL COMMENT '赠品规则类型(0:买赠类A+B,1:买赠类AorB,2:满赠类)',
  `gift_rule_name` varchar(100) DEFAULT NULL COMMENT '赠品规则名称',
  `trigger_type` tinyint(4) DEFAULT NULL COMMENT '触发类型',
  `gift_type` tinyint(4) DEFAULT NULL COMMENT '赠送类型(0:买x送x,1:买满x送1,2:买x送1,3:满即赠)',
  `gift_start_time` datetime DEFAULT NULL COMMENT '赠品活动开始时间',
  `gift_end_time` datetime DEFAULT NULL COMMENT '赠品活动结束时间',
  `gift_method` tinyint(4) DEFAULT NULL COMMENT '赠送方式(0:无,1:整个活动周期内,2:单个活动周期内，以工作日为界)',
  `satisfy_count` int(10) DEFAULT NULL COMMENT '满件数赠',
  `gift_count` int(10) DEFAULT NULL COMMENT '赠送件数',
  `gift_total_count` int(10) DEFAULT NULL COMMENT '赠送总件数',
  `gift_surplus_count` int(10) DEFAULT NULL COMMENT '剩余可赠送数量',
  `use_type` tinyint(4) DEFAULT NULL COMMENT '使用方式(仅满即赠使用0:无,1:结算金额,2:客户实付金额下拉选择)',
  `is_fold` tinyint(4) DEFAULT NULL COMMENT '是否叠加赠品(仅满即赠使用0:无,1:是,2:否)',
  `disabled_status` tinyint(4) unsigned DEFAULT '0' COMMENT '禁用状态（0：启用 1：禁用）',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人编号',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建人时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '修改人编号',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  `del_status` tinyint(4) DEFAULT '0' COMMENT '删除状态（0：启用 1：禁用）',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='赠品规则表'
~~~



>多表JOIN优化时。4个表关联需要建立3 个索引，其中2个为组合索引，组合索引的顺序不要错了、1个为单值索引。


###`正确`怎么判断索引在join中生效了？
索引在join中生效时，type等于ref，key中有值，ref中有值，Extra中没有using join buffer，row值大幅度减少。


###后续优化d上的where条件

d表索引再添加
~~~
CREATE TABLE `mgb_treasure_system`.`jg_gift_rule`  (
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index`(`gift_start_time`, `gift_end_time`, `del_status`) USING BTREE,
  INDEX `del_status`(`del_status`) USING BTREE,
  INDEX `gift_start_time`(`gift_start_time`) USING BTREE,
  INDEX `gift_end_time`(`gift_end_time`) USING BTREE,
  INDEX `gift_start_time_gift_end_time`(`gift_start_time`, `gift_end_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '赠品规则表' ROW_FORMAT = Dynamic;
~~~

d表的type从ALL变为index，且key用到了索引
~~~
mysql> EXPLAIN SELECT 
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code k3Code,
	b.bar_code barCode,
	b.model 
FROM
	stock_product a
	JOIN stock_product_detail b ON a.spu = b.spu
	JOIN jg_gift_rel_product c ON c.sku = b.sku
	JOIN jg_gift_rule d force index(`index`) ON d.id = c.gift_rule_id 
WHERE
 d.del_status = 0 and
	now() BETWEEN d.gift_start_time 
	AND d.gift_end_time;
+----+--------------------+------------------+------------+-------+---------------------+---------------------+---------+-----------------------------------+------+----------+--------------------------+
| id | select_type        | table            | partitions | type  | possible_keys       | key                 | key_len | ref                               | rows | filtered | Extra                    |
+----+--------------------+------------------+------------+-------+---------------------+---------------------+---------+-----------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | d                | NULL       | index | index               | index               | 14      | NULL                              |    1 |   100.00 | Using where; Using index |
|  1 | PRIMARY            | c                | NULL       | ref   | jg_gift_rel_product | jg_gift_rel_product | 8       | mgb_treasure_system.d.id          |    9 |   100.00 | Using index              |
|  1 | PRIMARY            | b                | NULL       | ref   | idx_sku_spu         | idx_sku_spu         | 302     | mgb_treasure_system.c.sku         |    1 |   100.00 | NULL                     |
|  1 | PRIMARY            | a                | NULL       | ref   | sp_idx_spu          | sp_idx_spu          | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | NULL                     |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO        | INDEX_CAT_NO        | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | NULL                     |
+----+--------------------+------------------+------------+-------+---------------------+---------------------+---------+-----------------------------------+------+----------+--------------------------+
5 rows in set (0.08 sec)

mysql> 
~~~

添加不同的索引结构集合，可以得到key_len = 14时三个条件都有用上！

>del_status key_len=2 Using where
		gift_start_time key_len=6 Using where
    gift_end_time key_len=6 Using where
    gift_start_time_gift_end_time key_len=6 Using index condition; Using where
		index  key_len=14 Using where; Using index
		

把del_status放到前面，貌似执行计划变得更好了：type变ref,ref变const
~~~
  INDEX `index2`(`del_status`, `gift_start_time`, `gift_end_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '赠品规则表' ROW_FORMAT = Dynamic;
~~~
~~~
mysql> EXPLAIN SELECT 
	a.spu,
	a.product_name productName,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) catName,
	b.sku,
	b.k3_code k3Code,
	b.bar_code barCode,
	b.model 
FROM
	stock_product a
	JOIN stock_product_detail b ON a.spu = b.spu
	JOIN jg_gift_rel_product c ON c.sku = b.sku
	JOIN jg_gift_rule d force index(`index2`) ON d.id = c.gift_rule_id 
WHERE
 d.del_status = 0 and
	now() BETWEEN d.gift_start_time 
	AND d.gift_end_time;
+----+--------------------+------------------+------------+------+---------------------+---------------------+---------+-----------------------------------+------+----------+--------------------------+
| id | select_type        | table            | partitions | type | possible_keys       | key                 | key_len | ref                               | rows | filtered | Extra                    |
+----+--------------------+------------------+------------+------+---------------------+---------------------+---------+-----------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | d                | NULL       | ref  | index2              | index2              | 2       | const                             |    1 |   100.00 | Using where; Using index |
|  1 | PRIMARY            | c                | NULL       | ref  | jg_gift_rel_product | jg_gift_rel_product | 8       | mgb_treasure_system.d.id          |    9 |   100.00 | Using index              |
|  1 | PRIMARY            | b                | NULL       | ref  | idx_sku_spu         | idx_sku_spu         | 302     | mgb_treasure_system.c.sku         |    1 |   100.00 | NULL                     |
|  1 | PRIMARY            | a                | NULL       | ref  | sp_idx_spu          | sp_idx_spu          | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | NULL                     |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref  | INDEX_CAT_NO        | INDEX_CAT_NO        | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | NULL                     |
+----+--------------------+------------------+------------+------+---------------------+---------------------+---------+-----------------------------------+------+----------+--------------------------+
5 rows in set (0.06 sec)

~~~



###继续在之前的基础上使用索引覆盖优化


~~~
mysql> 
 
 EXPLAIN SELECT a.spu, a.product_name productName, (
 SELECT cat_name
 FROM `product_category`
 WHERE cat_no = a.cat_root_no
 LIMIT 1 ) catName, b.sku, b.k3_code k3Code, b.bar_code barCode, b.model
 FROM stock_product a  JOIN stock_product_detail b 
 ON a.spu = b.spu JOIN jg_gift_rel_product c
 ON c.sku = b.sku JOIN jg_gift_rule d
 ON d.id = c.gift_rule_id
 WHERE d.del_status = 0 AND now( ) BETWEEN d.gift_start_time AND d.gift_end_time;
+----+--------------------+------------------+------------+------+------------------------------------------------------+----------------------------------------------+---------+-----------------------------------+------+----------+--------------------------+
| id | select_type        | table            | partitions | type | possible_keys                                        | key                                          | key_len | ref                               | rows | filtered | Extra                    |
+----+--------------------+------------------+------------+------+------------------------------------------------------+----------------------------------------------+---------+-----------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | d                | NULL       | ref  | PRIMARY,idx_del_status_gift_start_time_gift_end_time | idx_del_status_gift_start_time_gift_end_time | 2       | const                             |    2 |    50.00 | Using where; Using index |
|  1 | PRIMARY            | c                | NULL       | ref  | idx_gift_rule_id_sku                                 | idx_gift_rule_id_sku                         | 8       | mgb_treasure_system.d.id          |    7 |   100.00 | Using index              |
|  1 | PRIMARY            | b                | NULL       | ref  | index                                                | index                                        | 302     | mgb_treasure_system.c.sku         |    1 |   100.00 | Using index              |
|  1 | PRIMARY            | a                | NULL       | ref  | idx_spu_cat_root_no_product_name                     | idx_spu_cat_root_no_product_name             | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index              |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref  | INDEX_CAT_NO                                         | INDEX_CAT_NO                                 | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | Using index              |
+----+--------------------+------------------+------------+------+------------------------------------------------------+----------------------------------------------+---------+-----------------------------------+------+----------+--------------------------+
5 rows in set (0.05 sec)

mysql> 
~~~




表结构

~~~
CREATE TABLE `stock_product` (
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_spu_cat_root_no_product_name` (`spu`,`cat_root_no`,`product_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1442 DEFAULT CHARSET=utf8 COMMENT='商品库'

CREATE TABLE `stock_product_detail` (
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index` (`sku`,`spu`,`k3_code`,`bar_code`,`model`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1701 DEFAULT CHARSET=utf8 COMMENT='商品库商品sku详情'

CREATE TABLE `jg_gift_rel_product` (
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_gift_rule_id_sku` (`gift_rule_id`,`sku`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3281 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='触发赠品商品中间表'


CREATE TABLE `jg_gift_rule` (
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_del_status_gift_start_time_gift_end_time` (`del_status`,`gift_start_time`,`gift_end_time`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='赠品规则表'
~~~




