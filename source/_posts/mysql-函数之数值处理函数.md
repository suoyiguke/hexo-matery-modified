---
title: mysql-函数之数值处理函数.md
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
title: mysql-函数之数值处理函数.md
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
> 在齐太史简，在晋董狐笔
###最值
######行最值
~~~
SELECT GREATEST(3, 12, 34, 8, 25); 
SELECT LEAST(3, 12, 34, 8, 25); 
~~~
######列最值
~~~
SELECT MAX(a) FROM (SELECT 1 a UNION ALL SELECT 2 a UNION ALL SELECT 3 a UNION ALL SELECT 4 a UNION ALL SELECT 5 a ) tb;

SELECT MIN(a) FROM (SELECT 1 a UNION ALL SELECT 2 a UNION ALL SELECT 3 a UNION ALL SELECT 4 a UNION ALL SELECT 5 a ) tb;
~~~~
###整数处理
######整数随机值
500-1000之间的整数，包含500，不包含1000（这个我用存储过程验证过）
~~~
SELECT FLOOR( 500 + RAND() * (1000 - 500))
~~~
######绝对值
~~~
-- 1
SELECT ABS(-1)
-- 1
SELECT ABS(1)
~~~

######大于x的最小整数值和小于x的最大整数值
~~~
-- 2 返回大于x的最小整数值
SELECT CEIL(1.22)

-- 1 返回小于x的最大整数值
SELECT FLOOR(1.22)
~~~

######取模/取余运算
`mysql中的MOD()函数其实是取余数，而不是取模`

1、取余运算
> 可以使用MOD() 函数 或 %计算
~~~
SELECT MOD(5,3),5%3,MOD(5,-3),5%-3
~~~

2、取模运算
> 使用 div 运算
~~~
-- 输出 -1
SELECT 5 div -3
~~~

###浮点近似值

######四舍五入 
~~~
-- 输出 1.235
SELECT ROUND(1.23496,3) 
~~~

###### 直接截取
~~~
-- 输出 1.234
SELECT TRUNCATE(1.23496,3) 
~~~
######随机浮点数 
1、在0-1之前
~~~
SELECT RAND()
~~~

2、产生0到10000间的随机浮点数
~~~
SELECT RAND() * 10000
~~~


###聚合函数

>1、运行在行组上，计算和返回单个值的函数。
>2、聚合函数忽略列值为NULL的行。
>3、聚合函数可以和`DISTINCT`配合使用；如果指定列名，则DISTINCT只能用于COUNT()。DISTINCT不能用于COUNT(*)，因此不允许使用COUNT（ DISTINCT），否则会产生错误。类似地， DISTINCT必须使用列名，不能用于计算或表达式。
>4、聚集函数用来汇总数据。 MySQL支持一系列聚集函数，可以用多种方法使用它们以返回所需的结果。`这些函数是高效设计的，它们返回结果一般比你在自己的客户机应用程序中计算要快得多。` 所以请优先使用聚合函数，而不是在程序中实现！！

######聚合函数会忽略NULL值
我们以COUNT()函数为例子
~~~
SELECT
    COUNT( a ) 
FROM
    ( SELECT 1 a UNION ALL SELECT NULL a UNION ALL SELECT 3 a UNION ALL SELECT 4 a UNION ALL SELECT 5 a ) tb;
~~~
> 可见5行a字段，其中有一个为NULL，它输出4。NULL值没有参与统计

######聚合函数中使用DISTINCT
同样使用COUNT()函数举例如下： 
~~~
SELECT
    COUNT( DISTINCT a ) 
FROM
    ( SELECT 1 a UNION ALL SELECT 1 a UNION ALL SELECT 3 a UNION ALL SELECT 4 a UNION ALL SELECT 5 a ) tb;
~~~
> 可见a字段有两个为1，则同出来的数量是4而不是5

如果使用  count( DISTINCT * ) 会怎么样？
~~~
SELECT
    count( DISTINCT * ) 
FROM
    ( SELECT 1 a UNION ALL SELECT 1 a UNION ALL SELECT 3 a UNION ALL SELECT 4 a UNION ALL SELECT 5 a ) tb;
~~~
直接报错，这个sql无法正常执行！！

######列求和
~~~
SELECT
	SUM( a ) 
FROM
	( SELECT 1 a UNION ALL SELECT 2 a UNION ALL SELECT 3 a UNION ALL SELECT 4 a UNION ALL SELECT 5 a ) tb;
~~~

######平均
~~~
SELECT
	AVG( a ) 
FROM
	( SELECT 0 a UNION ALL SELECT 0 a UNION ALL SELECT 2 a UNION ALL SELECT 1 a ) tb;
~~~
######统计行数
~~~
SELECT
	count( a ) 
FROM
	( SELECT 0 a UNION ALL SELECT 0 a UNION ALL SELECT 2 a UNION ALL SELECT 1 a ) tb;
~~~
######列最值
1、max() 最大值
~~~
SELECT
	max( a ) 
FROM
	( SELECT 0 a UNION ALL SELECT 0 a UNION ALL SELECT 2 a UNION ALL SELECT 1 a ) tb;
~~~

2、min()最小值
~~~
SELECT
	min( a ) 
FROM
	( SELECT 0 a UNION ALL SELECT 0 a UNION ALL SELECT 2 a UNION ALL SELECT 1 a ) tb;
~~~
