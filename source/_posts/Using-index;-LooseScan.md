---
title: Using-index;-LooseScan.md
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
title: Using-index;-LooseScan.md
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
~~~
mysql>  EXPLAIN SELECT a.id, a.gift_rule_id giftRuleId, a.sku
 FROM jg_gift_rel_product a
 WHERE a.gift_rule_id in (
 SELECT b.gift_rule_id
 FROM jg_gift_rel_product b
 LEFT JOIN jg_gift_rule a
 ON a.id = b.gift_rule_id
 WHERE DATE_FORMAT( a.gift_end_time, '%Y-%m-%d %h:%i:%s' )>= DATE_FORMAT( NOW(), '%Y-%m-%d %h:%i:%s' ) AND DATE_FORMAT( NOW(), '%Y-%m-%d %h:%i:%s' )>= DATE_FORMAT( a.gift_start_time, '%Y-%m-%d %h:%i:%s' ) AND b.sku = 'K.33.11491.202201140027' );
+----+-------------+-------+------------+-------+----------------------+----------------------------------------------+---------+--------------------------------+------+----------+--------------------------+
| id | select_type | table | partitions | type  | possible_keys        | key                                          | key_len | ref                            | rows | filtered | Extra                    |
+----+-------------+-------+------------+-------+----------------------+----------------------------------------------+---------+--------------------------------+------+----------+--------------------------+
|  1 | SIMPLE      | a     | NULL       | index | PRIMARY              | idx_del_status_gift_start_time_gift_end_time | 14      | NULL                           |    2 |   100.00 | Using where; Using index |
|  1 | SIMPLE      | b     | NULL       | ref   | idx_gift_rule_id_sku | idx_gift_rule_id_sku                         | 310     | mgb_treasure_system.a.id,const |    1 |   100.00 | Using index; LooseScan   |
|  1 | SIMPLE      | a     | NULL       | ref   | idx_gift_rule_id_sku | idx_gift_rule_id_sku                         | 8       | mgb_treasure_system.a.id       |    7 |   100.00 | Using index              |
+----+-------------+-------+------------+-------+----------------------+----------------------------------------------+---------+--------------------------------+------+----------+--------------------------+
3 rows in set (0.03 sec)

mysql> 
~~~
