---
title: MySQL过亿的大表是怎么解决的？.md
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
title: MySQL过亿的大表是怎么解决的？.md
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
但行好事  莫问前程:
MySQL过亿的大表是怎么解决的？

但行好事  莫问前程:
如何保证其性能？

但行好事  莫问前程:
我这边是做了冷热数据隔离。

但行好事  莫问前程:
系统运行一段时间后，比较久的数据就通过时间字段，归档起来。

但行好事  莫问前程:
MySQL大表的数据保留在5000万左右。

RegulusZ:
sharding分表？

但行好事  莫问前程:
避免单表数据量过大。

但行好事  莫问前程:
分表中间件，过一段时间都不维护了。

走失的小老虎儿:
mysql 单表大了就玩不转了。 这是硬伤

戒糖低盐轻碳水:
基本都这样

潘佳伟:
@北京-青牛-王寒 一般多大会玩不转

但行好事  莫问前程:
架构师告诉我超过5000万左右，性能下降的厉害。

我们系统一般快上亿就特别不好了，我们机器的配置较差。配置高的情况下，可能稍微好点。
所以我们一般都是分表，1个月分一个表
