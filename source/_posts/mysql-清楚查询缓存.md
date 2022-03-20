---
title: mysql-清楚查询缓存.md
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
title: mysql-清楚查询缓存.md
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
进行sql优化时，连续执行两个sql。想要看看他们的效率差别。但是因为mysql有查询缓存的存在，导致两次sql查询差别不明显。

~~~
FLUSH QUERY CACHE; -- // 清理查询缓存内存碎片。
RESET QUERY CACHE; -- // 从查询缓存中移出所有查询。
FLUSH TABLES; -- //关闭所有打开的表，同时该操作将会清空查询缓存中的内容。
~~~

设置
~~~
SET GLOBAL innodb_old_blocks_time = 250; 
 SET GLOBAL innodb_old_blocks_pct = 5; 
 SET GLOBAL innodb_max_dirty_pages_pct = 0; 
  ~~~

恢复
~~~
SET GLOBAL innodb_old_blocks_time = 1000; 
 SET GLOBAL innodb_old_blocks_pct = 37; 
 SET GLOBAL innodb_max_dirty_pages_pct = 75.000000 ; 
~~~

查询
~~~
SELECT @@innodb_old_blocks_time
SELECT @@innodb_old_blocks_pct
SELECT @@innodb_max_dirty_pages_pct
~~~



SELECT count(*) from sbtest10 -- 0.619
![image.png](https://upload-images.jianshu.io/upload_images/13965490-edad481e239a74fd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-11dd06fc7ed4bf2b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



快 0.064
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d8a128658425c006.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6ebd33c979819b6e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
