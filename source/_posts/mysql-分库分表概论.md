---
title: mysql-分库分表概论.md
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
title: mysql-分库分表概论.md
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
###为什么要分库分表
解决大数据存储时数据访问性能，具体来说就是解决超大容量问题和性能问题。

举例说明，订单表或用户表如果数据量达到上亿条记录，此时数据库的IO能力、处理能力就会出现一个瓶颈（MySQL官方统计单表数据量超过1000万性能会逐渐下降）。另




###拆分以后带来的问题
1）跨库join的问题，select a.x,b.y from user a join merchant b on a.id=b.userid

解决方法：

设计的时候充分考虑到应用层的join问题，尽量避免跨库join；

关联表数据可以通过服务层去远程RPC调用，例如上述sql语句，可以先本地查询出a表数据，然后通过远程RPC调用获取关联b表数据；

创建全局表，即在每个数据库中都创建相同的表，数据变更较少的基于全局应用的表；

做字段冗余，用空间换时间，例如在订单表中保存商户id，商户名称。

2）跨分片数据排序分页

解决方法：

在应用层进行数据拼接，对每个表中的数据进行查询，然后按照排序字段再进行数据拼接。

3）唯一主键问题，例如用自增ID做主键，分库后必然会出现重复主键

解决方法：

用UUID作为主键，UUID字符串比较大，造成生成的索引较大，性能较低；

利用Snowflake雪花算法生成主键，根据时间序列、机器标识、技术顺序号，按照指定算法生成唯一ID；

借助MongoDB的ObjectId作为唯一主键；

借助zookeeper自动生成递增ID作为唯一主键。

4）分布式事务

多个数据库表之间保证原子性
84495059
