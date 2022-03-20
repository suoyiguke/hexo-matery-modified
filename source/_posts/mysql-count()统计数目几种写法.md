---
title: mysql-count()统计数目几种写法.md
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
title: mysql-count()统计数目几种写法.md
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
>古之学者必有师



###COUNT(字段)、 COUNT(*) 、COUNT(1)之间的区别
首先我们通过一条sql来感受COUNT()函数 使用在 字段、*、1之间的区别
~~~
SELECT
	count( a ),
	count( * ),
	count( 1 ) 
FROM
	( SELECT 1 a UNION ALL SELECT 2 a UNION ALL SELECT 3 a UNION ALL SELECT NULL a ) tb
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-51704323f1825adf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 可见， count(a) 统计的是不为NULL的所有a字段记录数；count(*) 和count(1) 都是统计该表的所有行(包括NULL)

1、统计某列值的数量
  count(可能为空的字段) 只是统计统计某列值的数量（不为空部分的数量）

2、当count()函数的参数是不可能为NULL时就是统计结果集行数
 count(*)、count(id主键) 、count(常数1) 都是统计结果集行数


###性能上的区别
>count(*)=count(1)>count(primary key)>count(column)
