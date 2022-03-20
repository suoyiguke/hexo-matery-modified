---
title: 例行巡检查询1---mysql基本情况.md
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
title: 例行巡检查询1---mysql基本情况.md
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
1、检查哪些表不是innodb
查看默认引擎 
~~~
SHOW VARIABLES LIKE '%storage_engine%'; 
~~~

2、查看非InnoDB引擎的业务表： 
~~~
SELECT
	`TABLE_NAME`,
	`TABLE_SCHEMA`,
	`ENGINE`,
	sys.format_bytes ( DATA_LENGTH ) AS data_size 
FROM
	information_schema.`TABLES` 
WHERE
	`ENGINE` != 'innodb' 
	AND TABLE_SCHEMA  IN ( 'mgb_treasure_system' ); 
~~~

3、检查哪些表的字符集不是utf8-mb4

~~~
SELECT
	* 
FROM
	information_schema.TABLES 
WHERE
	TABLE_COLLATION LIKE 'utf8%' 
	AND  TABLE_SCHEMA  IN ( 'mgb_treasure_system' ); 
~~~


4、查看哪些表没有设置主键
~~~
SELECT
	table_schema,
	table_name 
FROM
	information_schema.TABLES 
WHERE
	table_name NOT IN ( SELECT DISTINCT table_name FROM information_schema.COLUMNS WHERE column_key = 'PRI' ) 
	AND  TABLE_SCHEMA  IN ( 'mgb_treasure_system' ); 
~~~


5、查看没有使用到的索引
~~~
SELECT
	OBJECT_SCHEMA 'db',
	OBJECT_NAME 'table_name',
	INDEX_NAME 'index name',
	COUNT_STAR 'use count' 
FROM
	performance_schema.table_io_waits_summary_by_index_usage 
WHERE
	INDEX_NAME IS NOT NULL 
	AND COUNT_STAR = 0 
	AND OBJECT_SCHEMA IN ( 'mgb_treasure_system' ) 
	AND index_name != 'PRIMARY' 
ORDER BY
	OBJECT_SCHEMA,
	OBJECT_NAME;
~~~

6、查询各个表的当前AUTO_INCREMENT值。还有主键的数据类型

~~~
SELECT
	* 
FROM
	(
	SELECT
		ts.TABLE_SCHEMA,
		t.TABLE_NAME,
		t.CONSTRAINT_TYPE,
		c.COLUMN_NAME,
		c.ORDINAL_POSITION,
		ts.AUTO_INCREMENT,
		cs.COLUMN_TYPE,
		cs.CHARACTER_SET_NAME,
		cs.COLLATION_NAME,
		cs.COLUMN_KEY 
	FROM
		INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS t,
		INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS c,
		INFORMATION_SCHEMA.TABLES AS ts,
		information_schema.COLUMNS AS cs 
	WHERE
		t.TABLE_SCHEMA = c.TABLE_SCHEMA 
		AND t.TABLE_NAME = c.TABLE_NAME 
		AND ts.TABLE_SCHEMA = t.TABLE_SCHEMA 
		AND cs.TABLE_SCHEMA = c.TABLE_SCHEMA 
		AND cs.TABLE_NAME = c.TABLE_NAME 
		AND cs.COLUMN_NAME = c.COLUMN_NAME 
		AND ts.TABLE_SCHEMA  IN ( 'mgb_treasure_system' ) 
		AND t.CONSTRAINT_TYPE = 'PRIMARY KEY' 
	) AS a 
ORDER BY
	AUTO_INCREMENT DESC
	
	
~~~




###MySQL查看数据库表容量大小


1.查看所有数据库容量大小
~~~
select 
table_schema as '数据库',
sum(table_rows) as '记录数',
sum(truncate(data_length/1024/1024, 2)) as '数据容量(MB)',
sum(truncate(index_length/1024/1024, 2)) as '索引容量(MB)'
from information_schema.tables
group by table_schema
order by sum(data_length) desc, sum(index_length) desc;
~~~

2.查看所有数据库各表容量大小
~~~
select 
table_schema as '数据库',
table_name as '表名',
table_rows as '记录数',
truncate(data_length/1024/1024, 2) as '数据容量(MB)',
truncate(index_length/1024/1024, 2) as '索引容量(MB)'
from information_schema.tables
order by data_length desc, index_length desc;
~~~

3.查看指定数据库容量大小
例：查看mysql库容量大小
~~~
select 
table_schema as '数据库',
sum(table_rows) as '记录数',
sum(truncate(data_length/1024/1024, 2)) as '数据容量(MB)',
sum(truncate(index_length/1024/1024, 2)) as '索引容量(MB)'
from information_schema.tables
where table_schema IN ( 'mgb_treasure_system' ) 
~~~


4.查看指定数据库各表容量大小
例：查看mysql库各表容量大小
~~~
select 
table_schema as '数据库',
table_name as '表名',
table_rows as '记录数',
truncate(data_length/1024/1024, 2) as '数据容量(MB)',
truncate(index_length/1024/1024, 2) as '索引容量(MB)'
from information_schema.tables
where table_schema IN ( 'mgb_treasure_system' ) 
order by data_length desc, index_length desc;
~~~


5、查看各个表的table_row估计值
~~~
SELECT
	TABLE_SCHEMA,
	table_name,
	table_rows,
	ENGINE,
	table_type,
	Avg_row_length,
	Data_length,
	Max_data_length,
	Index_length,
	Data_free,
	Auto_increment,
	Create_time,
	Update_time,
	Check_time,
	Table_collation,
	CHECKSUM,
	Create_options,
	Table_comment 
FROM
	information_schema.TABLES 
WHERE
	TABLE_SCHEMA IN ( 'mgb_treasure_system' ) 
ORDER BY
	table_rows DESC;
~~~


