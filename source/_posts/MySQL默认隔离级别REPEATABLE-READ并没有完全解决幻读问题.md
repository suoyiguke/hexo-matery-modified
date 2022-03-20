---
title: MySQL默认隔离级别REPEATABLE-READ并没有完全解决幻读问题.md
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
title: MySQL默认隔离级别REPEATABLE-READ并没有完全解决幻读问题.md
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
RR只是部分解决幻读

MVCC的版本号升级现象，所以RR只解决了脏读，不可重复和幻读都只是部分解决～
https://blog.51cto.com/hcymysql/2541023


