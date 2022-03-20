---
title: 复杂join写法和in写法的性能差异-猜测.md
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
title: 复杂join写法和in写法的性能差异-猜测.md
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
###join写法
~~~
mysql> EXPLAIN SELECT
	a.spu,
	'' customer_goods_name,
	a.product_name,
	b.sku,
	b.k3_code,
	b.bar_code,
	b.model,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) cat_name 
FROM
	stock_product a
	JOIN stock_product_detail b ON a.spu = b.spu
	JOIN jg_gift_rel_product c ON c.sku = b.sku
	JOIN jg_gift_rule d ON d.id = c.gift_rule_id 
	AND d.del_status = 0 
	AND now( ) BETWEEN d.gift_start_time 
	AND d.gift_end_time UNION ALL
SELECT
	a.spu,
	a.customer_goods_name,
	c.product_name,
	a.sku,
	a.k3_code,
	b.bar_code,
	b.model,
	( SELECT cat_name FROM `product_category` WHERE cat_no = c.cat_root_no LIMIT 1 ) cat_name 
FROM
	jg_customer_goods_relationship a
	JOIN stock_product_detail b ON a.sku = b.sku
	JOIN stock_product c ON c.spu = b.spu 
WHERE
	a.platform_code = 'P20220107035730004' 
	AND a.del_status = 0;
+----+--------------------+------------------+------------+-------+--------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------+---------+-----------------------------------+------+----------+--------------------------+
| id | select_type        | table            | partitions | type  | possible_keys                                                                                                                                    | key                                                          | key_len | ref                               | rows | filtered | Extra                    |
+----+--------------------+------------------+------------+-------+--------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------+---------+-----------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | d                | NULL       | index | PRIMARY,index2                                                                                                                                   | index2                                                       | 22      | NULL                              |   12 |     8.33 | Using where; Using index |
|  1 | PRIMARY            | c                | NULL       | ref   | idx_sku_gift_rule_id,idx_gift_rule_id_sku                                                                                                        | idx_gift_rule_id_sku                                         | 8       | mgb_treasure_system.d.id          |    1 |   100.00 | Using index              |
|  1 | PRIMARY            | b                | NULL       | ref   | sku_spu_k3_code_bar_code_model,spu_sku_k3_code_bar_code_model                                                                                    | sku_spu_k3_code_bar_code_model                               | 302     | mgb_treasure_system.c.sku         |    1 |   100.00 | Using index              |
|  1 | PRIMARY            | a                | NULL       | ref   | idx_spu_cat_root_no_product_name,index,idx_spu                                                                                                   | idx_spu_cat_root_no_product_name                             | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index              |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO                                                                                                                                     | INDEX_CAT_NO                                                 | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | Using index              |
|  3 | UNION              | a                | NULL       | ref   | idx_del_status_customer_goods_code,idx_sku_sku_platform_code`, _customer_goods_name,platform_code,del_status,spu,sku,k3_code,customer_goods_name | platform_code,del_status,spu,sku,k3_code,customer_goods_name | 304     | const,const                       |    4 |   100.00 | Using index              |
|  3 | UNION              | b                | NULL       | ref   | sku_spu_k3_code_bar_code_model,spu_sku_k3_code_bar_code_model                                                                                    | sku_spu_k3_code_bar_code_model                               | 302     | mgb_treasure_system.a.sku         |    1 |   100.00 | Using index              |
|  3 | UNION              | c                | NULL       | ref   | idx_spu_cat_root_no_product_name,index,idx_spu                                                                                                   | idx_spu_cat_root_no_product_name                             | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index              |
|  4 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO                                                                                                                                     | INDEX_CAT_NO                                                 | 303     | mgb_treasure_system.c.cat_root_no |    1 |   100.00 | Using index              |
+----+--------------------+------------------+------------+-------+--------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------+---------+-----------------------------------+------+----------+--------------------------+
9 rows in set (0.07 sec)

mysql> 
~~~



分析：以小表d表为外表，进行all index扫描。只需扫12行

再来看 改写为in的写法：以a表作为了外表。all index扫描需要 1129行。性能差

~~~
mysql> EXPLAIN SELECT
	a.spu,
	( SELECT customer_goods_name FROM jg_customer_goods_relationship WHERE platform_code = 'P20220107035613003' AND sku = b.sku LIMIT 1 ) customer_goods_name,
	a.product_name,
	b.sku,
	b.k3_code,
	b.bar_code,
	b.model,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) cat_name 
FROM
	stock_product a
	JOIN stock_product_detail b USING ( spu ) 
WHERE
	b.sku IN (
SELECT
	c.sku 
FROM
	jg_gift_rel_product c
	JOIN jg_gift_rule d ON d.id = c.gift_rule_id 
	AND d.del_status = 0 
	AND now( ) BETWEEN d.gift_start_time 
	AND d.gift_end_time UNION ALL
SELECT
	sku 
FROM
	jg_customer_goods_relationship 
WHERE
	platform_code = 'P20220107035613003');
+----+--------------------+--------------------------------+------------+--------+---------------------------------------------------------------------------------------------------------------+--------------------------------------------------+---------+------------------------------------+------+----------+--------------------------+
| id | select_type        | table                          | partitions | type   | possible_keys                                                                                                 | key                                              | key_len | ref                                | rows | filtered | Extra                    |
+----+--------------------+--------------------------------+------------+--------+---------------------------------------------------------------------------------------------------------------+--------------------------------------------------+---------+------------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | a                              | NULL       | index  | idx_spu_cat_root_no_product_name,index,idx_spu                                                                | idx_spu_cat_root_no_product_name                 | 1206    | NULL                               | 1129 |   100.00 | Using index              |
|  1 | PRIMARY            | b                              | NULL       | ref    | spu_sku_k3_code_bar_code_model                                                                                | spu_sku_k3_code_bar_code_model                   | 302     | mgb_treasure_system.a.spu          |    1 |   100.00 | Using where; Using index |
|  4 | DEPENDENT SUBQUERY | c                              | NULL       | ref    | idx_sku_gift_rule_id,idx_gift_rule_id_sku                                                                     | idx_sku_gift_rule_id                             | 302     | func                               |    1 |   100.00 | Using index              |
|  4 | DEPENDENT SUBQUERY | d                              | NULL       | eq_ref | PRIMARY,index2                                                                                                | PRIMARY                                          | 8       | mgb_treasure_system.c.gift_rule_id |    1 |     8.33 | Using where              |
|  5 | DEPENDENT UNION    | jg_customer_goods_relationship | NULL       | ref    | idx_sku_sku_platform_code`, _customer_goods_name,platform_code,del_status,spu,sku,k3_code,customer_goods_name | idx_sku_sku_platform_code`, _customer_goods_name | 604     | func,const                         |    1 |   100.00 | Using index              |
|  3 | DEPENDENT SUBQUERY | product_category               | NULL       | ref    | INDEX_CAT_NO                                                                                                  | INDEX_CAT_NO                                     | 303     | mgb_treasure_system.a.cat_root_no  |    1 |   100.00 | Using index              |
|  2 | DEPENDENT SUBQUERY | jg_customer_goods_relationship | NULL       | ref    | idx_sku_sku_platform_code`, _customer_goods_name,platform_code,del_status,spu,sku,k3_code,customer_goods_name | idx_sku_sku_platform_code`, _customer_goods_name | 604     | mgb_treasure_system.b.sku,const    |    1 |   100.00 | Using index              |
+----+--------------------+--------------------------------+------------+--------+---------------------------------------------------------------------------------------------------------------+--------------------------------------------------+---------+------------------------------------+------+----------+--------------------------+
7 rows in set (0.08 sec)

mysql> 
~~~

###查看性能消耗对比

"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "8.98"
},


query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "1938.54"
    },
