---
title: mysql-的页大小.md
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
title: mysql-的页大小.md
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
在计算机中磁盘存储数据最小单元是扇区，一个扇区的大小是 512 字节，而文件系统（例如XFS/EXT4）他的最小单元是块，一个块的大小是 4k，而对于我们的 InnoDB 存储引擎也有自己的最小储存单元——页（Page），一个页的大小是 16K。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-5e8205ff1e1dc63e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-7ab35637779cffe3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
