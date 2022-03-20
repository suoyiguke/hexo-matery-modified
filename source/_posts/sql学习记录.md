---
title: sql学习记录.md
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
title: sql学习记录.md
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
SQL89




SQL92
1、出现out join

###

不去重
select * from x join y on x.id=y.id 

IN子查询会去重
select * from x where   id in (select id from y)


如何改写子查询为join？
select distinct x.* from x join y on x.id=y.id 


###在一对多的关系表中取出一对一数据
employess 与titles一对多

如：查询每个员工表的最新title

错误写法：这样求的是每个员工的每个title，这里的MAX函数不起作用
~~~
SELECT emp_no,MAX( to_date )
FROM
	titles 
GROUP BY emp_no
~~~

正确写法：使用子查询
~~~
SELECT
	emp_no,
	title 
FROM
	titles 
WHERE
	( emp_no, to_date ) IN ( SELECT emp_no, MAX( to_date ) FROM titles GROUP BY emp_no );
~~~

###默认排序不是id
mysql 不写order by 并不是按id排序！
只是mysql觉得根据哪个快就用哪个







###LEFT JOIN ON 条件和where 条件又有什么区别？

1、LEFT JOIN ON 后面只写表关联的语句，其它过滤条件请写在where条件中。
2、如果把其它条件写到LEFT JOIN ON 后并不好理解，而且在特定情景下容易出错！
3、LEFT JOIN ON 后的表关联条件请不要写到where条件中，这个的话left join就实际上执行成inner join了



###自己创建临时表和GROUPBY临时表区别
自定义临时表创建实例：
~~~
CREATE TEMPORARY TABLE a ( id INT ( 11 ) );
~~~

SHOW CREATE TABLE a
~~~
CREATE TEMPORARY TABLE `a` (
  `id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
~~~



这两种临时表是不同的概念

1、GROUP BY临时表是mysql隐式创建的，存储引擎是memory。受tmp_table_size参数影响。内存放不下就会放磁盘。


2、create tempray table 创建的临时表是用户显式创建的，存储引擎是默认引擎。
这个临时表是会话级别的。会话退出表就会被删除，不同会话之间可以创建相同名字的临时表。

ibtmp1文件是临时表空间，用于存放数据内容。数据库启动之后会自动删除ibtmp1文件。

tmpdir=/tmp 中tmp目录存放表结构.frm文件，在5.6下这个目录因为空间太小建议更改。5.6下会没有ibtmp1文件，表空间和frm都存在tmpdir目录下。所以临时表过大，建议设置到datadir下，以防临时表空间占用空间过大导致磁盘空间不足。

~~~
(root@localhost) [(none)]>show variables like '%tmpdir%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| innodb_tmpdir     |       |
| slave_load_tmpdir | /tmp  |
| tmpdir            | /tmp  |
+-------------------+-------+
~~~

~~~
[mysqld-5.6]
tmpdir=/mdata/temp
~~~



