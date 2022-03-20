---
title: mysql-事务之基本用法与手动提交.md
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
title: mysql-事务之基本用法与手动提交.md
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
###mysql中使用事务

######1、用begin,rollback,commit来实现

>- begin    开始一个事务
>- rollback 事务回滚
>- commit  事务提交


######使用begin的方式开启事务试验
提交一个事务示例
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0241e803a1f2f40d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
回滚一个事务示例
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1991cd8d23bc53d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######2、使用 set @@autocommit  = 0开启事务
>- mysql默认是自动提交的，也就是你提交一个query，就直接执行！
>- set @@autocommit  = 0 禁止自动提交
>- set @@autocommit = 1 开启自动提交

######关于mysql的手动提交和自动提交
主要是看@@autocommit 值
> 0 表示手动提交，即使用mysql客户端执行 sql后必须使用commit命令提交事务，否则所执行的 sql 无效，如果想撤销事务则使用 rollback 命令。`在手动提交模式下的set autocommit = 0、commit和rollback 命令都会隐式的开启一个新事务`

> 1 表示自动提交，即在 mysql 客户端下不再需要手动执行 commit 命令。`MySQL 在自动提交模式下，每个 SQL 语句都是一个独立的事务`，所以这样会带来一定程度的性能问题。
- mysql 客户端默认为 1，默认是自动提交的
- 查看当前客户端的autocommit值：select @@autocommit;
- 修改当前连接的事务提交方式为手动提交命令：set @@autocommit = 0;



- 手动设置set @@autocommit = 0，即设定为非自动提交模式，只对当前的mysql命令行窗口有效


######使用autocommit 的方式开启事务
提交一个事务示例
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b989f0c1aab029f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

回滚一个事务示例
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ea3c9a0eab09301b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
