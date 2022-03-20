---
title: mysql-参数调优之-innodb_lock_wait_timeout和lock_wait_timeout的区别.md
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
title: mysql-参数调优之-innodb_lock_wait_timeout和lock_wait_timeout的区别.md
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
**innodb_lock_wait_timeout**
The length of time in seconds an InnoDB transaction waits for a row lock before giving up.
innodb的dml操作的行级锁的等待时间，默认50秒

**lock_wait_timeout**
This variable specifies the timeout in seconds for attempts to acquire `metadata locks`.
说到lock_wait_timeout我们就不得不提到 metadata locks， 我们称之为`元数据锁`。 实质上就是进行修改字段数据类型、字符集等线上DDL时容易阻塞对该表的其它DML操作，lock_wait_timeout 这个参数的默认时间是8760 小时非常长，如果生产环境出现metadata locks无疑是灾难性的，会严重影响正常的业务操作。所以我们需要将之设为50秒或者更短。
~~~
SET GLOBAL lock_wait_timeout = 50
SET SESSION lock_wait_timeout = 50
~~~
如果线上已经出现了metadata locks，那么我们应该如何紧急处理下？为了业务能正常运作，不要继续让它阻塞下去了，杀死引发阻塞的事务线程。
~~~
SHOW PROCESSLIST
kill 线程id 
~~~

当然，为了避免出现metadata locks`，这需要我们研发人员了解DDL和DML的并发关系。
https://www.jianshu.com/p/e7da2e579dfa
我i们还需学习使用一些代价较低的修改表结构的方法。
