---
title: mybatis源码.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis源码.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
org.apache.ibatis.datasource.pooled.PoolState 维护活跃连接和闲置连接


org.apache.ibatis.datasource.pooled.PooledDataSource 使用了PoolState 


###事务
JdbcTransaction

###缓存
CacheKey 中可以添加多个对象，由这些对象共同确定两个 CacheKey 对象是否相同。
在第 章的介绍中，可以见到下面四个部分构成的 CacheKey 对象，也就是说这四部分都会记录到该 acheKey 象的 updateList 集合中。
1、MappedStatement id
2、指定查询结果集的范围，也就是 RowBounds .offset RowBounds.limit
3、查询所使用的 SQL 语句，也就是 boundSql.getSql（）方法返回的 SQL 语句，其中可能包
含“？”占位符。
4、用户传递给上述 SQL 句的实际参数值。
在向 acheKey.updateList 集合中添加对象时，使用的是 CacheKey.update（） 方法，具体实现
如下：
