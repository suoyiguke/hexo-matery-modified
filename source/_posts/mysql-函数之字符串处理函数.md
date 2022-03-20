---
title: mysql-函数之字符串处理函数.md
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
title: mysql-函数之字符串处理函数.md
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
> 时穷节乃现，一一垂丹青
######字符串长度
~~~
SELECT Length('yinkai')   
~~~
输出 6


######字符串截取
1、left
~~~
SELECT  Left('yinkai',3)  
~~~
输出 yin，返回'yinkai'最左3个字符

2、right
~~~
SELECT  RIGHT('yinkai',3)  
~~~
输出 kai，返回'yinkai'最右3个字符

3、SubString
~~~
--  输出 kai
SELECT SUBSTRING('yinkai',4)
--  输出 kai
SELECT SUBSTRING('yinkai',4,3) 
~~~
将'yinkai'第4个字符（包含）之后长度为3的字符截取返回


4、
~~~
 select substring_index('2565545878812-1','-',1)
~~~


######字符串替换
~~~
SELECT INSERT('yinkai',2,2,'aa')
~~~
输出 yaakai ，将字符串'yinkai' 从2开始，2个长度的子串替换为字符串'aa'

######字符串拼接（select a,b,c 其中a,b,c 列之间）
~~~
--  输出 SQL Runoob Gooogle Facebook
SELECT CONCAT("SQL ", "Runoob ", "Gooogle ", "Facebook")
--  输出SQL-Tutorial-is-fun!
SELECT CONCAT_WS("-", "SQL", "Tutorial", "is", "fun!")
~~~

使用举例：
可用于拼接各个select的列，如下：
~~~
SELECT CONCAT_WS('-',a,b,c) FROM (SELECT 1 a , 2 b, 3 c) tb
~~~

其中 `SELECT 1 a , 2 b, 3 c` 中构建了一个有a，b，c三列的表如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6272d57095f2dd10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######字符串拼接（select a 行之间）
~~~
SELECT GROUP_CONCAT(a SEPARATOR '-') FROM (SELECT 1 a UNION ALL SELECT 2 a  UNION ALL SELECT 3 a) tb
~~~
> GROUP_CONCAT(expr) 函数若只传列名，则默认按逗号分隔所有的行；当然可以使用 GROUP_CONCAT(a SEPARATOR '-') 指定所需要的分隔符，这里是`-`

其中 `SELECT 1 a UNION ALL SELECT 2 a  UNION ALL SELECT 3 a` 构建了一个只有a列的表如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3b9c0879706802fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######字符串填充
1、LPAD
~~~
SELECT LPAD('yinkai',LENGTH('yinkai')+2+2,'aa')
~~~
输出aaaayinkai，用字符串'aa'去对'yinkai'的最左边进行填充，直到最终长度为 LENGTH('yinkai')+2+2 = 10

2、RPAD
~~~
SELECT RPAD('yinkai',LENGTH('yinkai')+2+2,'aa')
~~~
输出yinkaiaaaa，用字符串'aa'去对'yinkai'的最右边进行填充，直到最终长度为 LENGTH('yinkai')+2+2 = 10



######判断是否包含子串

1、Locate   返回索引数值；返回字符串'yinkai'中第一个出现子字符串的 'kai'位置，从位置4开始
~~~
-- 输出4
SELECT LOCATE('kai','yinkai') 
-- 输出4
SELECT LOCATE('kai','yinkai',4) 
~~~ 

> 只需判断返回值是否等于0即可判断是否包含指定子串

2、FIELD、FIND_IN_SET  返回索引数值

~~~
-- 输出3
SELECT FIELD("c", "a", "b", "c", "d", "e"); 
--  输出3
SELECT FIND_IN_SET("c", "a,b,c,d,e");
~~~
> FIELD和FIND_IN_SET未找到均返回0

使用举例：
我们可以使用FIND_IN_SET()函数来实现一种 `IN` 的功能如下：
> 然而这和IN又有区别：它的值是在一个字符串中使用逗号分隔开的，而in的值是在多个字符串中
~~~
SELECT
	* 
FROM
	( SELECT '1249602002032267265' id UNION ALL SELECT '1249627442268606466' id UNION ALL SELECT '1249601566097281025' id ) tb 
WHERE
	FIND_IN_SET( id, '1249602002032267265,1249627442268606466,1249601566097281025' )
~~~ 


 ######大小写转换
~~~
--  输出nba
SELECT LOWER('NBA')
--  输出 NBA
SELECT Upper('nba')
~~~


######去除空格
~~~
SELECT RTrim(a),a FROM  (SELECT  'yinkai ' a )tb
~~~

>Trim函数 MySQL除了支持RTrim()（正如刚才所见，它去掉串右边的空格），还支持LTrim()（去掉串左边的空格）以及Trim()


######随机字符串
~~~
CREATE DEFINER=`root`@`localhost` FUNCTION `rand_string`(n int) RETURNS varchar(255) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci
begin
   declare chars_str varchar(100) default 'qwertyuiopasdfghjklzxcvbnm';
   declare return_str varchar(255) default '';
   declare i int default 0;
   while i<n do
   set return_str=concat(return_str,substring(chars_str,floor(1+rand()*52),1));
   set i=i+1;
   end while;
   return return_str;
 end
~~~
~~~
SELECT rand_string(100)
~~~
######重复拼接字符串
~~~
SELECT REPEAT('yinkai',2)
~~~
输出yinkaiyinkai

######比较字符串
~~~
-- 0
SELECT STRCMP('yinkai','yinkai')
-- 1
SELECT STRCMP('yinkai','yin')
~~~
相同返回0，不同返回1

######uuid
~~~
SELECT REPLACE(UUID(),'-','')
~~~

######字符串转数值

url等大文本转数值
1、crc32
SELECT CRC32('https://www.baidu.com')
crc32很可能出现重复

2、crc64
需要安装 common_schema database函数库

ip转数值

INET_ATON(str)，address to number
INET_NTOA(number)，number to address


