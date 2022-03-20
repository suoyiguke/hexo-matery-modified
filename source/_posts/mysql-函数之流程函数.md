---
title: mysql-函数之流程函数.md
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
title: mysql-函数之流程函数.md
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
> 皇路当清夷，含和吐明庭

![image.png](https://upload-images.jianshu.io/upload_images/13965490-d8a48aeb317f6684.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###### IF() 函数
> 可使用“真”、“假” 两中情况替换第一个布尔值/表达式 参数
~~~
-- 真
SELECT IF(TRUE,'真','假')

-- 假
SELECT IF(FALSE,'真','假')

-- 假 ，若传入NULL，则视作为假
SELECT IF(NULL,'真','假')

~~~

if函数用来判断空字符串

~~~
select if((ISNULL('   ')=1) || (LENGTH(trim('   '))=0),'次字符串为空字符串','此字符串非空') 
~~~


######IFNULL()函数
>可用来替换NULL值

~~~
-- 0
SELECT IFNULL(NULL,0)
~~~

######CASE WHEN ..THEN .. ELSE .. END 语句(类似于if-else语句)
> 非此即彼
~~~
-- 我是FALG1
SELECT CASE WHEN TRUE
  THEN
		'我是FALG1'
	ELSE
		'我是默认返回'
END ;


-- 我是默认返回
SELECT CASE WHEN FALSE
  THEN
		'我是FALG1'
	ELSE
		'我是默认返回'
END ;

~~~

###### CASE .. WHEN ..THEN .. ELSE .. END 语句（类似于switch语句）

> 适用于有多种情况时
~~~

-- 我是FALG 
SELECT CASE 'FALG'
	WHEN 'FALG' THEN
		'我是FALG'
	ELSE
		'我是默认返回'
END ;

-- 我是默认返回
SELECT CASE 'FALG'
	WHEN 'FALG1' THEN
		'我是FALG'
	ELSE
		'我是默认返回'
END ;


-- FALG
SELECT CASE 'FALG'
	WHEN 'FALG1' THEN
		'我是FALG'
	WHEN 'FALG' THEN
		'FALG'
	ELSE
		'我是默认返回'
END ;

~~~
