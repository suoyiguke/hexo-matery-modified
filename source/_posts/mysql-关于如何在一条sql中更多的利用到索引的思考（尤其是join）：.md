---
title: mysql-关于如何在一条sql中更多的利用到索引的思考（尤其是join）：.md
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
title: mysql-关于如何在一条sql中更多的利用到索引的思考（尤其是join）：.md
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
把索引利用看成下楼梯,where条件可以让联合索引一直往下走







###order by 可以作用在当前楼和所有上层楼就是不能作用在下一楼
例子1、索引结构 identity_number,updated_at

>EXPLAIN SELECT
	* 
FROM
	biz_cloudsign_sign 
WHERE
	identity_number = '' 
	AND updated_at BETWEEN '2010-12-25 16:03:11' 
	AND '2020-12-25 16:03:11' 
ORDER BY
	`identity_number `DESC


或者



>EXPLAIN SELECT
	* 
FROM
	biz_cloudsign_sign 
WHERE
	identity_number = '' 
	AND updated_at BETWEEN '2010-12-25 16:03:11' 
	AND '2020-12-25 16:03:11' 
ORDER BY
	`updated_at` DESC


这两个sql分别以identity_number和updated_at作为排序条件，执行计划均没有出现Using filesort




例子2、索引结构 updated_at,identity_number,employee_num

>EXPLAIN SELECT
	* 
FROM
	biz_cloudsign_sign 
WHERE
	identity_number = '' 
	AND updated_at BETWEEN '2010-12-25 16:03:11' 
	AND '2020-12-25 16:03:11' 
ORDER BY
	`employee_num` DESC

以employee_num作为排序条件，出现 Using filesort


那么在上面sql的基础上添加一个employee_num的where条件：
>EXPLAIN SELECT
	* 
FROM
	biz_cloudsign_sign 
WHERE
	identity_number = '' 
	AND updated_at BETWEEN '2010-12-25 16:03:11' 
	AND '2020-12-25 16:03:11' 
	AND employee_num = '' 
ORDER BY
	`employee_num` DESC

这样Using filesort就消失了！看来是where条件将索引下到了employee_num处。

那么再来试下order by作用在updated_at 之上会是什么情况。

>EXPLAIN SELECT *
FROM
biz_cloudsign_sign
WHERE
identity_number = ''
AND updated_at BETWEEN '2010-12-25 16:03:11'
AND '2020-12-25 16:03:11' AND employee_num = ''
ORDER BY
`updated_at` DESC

没有出现 Using filesort


>得出结论：只要联合索引 (a,b,c) 下到了 c 时，那么order by a、order by b、order by c 都会使用到索引的！

order by 可以作用在当前楼和所有上层楼就是不能作用在下一楼

###思考

>EXPLAIN SELECT * from biz_cloudsign_sign WHERE updated_at BETWEEN '2010-12-25 16:03:11' and '2020-12-25 16:03:11' GROUP BY identity_number ORDER BY id desc

在这样一条sql里，同时存在了WHERE 、GROUP BY 和 ORDER BY。思考如何建立索引让它同时被这三个条件利用？
