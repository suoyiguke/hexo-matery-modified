---
title: mysql-分库.md
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
title: mysql-分库.md
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
###分库比分表有啥优势么
分库的话，对应道到不同服务器上的MySQL，这样你数据库的压力就分担了哩，同时又高可用。那在同一个服务器上分库就是傻叉行为了

###分库
垂直分库：解决数据表过多问题，按照功能模块、业务维度、ER图、领域模型等把相关联的表部署在一个数据库上。

######垂直分库
按照功能模块、业务维度、ER图、领域模型等进行表划分，将相关联的表放到统一数据库中，避免跨库关联join
######水平分库
