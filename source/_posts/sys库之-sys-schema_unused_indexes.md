---
title: sys库之-sys-schema_unused_indexes.md
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
title: sys库之-sys-schema_unused_indexes.md
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
查看未使用的索引
SELECT * from sys.schema_unused_indexes where object_schema='mgb_treasure_system' 

8.0 可以将索引设置为不可见的。


| schema_unused_indexes

使用索引的表

object_schema 库名

object_name 表名

index_name 未使用的索引名称
