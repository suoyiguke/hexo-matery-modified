---
title: python-字符串操作笔记.md
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
title: python-字符串操作笔记.md
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
######判断字符串中是否包含指定字符
~~~
str = 'yinkai'
if str.find('y') != -1:
    print('yes')
else:
    print('no')
~~~
######去除空格

~~~
str = 'yin kai'
replace = str.strip().replace("\n", "")
print(replace)
~~~
######字符串和数字拼接
~~~
str = "http://v.huya.com/lol/new_"+str(100)+".html"
print(str)
~~~
######字符串截取
1、按位截取
~~~
str = '0123456789'
print(str[0:3])  # 截取第一位到第三位的字符
print(str[:])  # 截取字符串的全部字符
print(str[6:])  # 截取第七个字符到结尾
print(str[:-3])  # 截取从头开始到倒数第三个字符之前
print(str[2])  # 截取第三个字符
print(str[-1])  # 截取倒数第一个字符
print(str[::-1])  # 创造一个与原字符串顺序相反的字符串
print(str[-3:-1])  # 截取倒数第三位与倒数第一位之前的字符
print(str[-3:])  # 截取倒数第三位到结尾
print(str[:-5:-3])  # 逆序截取，具体啥意思没搞明白？


str = '/play/133375971.html'
print(str[6:-5])  # 截取第一位到第三位的字符
~~~

2、按字符截取
知道首尾字符，截取中间的字符串
~~~
content_ = '(yinkai)'
content__ = content_[content_.find('(')+1:content_.rfind(')')]
print(content__)
~~~

######字符串比较
- Is比较的是两个对象的id值是否相等，也就是比较俩对象是否为同一个实例对象，是否指向同一个内存地址。

- == 比较的是两个对象的内容是否相等，默认会调用对象的__eq__()方法。

~~~
s1 = 'yinkai'
s2 = 'yinkai'
s3 = 'yin'+'kai'
s4 = str('yinkai')
print(s1 is s2) # True
print(s1 == s2) #True
print(s1.__eq__(s2)) #True

print(s1 is s3) # True
print(s1 == s3) #True
print(s1.__eq__(s3)) #True

print(s1 is s4) # True
print(s1 == s4) #True
print(s1.__eq__(s4)) #True
~~~

######生成UUID
~~~
import uuid

s_uuid = ''.join(str(uuid.uuid1()).split('-'))
print(s_uuid)
~~~

######大小写转换函数
capitalize() 首字母大写，其余全部小写 
upper() 全转换成大写
lower() 全转换成小写
title()  标题首字大写
~~~
print('yinkai'.capitalize())
print('yinkai'.upper())
print('YINKAI'.lower())
print('yinkai'.title())
~~~
######url 编码和解码
~~~
from urllib.parse import urlencode, unquote, quote

print(urlencode({"arg1": 1, "arg2": 2}))
print(quote("测试"))
print(unquote("%E6%B5%8B%E8%AF%95"))
~~~
######字符串提取数字
~~~
import re
s = 'speed=210,angle=150'
m = re.findall(r'(\w*[0-9]+)\w*',s)
print(m)
~~~

######splid分割字符串
~~~
str = "www.cyzxn.cn,www.yingmuzhi.cn";
split = str.split(',')
for s in split:
    print(s)
~~~

######字符转数字

int(x [,base ])                               将x转换为一个整数
long(x [,base ])                            将x转换为一个长整数
float(x )                                       将x转换到一个浮点数
complex(real [,imag ])                  创建一个复数
str(x )                                          将对象 x 转换为字符串
repr(x )                                       将对象 x 转换为表达式字符串
eval(str )                                     用来计算在字符串中的有效Python表达式,并返回一个对象
tuple(s )                                      将序列 s 转换为一个元组
list(s )                                          将序列 s 转换为一个列表
chr(x )                                         将一个整数转换为一个字符
unichr(x )                                    将一个整数转换为Unicode字符
ord(x )                                         将一个字符转换为它的整数值

######解析url参数
~~~
import urllib.parse

url = "https://ss.yy.com/pages/viewpage.action?userId=9434&pageId=1"
result = urllib.parse.urlsplit(url)
query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
ip = urllib.parse.urlsplit(url).netloc

path = urllib.parse.urlsplit(url).path
new_url = urllib.parse.urlparse(url)

print('第一、urllib.parse.urlsplit(url)=', result)
print('第二、dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))=', query)
print('ip或者域名=', ip)
print('ip或者域名=', new_url.netloc)
print('path路径=', path)
print('userId=', query['userId'], 'pageId=', query['pageId'])
~~~

######解析m3u8文件中的字符串，获得ts路径
~~~
import re
html_str = "#EXTM3U\n" +"#EXT-X-VERSION:3\n" +"#EXT-X-MEDIA-SEQUENCE:1\n" +"#EXT-X-TARGETDURATION:6\n" +"#EXTINF:5.000,\n" +"../../../../../record/huyalive/1419913746-1419913746-6098483102210850816-4516515348-10057-A-0-1_4000/1553344050_192043.ts\n" +"#EXTINF:5.000,\n" +"../../../../../record/huyalive/1419913746-1419913746-6098483102210850816-4516515348-10057-A-0-1_4000/1553344055_192044.ts\n" +"#EXTINF:5.000,\n" +"../../../../../record/huyalive/1419913746-1419913746-6098483102210850816-4516515348-10057-A-0-1_4000/1553344060_192045.ts\n" +"#EXTINF:5.000,\n" +"../../../../../record/huyalive/1419913746-1419913746-6098483102210850816-4516515348-10057-A-0-1_4000/1553344065_192046.ts\n"
local = re.findall(r',\n(.*)\n', html_str)
for str in local:
    if str.find(".ts")!=-1:
      print(str)
~~~


######获得url的后缀
~~~
s = "http://1251883823.vod2.myqcloud.com/0ca1536bvodcq1251883823/19db1ecd5285890793731562323/playlist.m3u8"
pos = s.rfind("/")
print(s[pos:] )
~~~

######字符串fomat
~~~
str = 'helll,{name},my sex is{sex}'
str_format = str.format(name='yinkai', sex='man')
print(str_format)
~~~
######替换字符串中指定位置
~~~
#替换字符串string中指定位置p的字符为c
def sub(string,p,c):
    new = []
    for s in string:
        new.append(s)
    new[p] = c
    return ''.join(new)

zz = sub("yinkai",0,'hello is me!')
print(zz)
~~~

###去掉换行符号
~~~
line.strip('\n')
~~~


###替换第一次出现的字符串
~~~
replace = "//www.jb51.net/article/202001.htm".replace('//', 'http://', 1)
print(replace)
~~~


###join，按逗号分隔
~~~
#!/usr/bin/python
# -*- coding: UTF-8 -*-
  
L = [1,2,3,4,5]
s1 = ','.join(str(n) for n in L)
print s1
~~~

###rstrip() 删除末尾字符
~~~
str = "     this is string example....wow!!!     "
print (str.rstrip())
str = "*****this is string example....wow!!!*****"
print (str.rstrip('*'))
~~~


