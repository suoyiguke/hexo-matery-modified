---
title: mysql-hint优化器提示之使用force-index-强制使用索引和指定禁用索引.md
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
title: mysql-hint优化器提示之使用force-index-强制使用索引和指定禁用索引.md
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
###mysql强制使用索引
1、mysql强制使用主键索引
~~~
select * from table force index(PRI) limit 2;(强制使用主键)
~~~

2、强制指定一个特定索引
~~~
select * from table force index(idx) limit 2;(强制使用索引”idx”)
~~~

3、同时指定两个
~~~
select * from table force index(PRI,idx) limit 2;(强制使用索引”PRI和idx”)
~~~

4、在多个表join中强制使用索引
~~~

EXPLAIN
SELECT
	updated_at_date,
	count(v.updated_at_date)
FROM
	biz_cloudsign_login v  force index(index_updated_at_date)
	INNER JOIN ( SELECT MAX( id ) 'id' FROM biz_cloudsign_login force index(index_employee_num,PRI) GROUP BY employee_num,updated_at_date order by null  ) c ON v.id = c.id 
 	GROUP BY v.updated_at_date order by null 

~~~

>把force index(索引A) 语句放在存在索引A的表名之后。比如上面的sql，索引 index_updated_at_date就是属于表 biz_cloudsign_login 的
 

### mysql禁止某个索引：ignore index(索引名或者主键PRI)


select * from table ignore index(PRI) limit 2;(禁止使用主键)

select * from table ignore index(idx) limit 2;(禁止使用索引”idx”)

select * from table ignore index(PRI,idx) limit 2;(禁止使用索引”PRI,idx”)


###这种hint不建议使用在生产sql中
force index 不建议使用，如果数据量有变化，指定的索引可能不是最佳的
