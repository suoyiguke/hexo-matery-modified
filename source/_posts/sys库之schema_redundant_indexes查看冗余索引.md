---
title: sys库之schema_redundant_indexes查看冗余索引.md
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
title: sys库之schema_redundant_indexes查看冗余索引.md
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
SELECT * from sys.schema_redundant_indexes  where table_schema='mgb_treasure_system' 


| schema_redundant_indexes

冗余索引

table_schema

table_name 表名

redundant_index_name 冗余索引名称

redundant_index_columns 冗余索引的列名称

redundant_index_non_unique  冗余索引中的列的数量

dominant_index_name 索引名称

dominant_index_columns 列的名称

dominant_index_non_uniqu

subpart_exists 是否索引一部分

sql_drop_index 要执行的语句 删除冗余索引
