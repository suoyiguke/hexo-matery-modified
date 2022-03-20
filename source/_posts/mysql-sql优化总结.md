---
title: mysql-sql优化总结.md
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
title: mysql-sql优化总结.md
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
###优化步骤
1、观察，至少跑一天，看看生成的慢sql情况
2、开启慢查询日志，设置阈值，比如超过5秒钟就是慢sql，并抓取出来
3、explain + 慢sql分析
4、show profile
     查询sql在mysql服务器里执行细节和生命周期情况
5、运维经理或DBA，进行sql数据库服务器的参数调优
