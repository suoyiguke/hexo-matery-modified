---
title: mysql-行锁之lock_data.md
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
title: mysql-行锁之lock_data.md
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
1、supremum pseudo-record
这个supremum pseudo-record我是在
~~~
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS; 
~~~
的lock_data看到的


他是怎么出现的呢？
一个事务做 `insert into box select * from tb_box ORDER BY create_time` 另一个事务做insert，id是原id的最大值加1。此时这个insert事务被阻塞。
