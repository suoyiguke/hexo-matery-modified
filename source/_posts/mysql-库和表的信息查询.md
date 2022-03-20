---
title: mysql-库和表的信息查询.md
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
title: mysql-库和表的信息查询.md
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
###查看所有数据库各容量大小
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
###查看所有数据库各表容量大小
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

###查看指定数据库容量大小
例：查看mysql库容量大小
~~~
select
table_schema as '数据库',
sum(table_rows) as '记录数',
sum(truncate(data_length/1024/1024, 2)) as '数据容量(MB)',
sum(truncate(index_length/1024/1024, 2)) as '索引容量(MB)'
from information_schema.tables
where table_schema='mysql';　
~~~
###查看指定数据库各表容量大小
例：查看mysql库各表容量大小
~~~
select
table_schema as '数据库',
table_name as '表名',
table_rows as '记录数',
truncate(data_length/1024/1024, 2) as '数据容量(MB)',
truncate(index_length/1024/1024, 2) as '索引容量(MB)'
from information_schema.tables
where table_schema='mysql'
order by data_length desc, index_length desc;
~~~

~~~
SELECT
	* 
FROM
	( SELECT count( * ) '表数量' FROM information_schema.TABLES WHERE table_schema = 'iam' ) a,
	( SELECT COUNT( column_name ) '列数量' FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'iam' ) b,
	( SELECT sum( TRUNCATE ( data_length / 1024 / 1024, 2 ) ) AS '数据容量(MB)' FROM information_schema.TABLES ) c
	
~~~
