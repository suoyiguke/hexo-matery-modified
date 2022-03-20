---
title: mysql-线上导出数据影响测试.md
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
title: mysql-线上导出数据影响测试.md
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
1、使用navicat 导出结构和数据不会影响到insert插入。不会加锁

2、使用 INSERT into tb_box_cp1  SELECT * FROM `tb_box`  语句copy数据到另一张表也不会影响insert。

但是要注意，若添加了where条件，且字段没有添加索引或索引失效。那么会锁主全表记录。where条件之外的
的insert特定行会被阻塞，直到insert select 语句执行完毕！

但是直接在原来表的尾巴insert是不会阻塞的。
