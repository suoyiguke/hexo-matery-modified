---
title: musql-主从复制之相关配置参数.md
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
title: musql-主从复制之相关配置参数.md
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
###slave_skip_errors跳过错误
1、跳过指定个数的event
一般来说，为了保险起见，在主从库维护中，有时候需要跳过某个无法执行的命令，需要在slave处于stop状态下，执行 set global sql_slave_skip_counter=1以跳过命令。但在测试和开发环境下，有时候为了快速解决不影响开发，需要使用set global sql_slave_skip_counter=N，其意思即为在start slave时，从当前位置起，跳过N个event。每跳过一个event，则 N--

2、使用跳过指定错误
配置实例


~~~
slave_skip_errors=1007,1008,1050,1051,1054,1060,1061,1068,1094,1146,1053,1062
slave-skip-errors=1062,1053
slave-skip-errors=all
slave-skip-errors=ddl_exist_errors
~~~
The shorthand value ddl_exist_errors is equivalent to the error code list 1007,1008,1050,1051,1054,1060,1061,1068,1094,1146.

除了跳过N个event外，还有一个很重要的参数是slave-skip-errors，其有四个可用值，分别为：off、all、ErorCode、ddl_exist_errors。
![技术分享](https://upload-images.jianshu.io/upload_images/13965490-06056479ae55321e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

根据各个值得字面意思即可知道它们的用法，但是其中ddl_exist_errors值却比较特别，它代表了一组errorCode的组合，分别是：
1007：数据库已存在，创建数据库失败
1008：数据库不存在，删除数据库失败
1050：数据表已存在，创建数据表失败
1050：数据表不存在，删除数据表失败
1054：字段不存在，或程序文件跟数据库有冲突
1060：字段重复，导致无法插入
1061：重复键名
1068：定义了多个主键
1094：位置线程ID
1146：数据表缺失，请恢复数据库


###log-slave-updates
log-slave-updates这个参数用来配置从库上的更新操作是否写二进制日志，默认是不打开 的。但是，如果这个从库同时也要作为其他服务器的主库，搭建一个链式的复制，那么就需要 打开这个选项，这样它的从库将获得它的二进制日志以进行同步操作。
这个启动参数需要和-logs-bin参数一起使用。

### master-connect-retry
master-connect-retry这个参数用来设置在和主库的连接丢失时重试的时间间隔，默认是60 秒，即每60秒重试一次。

### read-only
read-only该参数用来设置从库只能接受root超级用户的更新操作,从而限制应用程序错误的对从库的更新操作。下面创建了一个普通用户，在默认情况下，该用户是可以更新从数据库中的数据的，但是使用read-only选项启动从数据库以后，该用户对从数据库的更新会提示错误。

###指定从机复制的数据库或者表
可以使用replicate-do-db、replicate-do-table、replicate-ignore-db、replicate-ignore-table或 replicate-wild-do-table来指定从主数据库复制到从数据库的数据库或者表。有时用户只需要将关键表备份到从库上，或者只需要将提供查询操作的表复制到从库上，这样就可以通过配置这 几个参数来筛选进行同步的数据库和表。

###指定主机记录binlog的数据库或者表
binlog-do-db 
