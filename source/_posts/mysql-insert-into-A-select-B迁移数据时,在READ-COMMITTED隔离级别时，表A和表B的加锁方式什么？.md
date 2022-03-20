---
title: mysql-insert-into-A-select-B迁移数据时,在READ-COMMITTED隔离级别时，表A和表B的加锁方式什么？.md
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
title: mysql-insert-into-A-select-B迁移数据时,在READ-COMMITTED隔离级别时，表A和表B的加锁方式什么？.md
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
insert into A select B迁移数据时,在READ-COMMITTED隔离级别时，表A和表B的加锁方式什么？

@郑州-税友-常伟俊 8.0.19 是 如果rc+statement 那就是插入数据失败，如果rc+row，a表加个意向排他锁，b不加锁
