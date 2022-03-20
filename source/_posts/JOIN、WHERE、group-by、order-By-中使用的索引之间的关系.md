---
title: JOIN、WHERE、group-by、order-By-中使用的索引之间的关系.md
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
title: JOIN、WHERE、group-by、order-By-中使用的索引之间的关系.md
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
###JOIN 和 WHERE 二者用索引的优先级是一样的。先满足JOIN或WHERE都行。

####

先来看个执行计划：id=3的表a，type=index。ref为空。Extra 显示Using where; 说明有where字段没用索引
~~~
mysql>  EXPLAIN SELECT DISTINCT a.spu, '' customer_goods_name, a.product_name, b.sku, b.k3_code, b.bar_code, b.model, (
 SELECT cat_name
 FROM `product_category`
 WHERE cat_no = a.cat_root_no
 LIMIT 1 ) cat_name
 FROM stock_product a JOIN stock_product_detail b
 ON a.spu = b.spu JOIN jg_gift_rel_product c
 ON c.sku = b.sku JOIN jg_gift_rule d
 ON d.id = c.gift_rule_id AND d.del_status = 0 AND now( ) BETWEEN d.gift_start_time AND d.gift_end_time
 UNION ALL
 SELECT DISTINCT a.spu, a.customer_goods_name, c.product_name, a.sku, a.k3_code, b.bar_code, b.model, (
 SELECT cat_name
 FROM `product_category`
 WHERE cat_no = c.cat_root_no
 LIMIT 1 ) cat_name
 FROM jg_customer_goods_relationship a JOIN stock_product_detail b
 ON a.sku = b.sku JOIN stock_product c
 ON c.spu = b.spu
 WHERE a.platform_code = 'P20220107035520001' AND a.del_status = 0;
+----+--------------------+------------------+------------+-------+------------------------------------------------------------------+------------------------------------------------------------------+---------+-----------------------------------+------+----------+-------------------------------------------+
| id | select_type        | table            | partitions | type  | possible_keys                                                    | key                                                              | key_len | ref                               | rows | filtered | Extra                                     |
+----+--------------------+------------------+------------+-------+------------------------------------------------------------------+------------------------------------------------------------------+---------+-----------------------------------+------+----------+-------------------------------------------+
|  1 | PRIMARY            | d                | NULL       | index | PRIMARY,idx_gift_start_time_gift_end_time_del_status             | idx_gift_start_time_gift_end_time_del_status                     | 14      | NULL                              |   13 |     7.69 | Using where; Using index; Using temporary |
|  1 | PRIMARY            | c                | NULL       | ref   | idx_sku_gift_rule_id,idx_gift_rule_id_sku                        | idx_gift_rule_id_sku                                             | 8       | mgb_treasure_system.d.id          |    1 |   100.00 | Using index                               |
|  1 | PRIMARY            | b                | NULL       | ref   | sku_spu_k3_code_bar_code_model                                   | sku_spu_k3_code_bar_code_model                                   | 302     | mgb_treasure_system.c.sku         |    1 |   100.00 | Using index                               |
|  1 | PRIMARY            | a                | NULL       | ref   | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index                               |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO                                                     | INDEX_CAT_NO                                                     | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | Using index                               |
|  3 | UNION              | a                | NULL       | index | idx_platform_code_del_status_sku_spu_k3_code_customer_goods_name | idx_platform_code_del_status_sku_spu_k3_code_customer_goods_name | 1512    | NULL                              |   35 |     2.86 | Using where; Using index; Using temporary |
|  3 | UNION              | b                | NULL       | ref   | sku_spu_k3_code_bar_code_model                                   | sku_spu_k3_code_bar_code_model                                   | 302     | mgb_treasure_system.a.sku         |    1 |   100.00 | Using index                               |
|  3 | UNION              | c                | NULL       | ref   | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index                               |
|  4 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO                                                     | INDEX_CAT_NO                                                     | 303     | mgb_treasure_system.c.cat_root_no |    1 |   100.00 | Using index                               |
+----+--------------------+------------------+------------+-------+------------------------------------------------------------------+------------------------------------------------------------------+---------+-----------------------------------+------+----------+-------------------------------------------+
9 rows in set (0.10 sec)

~~~

 ON a.sku = b.sku JOIN stock_product c
 WHERE a.platform_code = 'P20220107035520001' AND a.del_status = 0;

舍弃sku，因为现在这个表是外表反正join肯定用不到索引。不如把位置让给where使用：
将结构 `idx_sku_spu_k3_code_platform_code_customer_goods_name_del_status`(`sku`, `spu`, `k3_code`, `platform_code`, `customer_goods_name`, `del_status`) 

改为：
`platform_code`, `del_status`, `sku`, `spu`, `k3_code`, `customer_goods_name`

看下id=3的a查询。此时 type=ref。ref = const,const ，Using where 消失了 。说明
**WHERE a.platform_code = 'P20220107035520001' AND a.del_status = 0;** 用到了索引
~~~
mysql>  EXPLAIN SELECT DISTINCT a.spu, '' customer_goods_name, a.product_name, b.sku, b.k3_code, b.bar_code, b.model, (
 SELECT cat_name
 FROM `product_category`
 WHERE cat_no = a.cat_root_no
 LIMIT 1 ) cat_name
 FROM stock_product a JOIN stock_product_detail b
 ON a.spu = b.spu JOIN jg_gift_rel_product c
 ON c.sku = b.sku JOIN jg_gift_rule d
 ON d.id = c.gift_rule_id AND d.del_status = 0 AND now( ) BETWEEN d.gift_start_time AND d.gift_end_time
 UNION ALL
 SELECT DISTINCT a.spu, a.customer_goods_name, c.product_name, a.sku, a.k3_code, b.bar_code, b.model, (
 SELECT cat_name
 FROM `product_category`
 WHERE cat_no = c.cat_root_no
 LIMIT 1 ) cat_name
 FROM jg_customer_goods_relationship a JOIN stock_product_detail b
 ON a.sku = b.sku JOIN stock_product c
 ON c.spu = b.spu
 WHERE a.platform_code = 'P20220107035520001' AND a.del_status = 0;
+----+--------------------+------------------+------------+-------+------------------------------------------------------------------+------------------------------------------------------------------+---------+-----------------------------------+------+----------+-------------------------------------------+
| id | select_type        | table            | partitions | type  | possible_keys                                                    | key                                                              | key_len | ref                               | rows | filtered | Extra                                     |
+----+--------------------+------------------+------------+-------+------------------------------------------------------------------+------------------------------------------------------------------+---------+-----------------------------------+------+----------+-------------------------------------------+
|  1 | PRIMARY            | d                | NULL       | index | PRIMARY,idx_gift_start_time_gift_end_time_del_status             | idx_gift_start_time_gift_end_time_del_status                     | 14      | NULL                              |   13 |     7.69 | Using where; Using index; Using temporary |
|  1 | PRIMARY            | c                | NULL       | ref   | idx_sku_gift_rule_id,idx_gift_rule_id_sku                        | idx_gift_rule_id_sku                                             | 8       | mgb_treasure_system.d.id          |    1 |   100.00 | Using index                               |
|  1 | PRIMARY            | b                | NULL       | ref   | sku_spu_k3_code_bar_code_model                                   | sku_spu_k3_code_bar_code_model                                   | 302     | mgb_treasure_system.c.sku         |    1 |   100.00 | Using index                               |
|  1 | PRIMARY            | a                | NULL       | ref   | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index                               |
|  2 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO                                                     | INDEX_CAT_NO                                                     | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | Using index                               |
|  3 | UNION              | a                | NULL       | ref   | idx_platform_code_del_status_sku_spu_k3_code_customer_goods_name | idx_platform_code_del_status_sku_spu_k3_code_customer_goods_name | 304     | const,const                       |   18 |   100.00 | Using index; Using temporary              |
|  3 | UNION              | b                | NULL       | ref   | sku_spu_k3_code_bar_code_model                                   | sku_spu_k3_code_bar_code_model                                   | 302     | mgb_treasure_system.a.sku         |    1 |   100.00 | Using index                               |
|  3 | UNION              | c                | NULL       | ref   | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | idx_spu_cat_root_no_supplier_no_product_name_is_combina          | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index                               |
|  4 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO                                                     | INDEX_CAT_NO                                                     | 303     | mgb_treasure_system.c.cat_root_no |    1 |   100.00 | Using index                               |
+----+--------------------+------------------+------------+-------+------------------------------------------------------------------+------------------------------------------------------------------+---------+-----------------------------------+------+----------+-------------------------------------------+
9 rows in set (0.06 sec)
~~~


###Order by

order by 可以接着 join/where的后面。也可以自己重新从当前索引开头开始走


