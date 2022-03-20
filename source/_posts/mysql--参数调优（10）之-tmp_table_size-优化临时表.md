---
title: mysql--参数调优（10）之-tmp_table_size-优化临时表.md
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
title: mysql--参数调优（10）之-tmp_table_size-优化临时表.md
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
https://dev.mysql.com/doc/refman/8.0/en/internal-temporary-tables.html



###实践
tmp_table_size默认16M。tmp_table_size如果过小，存不下了就会存到磁盘上。对于group by会有性能影响。

下面的sql EXPLAIN 如下，出现了Using temporary。表示查询会利用临时表。
~~~
(root@localhost) [dbt3]>EXPLAIN select date_format(o_orderDATE,'%Y-%m'),o_clerk,count(1),sum(o_totalprice),avg(o_totalprice) from orders group by date_format(o_orderDATE,'%Y-%m'),o_clerk
k;
+----+-------------+--------+------------+------+---------------+------+---------+------+---------+----------+---------------------------------+
| id | select_type | table  | partitions | type | possible_keys | key  | key_len | ref  | rows    | filtered | Extra                           |
+----+-------------+--------+------------+------+---------------+------+---------+------+---------+----------+---------------------------------+
|  1 | SIMPLE      | orders | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 1372000 |   100.00 | Using temporary; Using filesort |
+----+-------------+--------+------------+------+---------------+------+---------+------+---------+----------+---------------------------------+
1 row in set, 1 warning (0.00 sec)

~~~


在默认tmp_table_size大小16M下执行：
~~~

SELECT
	date_format( o_orderDATE, '%Y-%m' ),
	o_clerk,
	count( 1 ),
	sum( o_totalprice ),
	avg( o_totalprice ) 
FROM
	orders 
GROUP BY
	date_format( o_orderDATE, '%Y-%m' ),
	o_clerk;
79710 rows in set (7.34 sec)
~~~

查看临时表统计信息，Created_tmp_disk_tables 为0，Created_tmp_tables 为1表示上诉sql执行后生产了一张内存里的临时表。
~~~

(root@localhost) [dbt3]>show status like '%tmp%';
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| Created_tmp_disk_tables | 0     |
| Created_tmp_files       | 0     |
| Created_tmp_tables      | 1     |
+-------------------------+-------+
~~~
 
>Created_tmp_disk_tables 产生基于磁盘临时表数量
Created_tmp_tables   产生临时表数量



将tmp_table_size 调从16M调整为16K
~~~
set tmp_table_size = 16*1024
~~~



再次执行,查询时间从4变成了18秒
~~~
SELECT
	date_format( o_orderDATE, '%Y-%m' ),
	o_clerk,
	count( 1 ),
	sum( o_totalprice ),
	avg( o_totalprice ) 
FROM
	orders 
GROUP BY
	date_format( o_orderDATE, '%Y-%m' ),
	o_clerk;
79710 rows in set (18.58 sec)
~~~

重新统计
~~~
flush status;
~~~


再次查看status，这次有在磁盘上创建1个临时表。
~~~
(root@localhost) [dbt3]>show status like '%tmp%';
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| Created_tmp_disk_tables | 1     |
| Created_tmp_files       | 3     |
| Created_tmp_tables      | 1     |
+-------------------------+-------+
3 rows in set (0.00 sec)
~~~


###查看全局
~~~
(root@localhost) [dbt3]>show global status like '%tmp%';
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| Created_tmp_disk_tables | 75    |
| Created_tmp_files       | 3     |
| Created_tmp_tables      | 2840  |
+-------------------------+-------+
~~~

###对配置的建议
An internal temporary table can be held in memory and processed by the MEMORY storage engine, or stored on disk by the InnoDB or MyISAM storage engine.

**If an internal temporary table is created as an in-memory table but becomes too large, MySQL automatically converts it to an on-disk table. The maximum size for in-memory temporary tables is defined by the tmp_table_size or max_heap_table_size value, whichever is smaller.** This differs from MEMORY tables explicitly created with CREATE TABLE. For such tables, only the max_heap_table_size variable determines how large a table can grow, and there is no conversion to on-disk format. The internal_tmp_disk_storage_engine variable defines the storage engine the server uses to manage on-disk internal temporary tables. Permitted values are INNODB (the default) and MYISAM.

Note
When using internal_tmp_disk_storage_engine=INNODB, queries that generate on-disk internal temporary tables that exceed InnoDB row or column limits return Row size too large or Too many columns errors. The workaround is to set internal_tmp_disk_storage_engine to MYISAM.

**When an internal temporary table is created in memory or on disk, the server increments the Created_tmp_tables value. When an internal temporary table is created on disk, the server increments the Created_tmp_disk_tables value.**

**If too many internal temporary tables are created on disk, consider increasing the tmp_table_size and max_heap_table_size settings.**


-  内部临时表保存在内存中的存储引擎是 MEMORY ；磁盘上的话就是InnoDB or MyISAM
-  内部临时表在内存中的占用空间限制以 tmp_table_size 、max_heap_table_size 二者中较小值为准
-  看看Created_tmp_disk_tables多不多，多的话就加大，不多的话就维持

建议配置默认值为32M
~~~
[mysqld]
tmp_table_size=32M
Created_tmp_disk_tables=32M
~~~




###其他的
**Percona Server中的临时表信息会记录到慢查询日志**
由于MySQL慢查询日志里没有使用临时表的信息，这就给我们诊断性能问题带来了一些不便，第三方的版本如Percona Server，在慢查询里可以有更详细的信息，将会记录临时表使用的情况，从而有助于我们诊断和调优。 

**mysql8中对临时表有较大的优化**
临时表引擎使用innodb（default 磁盘）和temptable(default 内存) 

