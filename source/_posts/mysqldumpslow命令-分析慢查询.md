---
title: mysqldumpslow命令-分析慢查询.md
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
title: mysqldumpslow命令-分析慢查询.md
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
一般线上的慢查询日志会飞常大。可能到2G。这时候去提取信息会麻烦些。
我们可以使用mysqldumpslow 
tail -n 100000  mysql-slow.log > slowsql.log
mysqldumpslow slowsql.log


