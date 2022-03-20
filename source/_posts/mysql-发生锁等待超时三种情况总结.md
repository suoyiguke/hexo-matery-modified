---
title: mysql-发生锁等待超时三种情况总结.md
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
title: mysql-发生锁等待超时三种情况总结.md
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
1、有事务长时间未提交
查询正在活跃的事务
~~~
SELECT * FROM information_schema.INNODB_TRX
~~~
杀死指定 trx_tread_id 即可

2、线上dml，修改表结构

Waiting for table metadata lock

3、行锁触发
需要排查sql中update语句的where条件、显式加锁的sql的where条件 是不是走索引。不然全表扫描了！
导致接下来的insert都会被阻塞！

如果在where条件中加了索引，那么只会阻塞包含 特定值的insert。
比如：check_key上加了索引，这样就只会阻塞 heck_key= 'QT1234567890'的 insert语句！其它的就不会
~~~
UPDATE BIZ_CERT_INFO SET pwd_updated_at=NOW() WHERE check_key= 'QT1234567890'
~~~

4、表锁触发
