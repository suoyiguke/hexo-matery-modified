---
title: mysql-线上捕获sql的方法.md
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
title: mysql-线上捕获sql的方法.md
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
1、首先要得到一份线上都在跑的sql列表
2、常用sql捕获方式
  - 基于 TCPDUMP
  - 基于查询日志记录
  - 基于 slow query log

![image.png](https://upload-images.jianshu.io/upload_images/13965490-5884d135fb1bf325.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###捕获的sql分析方法
推荐工具 pt-query-digest
输出分块
- 文件概述部分
- Profile部分
- 具体sql部分

分析重点：
1、数量最多的
2、并发度高的
3、占用时间多的

###读写分离的目标
我们需要在哪些sql中做读写分离？

一定不是所有的sql，是业务中核心的部分。经常执行的sql，比如飞信平台，60%的sql都是获取好友列表，将之放到从库中。效率大大提升；

1、一个事务里有读有写是做不了读写分离的，全职在主库完成！
2、对实时性要求高的请在主库

###利用平台来收集慢查询日志
Anemometer

###怎么查看tps，什么硬件能达到 6W tps


###binlog分析
统计表的update次数等等
https://github.com/wubx/mysql-binlog-statistic

###mysql源码
