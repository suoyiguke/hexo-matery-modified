---
title: mysql-order-by-rand(-)-优化.md
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
title: mysql-order-by-rand(-)-优化.md
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
简言之，就是把下面这个SQL：

SELECT * FROM test1  ORDER BY RAND() LIMIT 200000

改造成下面这个：

SELECT * FROM test1 t1 JOIN 
 (SELECT RAND() * (SELECT MAX(id) FROM test1) AS nid) t2 
 ON t1.id > t2.nid LIMIT 200000
