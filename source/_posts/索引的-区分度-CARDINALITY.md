---
title: 索引的-区分度-CARDINALITY.md
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
title: 索引的-区分度-CARDINALITY.md
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
SELECT
	CARDINALITY,
	INDEX_NAME,
	TABLE_NAME 
FROM
	information_schema.STATISTICS 
WHERE
	TABLE_SCHEMA = 'dbt3' 
	AND TABLE_NAME = 'customer'
~~~
	
~~~
	SELECT
	TABLE_ROWS
	
FROM
	information_schema.TABLES 
WHERE
	TABLE_SCHEMA = 'dbt3' 
	AND TABLE_NAME = 'customer'

~~~


主键 的CARDINALITY  = 表记录行数


###找出 区分度 CARDINALITY 比较低的索引

~~~
SELECT
	p.table_schema,
	p.table_name,
	c.index_name,
	c.car,
	p.car total,
  c.car / p.car '%'	
FROM
	(
	SELECT
		table_schema,
		table_name,
		index_name,
		max( cardinality ) car 
	FROM
		INFORMATION_SCHEMA.STATISTICS 
	WHERE
		index_name != 'PRIMARY' 
	GROUP BY
		table_schema,
		table_name,
		index_name 
	) c,
	(
	SELECT
		table_schema,
		table_name,
		TABLE_ROWS car 
	FROM
		information_schema.TABLES 
	WHERE
		 table_schema != 'mysql' 
	) p 
WHERE
	c.table_name = p.table_name 
	AND c.table_schema = p.table_schema 
	AND p.car > 0 
	AND c.car / p.car < 0.1;
	
	
	SHOW  INDEX from employees.dept_emp
~~~


###像这样典型的sql
select * from t where a=,b= order by c
select * from t where b=,a= order by c

####这个时候a和b谁在前面？
尽可能把区分度CARDINALITY高的列放到前面

####具体怎么量化？
- 直接distinct计算
- 

