---
title: mysql-使用show-profiles性能分析和记录最近sql.md
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
title: mysql-使用show-profiles性能分析和记录最近sql.md
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
介绍：是mysql提供可以用来分析当前会话中语句执行的资源消耗情况。可以用于SQL的调优测量

我们知道：sql值慢主要是cpu和IO 慢
1、查看是否开启
- profiling = ON 开启 ； profiling = OFF 关闭
- profiling_history_size=15 保存最近15次sql
~~~
SHOW VARIABLES LIKE 'profiling%';
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e8dbea01605f2e56.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2、开启
~~~
set profiling=1;
~~~
3、修改记录sql条数
~~~
set profiling_history_size = 50
~~~
4、查看最近执行的sql
~~~
show profiles;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c4e1f7a34a85eea6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


5、查看某条sql的耗时信息；上一步前面的问题SQL 数字号码；
~~~
show profile cpu, block io for query 问题sql数字号码;
~~~

~~~
ALL: 显示所有的开销信息
BLOCK IO ： 显示块IO相关开销
CONTEXT SWITCHS: 上下文切换相关开销
CPU : 显示cpu 相关开销
IPC: 显示发送和接收相关开销
MEMORY： 显示内存相关开销
PAGE FAULTS：显示页面错误相关开销信息
SOURCE ： 显示和Source_function ,Source_file,Source_line 相关的开销信息
SWAPS：显示交换次数相关的开销信息
Status ： sql 语句执行的状态
Duration: sql 执行过程中每一个步骤的耗时
CPU_user: 当前用户占有的cpu
CPU_system: 系统占有的cpu
Block_ops_in : I/O 输入
Block_ops_out : I/O 输出
~~~

###出现以下情况说明sql性能问题，需要调优

- converting HEAP to MyISAM 查询结果太大，内存都不够用了往磁盘上搬了。
- Creating tmp table 、removing tmp table创建临时表、拷贝数据到临时表、用完再删除
- Copying to tmp table on disk 把内存中临时表复制到磁盘，危险！！！
- locked

###实验

1、执行查询
~~~
select * from emp group by id%10 limit 150000;
select * from emp group by id%20 order by 5;
show profiles;
~~~
2、分析相应sql耗时
~~~
show profile cpu,block io for query 116;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0f9ee8cc60f03ede.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###Sending data时间过长
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d30936ceb73d06c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

发现很长一段时间，查询都处在 “Sending data”状态

查询一下“Sending data”状态的含义，原来这个状态的名称很具有误导性，所谓的“Sending data”并不是单纯的发送数据，而是包括“收集 + 发送 数据”。

这里的关键是为什么要收集数据，原因在于：mysql使用“索引”完成查询结束后，mysql得到了一堆的行id，如果有的列并不在索引中，mysql需要重新到“数据行”上将需要返回的数据读取出来返回个客户端。
可能是下面的情况
- select中有大文本字段
