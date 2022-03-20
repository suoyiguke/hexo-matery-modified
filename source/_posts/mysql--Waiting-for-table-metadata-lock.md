---
title: mysql--Waiting-for-table-metadata-lock.md
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
title: mysql--Waiting-for-table-metadata-lock.md
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
###解决方案
1、SHOW  PROCESSLIST，得到Waiting for table metadata lock 的 id。然后kill之
2、 设置ddl语句超时时间，注意需要在出现问题之前就设置，可以防止一直阻塞下去。就连读都会有影响的！
~~~
SET GLOBAL lock_wait_timeout = 50
SET session lock_wait_timeout = 50
~~~



###我遇到的问题

线上遇到保存签名原文的问题，特殊表情符号不能不保存。于是去修改这个字段的字符编码。
~~~
ALTER TABLE `biz_cloudsign_sign_details`
MODIFY COLUMN `source_data`  longtext CHARACTER SET utf8mb4 NOT NULL AFTER `source_data`;
~~~

然后这条语句迟迟得不到执行成功，SHOW PROCESSLIST，得到Waiting for table metadata lock 的 id。
insert语句全部被阻塞。但是不知道为什么用户流程那边没有出现问题。难道是mybatis有自动超时返回机制？这个需要验证下。

所以说线上ddl操作非常危险！


![image.png](https://upload-images.jianshu.io/upload_images/13965490-5aeb6da6865bff84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
