---
title: Extra的性能优先级.md
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
title: Extra的性能优先级.md
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
Using Index(等值查询的索引覆盖)> 空Extra（等值查询用到索引，但是未索引覆盖）> Using where; Using index（范围查询用到索引且索引覆盖）> Using index condition（范围查询用到索引但是索引未覆盖） >Using where（where条件没有用到索引）
