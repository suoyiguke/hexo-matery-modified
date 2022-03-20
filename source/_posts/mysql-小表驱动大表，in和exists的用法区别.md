---
title: mysql-小表驱动大表，in和exists的用法区别.md
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
title: mysql-小表驱动大表，in和exists的用法区别.md
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
###小表驱动大表的原理
可以使用for循环来理解


###经验
按照“小表驱动大表”的优化经验，可以得出in和exists的使用经验

1、当子查询数据集大小小于父查询数据集时，使用in

2、当子查询数据集大小大于父查询数据集时，使用exists

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1078653619cda226.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

