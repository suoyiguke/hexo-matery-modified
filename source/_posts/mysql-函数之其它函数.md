---
title: mysql-函数之其它函数.md
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
title: mysql-函数之其它函数.md
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
-- test
SELECT DATABASE()
-- 5.7.22-log
SELECT VERSION()
-- root@localhost
SELECT USER()
-- ip字符串转ip数值 3232235620
SELECT INET_ATON('192.168.0.100')
-- ip数值转ip字符串 192.168.0.100
SELECT INET_NTOA(3232235620)
-- 密码加密 *23AE809DDACAF96AF0FD78ED04B6A265E05AA257
SELECT PASSWORD("123")
-- md5摘要  202cb962ac59075b964b07152d234b70
SELECT md5("123")
~~~

我们知道，ip推荐使用数值的方式存储而不是字符串，这样会获得更好的性能。所以就需要使用INET_ATON()函数将ip字符串转为数值然后存储；我们甚至可以使用这个函数来得到两个ip之间范围内的所有ip 


# IF 函数

判断空字符串
~~~
select if((ISNULL('string')=1) || (LENGTH(trim('string'))=0),'1','2') 
~~~
