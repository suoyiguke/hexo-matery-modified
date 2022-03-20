---
title: mysql-的-_rowid.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-的-_rowid.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
MySQL中有一个隐藏列_rowid来标记唯一的标识。但是需要注意_rowid并不是一个真实存在的列，其本质是一个非空唯一列的别名。

>PS：本文是基于MySQL 5.7进行研究的

在某些情况下_rowid是不存在的

###_rowid什么时候存在，什么时候又不存在？
######其只存在于以下情况：

1、当表中存在一个数字类型的单列主键时，_rowid其实就是指的是这个主键列

数值类型+单列主键

2、当表中不存在主键但存在一个数字类型的非空唯一列时，_rowid其实就是指的是对应非空唯一列。

数值类型+非空+唯一索引

######需要注意以下情况是不存在_rowid的

1、主键列或者非空唯一列的类型不是数字类型 （uuid为主键的表没有_rowid）
2、主键是联合主键
3、唯一列不是非空的。

###_rowid表示的是什么？
rowid 可以显示表的主键,即使没有显式的指定主键，也会去选择一个 非空、唯一、数值类型的列做主键。
若没有找到符合条件的列，那么_rowid列就不存在了。innodb引擎将Z自动创建一个6字节大小的指针
###有多个符合条件的列，那么_rowid使用哪一个？
当表中有多个非空唯一索引时, InnoDB存储引擎将选择建表时`第一个`定义的非空唯 一索引为主键。这里需要非常注意的是主键的选择根据的是`定义索引的顺序`,而不是 建表时列的顺序。
