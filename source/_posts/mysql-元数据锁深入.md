---
title: mysql-元数据锁深入.md
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
title: mysql-元数据锁深入.md
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

我们可以通过执行这个

UPDATE performance_schema.setup_consumers SET ENABLED = 'YES' WHERE NAME ='global_instrumentation';
UPDATE performance_schema.setup_instruments SET ENABLED = 'YES' WHERE NAME ='wait/lock/metadata/sql/mdl';

之后就能查询到元数据锁相关信息了
~~~
mysql> select * from performance_schema.metadata_locks;
+-------------+--------------------+----------------+-----------------------+---------------------+---------------+-------------+-------------------+-----------------+----------------+
| OBJECT_TYPE | OBJECT_SCHEMA      | OBJECT_NAME    | OBJECT_INSTANCE_BEGIN | LOCK_TYPE           | LOCK_DURATION | LOCK_STATUS | SOURCE            | OWNER_THREAD_ID | OWNER_EVENT_ID |
+-------------+--------------------+----------------+-----------------------+---------------------+---------------+-------------+-------------------+-----------------+----------------+
| TABLE       | test               | test           |         1389034001616 | SHARED_READ         | TRANSACTION   | GRANTED     | sql_parse.cc:5978 |             278 |             62 |
| GLOBAL      | NULL               | NULL           |         1389053299776 | INTENTION_EXCLUSIVE | STATEMENT     | GRANTED     | sql_base.cc:5495  |             290 |              4 |
| SCHEMA      | test               | NULL           |         1389053298624 | INTENTION_EXCLUSIVE | TRANSACTION   | GRANTED     | sql_base.cc:5480  |             290 |              4 |
| TABLE       | test               | test           |         1389053298048 | EXCLUSIVE           | TRANSACTION   | PENDING     | sql_parse.cc:5978 |             290 |              4 |
| TABLE       | test               | test           |         1389053298240 | SHARED_READ         | TRANSACTION   | PENDING     | sql_parse.cc:5978 |             280 |             26 |
| TABLE       | performance_schema | metadata_locks |         1389038576880 | SHARED_READ         | TRANSACTION   | GRANTED     | sql_parse.cc:5978 |             291 |              4 |
+-------------+--------------------+----------------+-----------------------+---------------------+---------------+-------------+-------------------+-----------------+----------------+
6 rows in set (0.02 sec)
~~~
 SHARED_READ    共享读 S
 INTENTION_EXCLUSIVE 意向排他 IX
 EXCLUSIVE   排他X
