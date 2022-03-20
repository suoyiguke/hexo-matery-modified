---
title: mysql-子查询在update、delete中和select中的区别.md
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
title: mysql-子查询在update、delete中和select中的区别.md
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
https://dev.mysql.com/doc/refman/5.7/en/subquery-optimization.html

update和delete不支持semijoin和Materialization的子查询优化，改写成join试试吧
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6b2bd3cbf97bebf7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
