---
title: mysql-myisam引擎.md
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
title: mysql-myisam引擎.md
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
###myisam 特性
myisam 采用表级锁 
读写数据都会对表加锁 ，主要有3中锁类型 
1、read local 
  允许并发读取，但不允许写入。除非是在表尾追加数据 
2、read 
  跟 read local类似 但不允许追加数据 
3、 write 
  会阻塞其他对这张表的读和写操作，真正的独占锁。write锁的性能是最低的 

###myisam引擎的文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ad1036955c184f9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######frm
表定义，是描述表结构的文件。frm文件不管是什么存储引擎都是由它当做表结构文件的。



######MYD
"D" 即是date，数据信息文件，是表的数据文件。

######MYI
"I" 即是 index，索引信息文件，是表数据文件中任何索引的数据树。这点和innodb不同，innodb的数据文件和索引文件都在ibd 文件中。

若使用分区MYD和MYI 在各个分区上都各有一份！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-572c84207b440011.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
