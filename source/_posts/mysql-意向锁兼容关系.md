---
title: mysql-意向锁兼容关系.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-意向锁兼容关系.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---


从锁的粒度和范围，大致分三类：全局锁，表锁，行锁。
共享锁S，与排它锁X均为行锁。innodb支持对更粗粒度（数据库级，表级，页级）加意向锁。MYSQL意向共享锁IS及意向排他锁IX均属于表级锁。

![image](//upload-images.jianshu.io/upload_images/13932735-ed72ec05278d0b0a.png?imageMogr2/auto-orient/strip|imageView2/2/w/809/format/webp)

![image](//upload-images.jianshu.io/upload_images/13932735-761ab67736442e9b.png?imageMogr2/auto-orient/strip|imageView2/2/w/856/format/webp)

IS、IX相互兼容，S兼容S、IS，X谁都不兼容
**注：截图来源<高性能MySQL（第三版）>**

