---
title: sys库之statement_analysis查看索引的使用情况.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: sys库之statement_analysis查看索引的使用情况.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
介绍的是实例下所有库里的索引的信息

SELECT
	* 
FROM
	sys.schema_index_statistics 
WHERE
	table_schema = 'mgb_treasure_system' 
ORDER BY
	rows_selected DESC



table_schema: 库名

table_name: 表名

index_name: 索引名称

rows_selected: 使用索引读取的总行数

select_latency: 读取索引总等待时间

rows_inserted: 插入行总索引数

insert_latency: 插入索引总等待时间

rows_updated: 更新索引总行数

update_latency: 更新索引总等待时间

 rows_deleted: 从索引删除总行数

delete_latency: 删除索引总等待时间

 
~~~
mysql> select * from schema_index_statisticswhere table_schema='test' and table_name='test2' \G;

*************************** 1. row***************************

 table_schema: test

   table_name: test2

   index_name: test2_id

 rows_selected: 0

select_latency: 0 ps

 rows_inserted: 0

insert_latency: 0 ps

 rows_updated: 0

update_latency: 0 ps

 rows_deleted: 0

delete_latency: 0 ps

1 row in set (0.00 sec)

~~~
