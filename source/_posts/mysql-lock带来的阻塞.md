---
title: mysql-lock带来的阻塞.md
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
title: mysql-lock带来的阻塞.md
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
因为不同锁之间的兼容性关系,在有些时刻一个事务中的锁需要等待另一个事务中的锁释放它所占用的资源,这就是阻塞。

阻塞并不是一件坏事,其是为了确保事务可以 并发且正常地运行。
在 InnoDB存储引擎中,参数 innodb_lock_wait_timeout 用来控制等待的时间(默认 是50秒),
~~~
mysql> SHOW VARIABLES LIKE '%innodb_lock_wait_timeout%';
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| innodb_lock_wait_timeout | 50    |
+--------------------------+-------+
1 row in set (0.02 sec)

~~~

innodb_rollback_on_timeout 用来设定是否在等待超时时对进行中的事务进行回滚操作(默认是OFF,代表不回滚)
~~~
mysql> SHOW VARIABLES LIKE '%innodb_rollback_on_timeout%';
+----------------------------+-------+
| Variable_name              | Value |
+----------------------------+-------+
| innodb_rollback_on_timeout | OFF   |
+----------------------------+-------+
1 row in set (0.02 sec)

~~~

参数 innodb_lock_wait_timeout 是动态的,可以在 MySQL数据库运行时进行调整: 
~~~
mysql> SET @@innodb lock wait timeout=60; 
Query OK, 0 rows affected (0 .00 sec)
~~~
而 innodb rollback on timeout是静态的,不可在启动时进行修改,如: 
~~~
mysql> SETinnodb_ rollback_on_ timeout=on ERROR 1238 (HY000): Variable 'innodb_rollback_on_timeout'is a read only variable 
~~~
当发生超时, MySQL数据库会抛出一个1205的错误,如: 
~~~
mysql> BEGIN; Query OK, rows affected(0.00sec) 
mysql> SELECT FROM t WHERE a FORUPDATE; ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction 
~~~

需要牢记的是,在默认情况下InnoDB存储引擎不会回滚超时引发的错误异常。其实 InnoDB存储引擎在大部分情况下都不会对异常进行回滚。如在一个会话中执行了如下语句：

客户端A先执行
~~~
mysql> set @@autocommit = 0;
Query OK, 0 rows affected (0.00 sec)

mysql> select * from t where a >2 for update;
+---+
| a |
+---+
| 5 |
+---+
1 row in set (0.02 sec)

~~~
客户端B后执行
~~~
mysql> set @@autocommit = 0;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO `iam`.`t`(`a`) VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO `iam`.`t`(`a`) VALUES (3);
1205 - Lock wait timeout exceeded; try restarting transaction
mysql> select * from t;
+---+
| a |
+---+
| 1 |
| 2 |
| 5 |
+---+
3 rows in set (0.03 sec)

mysql> 
~~~

可以看到，客户端B之前插入的 1 值在lock wait timeout 1205报错之后仍然存在。这时会话B中的事务虽然抛出了异常,但是既没有进行 COMMIT操 作,也没有进行 ROLLBACK。而这是十分危险的状态,因此用户必须判断是否需要 COMMIT还是 ROLLBACK,之后再进行下一步的操作。

相对于死锁的 1213错误，innodb会选择一个事务正常提交，其它的事务全部回滚！
