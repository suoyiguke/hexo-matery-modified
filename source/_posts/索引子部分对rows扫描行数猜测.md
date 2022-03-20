---
title: 索引子部分对rows扫描行数猜测.md
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
title: 索引子部分对rows扫描行数猜测.md
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
索引子部分设置对rows列有影响。需要设置一个合理的值
- 索引子部分设置太小，rows变多。需要扫描更多行才能找到数据，减低查找效率。
- 索引子部分设置太大又浪费索引空间！

a表的spu字段索引全部建立，扫描1行
~~~
mysql> EXPLAIN SELECT
	a.spu,
	a.is_combination,
	a.supplier_no,
	a.product_name,
	( SELECT supplier_name FROM supplier WHERE supplier_no = a.supplier_no LIMIT 1 ) supplier_name,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) cat_name,
	b.id,
	b.sku,
	b.k3_code,
	-- b.spec_data,
	b.bar_code,
	b.model 
FROM
	stock_product a FORCE INDEX ( `index` )
	JOIN stock_product_detail b USING ( spu ) 
WHERE
	b.sku IN ( 'K.33.11491.202201140029', 'K.33.10704.202201240002', 'K.33.10704.202201120088', 'K.33.11491.202201140027', 'K.33.10767.202201140020', 'K.33.11491.202201140025', 'K.33.11231.202201200002', 'K.33.10704.202201120086' );;
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
| id | select_type        | table            | partitions | type  | possible_keys   | key             | key_len | ref                               | rows | filtered | Extra                    |
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | b                | NULL       | range | index           | index           | 302     | NULL                              |    8 |   100.00 | Using where; Using index |
|  1 | PRIMARY            | a                | NULL       | ref   | index           | index           | 302     | mgb_treasure_system.b.spu         |    1 |   100.00 | Using index              |
|  3 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO    | INDEX_CAT_NO    | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | Using index              |
|  2 | DEPENDENT SUBQUERY | supplier         | NULL       | ref   | idx_supplier_no | idx_supplier_no | 152     | mgb_treasure_system.a.supplier_no |    1 |   100.00 | Using where; Using index |
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
4 rows in set (0.04 sec)

mysql> 
~~~

spu字段索引建立前2个字符，rows扫描1126行
~~~
mysql> EXPLAIN SELECT
	a.spu,
	a.is_combination,
	a.supplier_no,
	a.product_name,
	( SELECT supplier_name FROM supplier WHERE supplier_no = a.supplier_no LIMIT 1 ) supplier_name,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) cat_name,
	b.id,
	b.sku,
	b.k3_code,
	-- b.spec_data,
	b.bar_code,
	b.model 
FROM
	stock_product a FORCE INDEX ( `index` )
	JOIN stock_product_detail b USING ( spu ) 
WHERE
	b.sku IN ( 'K.33.11491.202201140029', 'K.33.10704.202201240002', 'K.33.10704.202201120088', 'K.33.11491.202201140027', 'K.33.10767.202201140020', 'K.33.11491.202201140025', 'K.33.11231.202201200002', 'K.33.10704.202201120086' );;
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
| id | select_type        | table            | partitions | type  | possible_keys   | key             | key_len | ref                               | rows | filtered | Extra                    |
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | b                | NULL       | range | index           | index           | 302     | NULL                              |    8 |   100.00 | Using where; Using index |
|  1 | PRIMARY            | a                | NULL       | ref   | index           | index           | 8       | mgb_treasure_system.b.spu         | 1126 |   100.00 | Using where              |
|  3 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO    | INDEX_CAT_NO    | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | Using index              |
|  2 | DEPENDENT SUBQUERY | supplier         | NULL       | ref   | idx_supplier_no | idx_supplier_no | 152     | mgb_treasure_system.a.supplier_no |    1 |   100.00 | Using where; Using index |
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
4 rows in set (0.06 sec)

mysql> 
~~~


如果为了节省索引空间和让索引效率更高，我们可以使用公式来取最优值：

经过反复测试，设置spu索引前缀24位是最优的！
~~~
mysql> select count(distinct left(spu,50))/count(*) FROM stock_product;
+---------------------------------------+
| count(distinct left(spu,50))/count(*) |
+---------------------------------------+
| 0.9993                                |
+---------------------------------------+
1 row in set (0.05 sec)

mysql> select count(distinct left(spu,25))/count(*) FROM stock_product;
+---------------------------------------+
| count(distinct left(spu,25))/count(*) |
+---------------------------------------+
| 0.9993                                |
+---------------------------------------+
1 row in set (0.05 sec)

mysql> select count(distinct left(spu,24))/count(*) FROM stock_product;
+---------------------------------------+
| count(distinct left(spu,24))/count(*) |
+---------------------------------------+
| 0.9993                                |
+---------------------------------------+
1 row in set (0.05 sec)

mysql> select count(distinct left(spu,23))/count(*) FROM stock_product;
+---------------------------------------+
| count(distinct left(spu,23))/count(*) |
+---------------------------------------+
| 0.8530                                |
+---------------------------------------+
1 row in set (0.05 sec)

mysql> select count(distinct left(spu,24))/count(*) FROM stock_product;
+---------------------------------------+
| count(distinct left(spu,24))/count(*) |
+---------------------------------------+
| 0.9993                                |
+---------------------------------------+
1 row in set (0.05 sec)
~~~

测试下，也只扫1条就行了
~~~
mysql> EXPLAIN SELECT
	a.spu,
	a.is_combination,
	a.supplier_no,
	a.product_name,
	( SELECT supplier_name FROM supplier WHERE supplier_no = a.supplier_no LIMIT 1 ) supplier_name,
	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) cat_name,
	b.id,
	b.sku,
	b.k3_code,
	-- b.spec_data,
	b.bar_code,
	b.model 
FROM
	stock_product a FORCE INDEX ( `index` )
	JOIN stock_product_detail b USING ( spu ) 
WHERE
	b.sku IN ( 'K.33.11491.202201140029', 'K.33.10704.202201240002', 'K.33.10704.202201120088', 'K.33.11491.202201140027', 'K.33.10767.202201140020', 'K.33.11491.202201140025', 'K.33.11231.202201200002', 'K.33.10704.202201120086' );;
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
| id | select_type        | table            | partitions | type  | possible_keys   | key             | key_len | ref                               | rows | filtered | Extra                    |
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
|  1 | PRIMARY            | b                | NULL       | range | index           | index           | 302     | NULL                              |    8 |   100.00 | Using where; Using index |
|  1 | PRIMARY            | a                | NULL       | ref   | index           | index           | 74      | mgb_treasure_system.b.spu         |    1 |   100.00 | Using where              |
|  3 | DEPENDENT SUBQUERY | product_category | NULL       | ref   | INDEX_CAT_NO    | INDEX_CAT_NO    | 303     | mgb_treasure_system.a.cat_root_no |    1 |   100.00 | Using index              |
|  2 | DEPENDENT SUBQUERY | supplier         | NULL       | ref   | idx_supplier_no | idx_supplier_no | 152     | mgb_treasure_system.a.supplier_no |    1 |   100.00 | Using where; Using index |
+----+--------------------+------------------+------------+-------+-----------------+-----------------+---------+-----------------------------------+------+----------+--------------------------+
4 rows in set (0.08 sec)
~~~
