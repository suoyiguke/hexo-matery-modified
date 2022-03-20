---
title: 获取最大id对应记录写法.md
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
title: 获取最大id对应记录写法.md
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
ORDER BY方式
~~~
EXPLAIN
SELECT
	* 
FROM
	`test1` 
ORDER BY
	id DESC 
	LIMIT 1
~~~

max join方式
~~~
EXPLAIN
SELECT * from test1 a join (
SELECT
	max(id) id
FROM
	`test1` 
	)  b using(id)
~~~
