---
title: mysql-中求行号.md
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
title: mysql-中求行号.md
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

方法1：使用自定义变量
SELECT @a:=@a+1 as rownum,a.* from employees a,(SELECT @a:=0) b limit 10000

方法2：相关子查询
~~~

SELECT
	emp_no,
	( SELECT count( 1 ) FROM employees t2 WHERE t2.emp_no <= t1.emp_no ) AS row_num 
FROM
	employees t1 
ORDER BY
	emp_no 
	LIMIT 10;
~~~
