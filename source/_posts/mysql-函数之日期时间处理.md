---
title: mysql-函数之日期时间处理.md
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
title: mysql-函数之日期时间处理.md
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
>于人曰浩然，沛乎塞苍冥

日期和时间采用相应的数据类型和特殊的格式存储，以便能快速和
有效地排序或过滤，并且节省物理存储空间（出于性能的考虑，不允许直接存储字符串）。


###使用示例

######当前时间
~~~
-- 当前日期-时间  2020-04-19 17:08:29
SELECT now()
-- 当前日期 2020-04-19
SELECT CurDate()
-- 当前时间 17:08:22
SELECT CurTime()
-- 当前时间戳 1587289920
SELECT UNIX_TIMESTAMP()
~~~

######时间参数提取
1、直接使用对应函数
~~~

-- 时间的日期部分 2020-04-19
SELECT Date(now())

-- 时间：时:分:秒

SELECT time(now())

-- 月份
SELECT MONTH(now())

-- 年
SELECT YEAR(now())

-- 秒
SELECT SECOND(now())

-- 分钟
SELECT Minute(now())

-- 小时
SELECT Hour(now())

-- 星期几
SELECT DayOfWeek(now())


-- 一年中第几周 16
SELECT WEEK(now()) 

-- 天
SELECT Day(now())


~~~
2、使用高度灵活的EXTRACT()函数
> SELECT EXTRACT(unit FROM date)  有两个参数；第一个是时间单位（在本文后面有列出），第二个是具体时间

~~~
SELECT EXTRACT(MICROSECOND FROM now())
SELECT EXTRACT(YEAR_MONTH FROM now())
~~~



######时间计算

1、高度灵活的日期运算函数
> SELECT DATE_ADD(date,INTERVAL expr unit); 第一个参数为具体时间，第二个参数为计算数值，第三个参数为时间单位（在后面有列）
~~~
SELECT DATE_ADD(now(),INTERVAL 1 MICROSECOND)
SELECT DATE_ADD(now(),INTERVAL 1 MINUTE)
SELECT DATE_ADD(now(),INTERVAL 1 HOUR)
SELECT DATE_ADD(now(),INTERVAL 1 DAY)
SELECT DATE_ADD(now(),INTERVAL -1 DAY)
SELECT DATE_ADD(now(),INTERVAL 1 WEEK)
SELECT DATE_ADD(now(),INTERVAL 1 MONTH)
SELECT DATE_ADD(now(),INTERVAL 1 QUARTER)
SELECT DATE_ADD(now(),INTERVAL 1 YEAR)
~~~
同样，SELECT DATE_SUB(date,INTERVAL expr unit)即是灵活的时间/日期减法函数

2、加减日期
> SELECT ADDDATE(expr,days)；这是一个ADDDATE的重载，参数1具体时间，参数2添加天数
~~~
SELECT ADDDATE(now(),1)
~~~
3、加减时间
>SELECT ADDTIME(expr1,expr2); 参数1为具体时间，参数2为添加大小
~~~
SELECT ADDTIME('2018-10-31 23:59:59','0:1:1'),ADDTIME('10:30:59','5:10:37');
~~~

3、计算日期之差
> SELECT DATEDIFF(expr1,expr2)；参数1时间，参数2时间；返回时间相差的天数
~~~
SELECT DATEDIFF(DATE_ADD(now(),INTERVAL 1 DAY),now())    
~~~



######格式化输出
~~~
-- 把字符串转为日期格式
SELECT DATE_FORMAT('2017-09-20 08:30:45',   '%Y-%m-%d %H:%i:%S');

-- 把日期转为字符串格式
SELECT DATE_FORMAT(NOW(),   '%Y-%m-%d %H:%i:%S');

-- 时间戳格式化输出
SELECT FROM_UNIXTIME(1587289920, '%Y-%m-%d %H:%i:%S')
~~~


######随机得到两个日期-时间范围内的日期-时间
~~~
SET @startdate:='2019-01-01 00:00:00';
SET @enddate:='2020-12-31 23:59:59';
SELECT FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(@startdate)+RAND()*(UNIX_TIMESTAMP(@enddate)-UNIX_TIMESTAMP(@startdate))))
~~~
分装为函数
~~~
CREATE DEFINER="root"@"%" FUNCTION "getDateTime"(`start` datetime,`end` datetime) RETURNS datetime
BEGIN
RETURN FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(start)+RAND()*(UNIX_TIMESTAMP(end)-UNIX_TIMESTAMP(start))));
END
~~~
> SELECT getDateTime('2019-01-01 00:00:00','2020-12-31 23:59:59');


###附录


######mysql中的时间单位枚举选项
>MICROSECOND
SECOND
MINUTE
HOUR
DAY
WEEK
MONTH
QUARTER
YEAR
SECOND_MICROSECOND
MINUTE_MICROSECOND
MINUTE_SECOND
HOUR_MICROSECOND
HOUR_SECOND
HOUR_MINUTE
DAY_MICROSECOND
DAY_SECOND
DAY_MINUTE
DAY_HOUR
YEAR_MONTH

######mysql中格式化参数
>%M 月名字(January……December)
%W 星期名字(Sunday……Saturday)
%D 有英语前缀的月份的日期(1st, 2nd, 3rd, 等等。）
%Y 年, 数字, 4 位
%y 年, 数字, 2 位
%a 缩写的星期名字(Sun……Sat)
%d 月份中的天数, 数字(00……31)
%e 月份中的天数, 数字(0……31)
%m 月, 数字(01……12)
%c 月, 数字(1……12)
%b 缩写的月份名字(Jan……Dec)
%j 一年中的天数(001……366)
%H 小时(00……23)
%k 小时(0……23)
%h 小时(01……12)
%I 小时(01……12)
%l 小时(1……12)
%i 分钟, 数字(00……59)
%r 时间,12 小时(hh:mm:ss [AP]M)
%T 时间,24 小时(hh:mm:ss)
%S 秒(00……59)
%s 秒(00……59)
%p AM或PM
%w 一个星期中的天数(0=Sunday ……6=Saturday ）
%U 星期(0……52), 这里星期天是星期的第一天
%u 星期(0……52), 这里星期一是星期的第一天
%% 一个文字“%”。
