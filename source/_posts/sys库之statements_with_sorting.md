---
title: sys库之statements_with_sorting.md
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
title: sys库之statements_with_sorting.md
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
找出线上using filesort的sql

SELECT * from sys.statements_with_sorting where db='mgb_treasure_system' order by  rows_sorted desc limit 10
