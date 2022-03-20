---
title: python-时间操作笔记.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: python-时间操作笔记.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
######当前时间
1、获得当前时间戳
~~~
print(int(time.time()))
~~~

2、格式化输出当前时间
~~~
import time
t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print(t)
~~~
######时间戳转格式化字符串
~~~
import datetime
dateArray = datetime.datetime.utcfromtimestamp(1581598281)
t = dateArray.strftime('%Y-%m-%d %H:%M:%S')
print(t)

~~~

######13位时间戳获取方法
~~~
import time
millis = int(round(time.time() * 1000))
print(millis)
~~~

######datetime时间类的转换
~~~
import datetime
import time


# 日期时间字符串
st = "2017-11-23 16:10:10"
# 当前日期时间
dt = datetime.datetime.now()
# 当前时间戳
sp = time.time()

# 1.把datetime转成字符串
def datetime_toString(dt):
    print("1.把datetime转成字符串: ", dt.strftime("%Y-%m-%d %H:%M:%S"))


# 2.把字符串转成datetime
def string_toDatetime(st):
    print("2.把字符串转成datetime: ", datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))


# 3.把字符串转成时间戳形式
def string_toTimestamp(st):
    print("3.把字符串转成时间戳形式:", time.mktime(time.strptime(st, "%Y-%m-%d %H:%M:%S")))


# 4.把时间戳转成字符串形式
def timestamp_toString(sp):
    print("4.把时间戳转成字符串形式: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sp)))


# 5.把datetime类型转外时间戳形式
def datetime_toTimestamp(dt):
    print("5.把datetime类型转外时间戳形式:", time.mktime(dt.timetuple()))


# 1.把datetime转成字符串
datetime_toString(dt)
# 2.把字符串转成datetime
string_toDatetime(st)
# 3.把字符串转成时间戳形式
string_toTimestamp(st)
# 4.把时间戳转成字符串形式
timestamp_toString(sp)
# 5.把datetime类型转外时间戳形式
datetime_toTimestamp(dt)
~~~


1、中文
locale.setlocale(locale.LC_CTYPE, 'chinese')
s_uuid = time.strftime("%Y年%d月%d日%I:%M:%S%p", time.localtime(time.time()))+''.join(str(uuid.uuid1()).split('-'))[25:]
print(s_uuid)
