---
title: 慢查询日志分析工具之-mysqldumpshow.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: 慢查询日志分析工具之-mysqldumpshow.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---


###日志分析工具mysqldumpshow
####参数说明
  s:是表示按何种方式排序
  c:访问次数
  l:锁定时间
  r:返回记录
  t:查询时间
  al:平均锁定时间
  ar:平均返回记录数
  at:平均查询时间
  t:即为返回前面多少条的数据
  g:后边搭配一个正则匹配模式，大小写不敏感的

####在window下使用
1、下载ActivePerl_5.16.2.3010812913.msi。安装后将安装目录的bin配置搭配系统环境变量的path下；我这里是C:\Perl\bin
- 下载地址 https://pan.baidu.com/s/1i3GLKAp

![image.png](https://upload-images.jianshu.io/upload_images/13965490-27f8279a22930d8c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、找到mysqldumpslow.pl的路径,cd进入目录，执行help命令。如下输出证明环境好了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-194e6bd30d63cd3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
~~~
C:\Users\yinkai>cd G:\mysql\mysql-5.7.22-winx64\bin
C:\Users\yinkai>g:
G:\mysql\mysql-5.7.22-winx64\bin>perl mysqldumpslow.pl --help
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bddf603719ff2a2b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、执行
~~~
mysqldumpslow.pl -s r -t 10  G:\mysql\mysql-5.7.22-winx64\data\DESKTOP-ALJL296-slow.log
~~~
输出情况
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fdd1403a351a2364.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


####一些例子：
~~~
得到返回记录集最多的10个SQL。
mysqldumpslow.pl -s r -t 10  G:\mysql\mysql-5.7.22-winx64\data\DESKTOP-ALJL296-slow.log
得到访问次数最多的10个SQL
mysqldumpslow.pl -s c -t 10  G:\mysql\mysql-5.7.22-winx64\data\DESKTOP-ALJL296-slow.log
得到按照时间排序的前10条里面含有左连接的查询语句。
mysqldumpslow.pl -s t -t 10 -g “left join”  G:\mysql\mysql-5.7.22-winx64\data\DESKTOP-ALJL296-slow.log
另外建议在使用这些命令时结合 | 和more 使用 ，否则有可能出现刷屏的情况。
mysqldumpslow.pl -s r -t 20 G:\mysql\mysql-5.7.22-winx64\data\DESKTOP-ALJL296-slow.log | more
~~~

