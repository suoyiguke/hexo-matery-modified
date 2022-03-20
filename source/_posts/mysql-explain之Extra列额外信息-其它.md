---
title: mysql-explain之Extra列额外信息-其它.md
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
title: mysql-explain之Extra列额外信息-其它.md
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
###官网信息
https://dev.mysql.com/doc/refman/5.7/en/explain-output.html

### FirstMatch(b)
半连接的一种策略

###LooseScan
半连接的一种策略
松散扫描(LooseScan)策略 关于LooseScan更多信息: 列出使用到LooseScan的情景：group by、distinct、max()等
https://dev.mysql.com/doc/refman/5.7/en/group-by-optimization.html
与之对应的就是紧密索引扫描


###batched_key_access 
BKA是一种join算法，区别于NLJ
开启BKA后，若没有完成索引覆盖。则bka可以对回表查询IO进行优化

###mrr

###mrr_cost_based 


###配置
https://dev.mysql.com/doc/refman/5.7/en/switchable-optimizations.html#optflag_batched-key-access

SELECT @@optimizer_switch\G
index_merge = ON,
index_merge_union = ON,
index_merge_sort_union = ON,
index_merge_intersection = ON,
engine_condition_pushdown = ON,
index_condition_pushdown = ON,
mrr = ON,
mrr_cost_based = ON,
block_nested_loop = ON,
batched_key_access = off, 
materialization = ON,
semijoin = ON,
loosescan = ON,
firstmatch = ON,
duplicateweedout = ON,
subquery_materialization_cost_based = ON,
use_index_extensions = ON,
condition_fanout_filter = ON,
derived_merge = ON,
prefer_ordering_index = ON
