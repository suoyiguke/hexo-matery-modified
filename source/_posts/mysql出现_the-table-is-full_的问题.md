---
title: mysql出现_the-table-is-full_的问题.md
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
title: mysql出现_the-table-is-full_的问题.md
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
SHOW VARIABLES LIKE '%ibuf_pool_size_per%'


SHOW VARIABLES LIKE '%tmp_table_size%' SHOW VARIABLES LIKE '%max_heap_table_size%' SHOW VARIABLES LIKE '%datadir%' 
SET GLOBAL tmp_table_size = 32 M 
SET GLOBAL tmp_table_size = 32 * 1024 * 1024;
