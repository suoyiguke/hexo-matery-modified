---
title: mysql-lock和latch区别.md
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
title: mysql-lock和latch区别.md
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
这里还要区分锁中容易令人混淆的概念lock与 latch.在数据库中,lock与 latch都 可以被称为“锁”。但是两者有着截然不同的含义,本章主要关注的是lock。

latch 一般称为闩锁(轻量级的锁),因为其要求锁定的时间必须非常短。若持续的时间长,则应用的性能会非常差。在 InnoDB存储引擎中, latch又可以分为 mutex(互 斥量)和rwlock(读写锁)。其目的是用来保证并发线程操作临界资源的正确性,并且 通常没有死锁检测的机制。 
>latch就像是Java里的 lock，锁定对象也是线程。用于保证线程操作临界资源的正确性

lock的对象是事务,用来锁定的是数据库中的对象,如表、页、行。并且一般lock 的对象仅在事务commit或 rollback后进行释放(不同事务隔离级别释放的时间可能不同)。

此外,lock,正如在大多数数据库中一样,是有死锁机制的。表6-1显示了lock与 latch的不同。对于 InnoDB存储引擎中的 latch,可以通过 命令 SHOW ENGINE INNODB MUTEX来进行 查看,如图6-1所示。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-09becf825371c1e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
mysql> SHOW ENGINE INNODB MUTEX;
+--------+-----------------------------+---------+
| Type   | Name                        | Status  |
+--------+-----------------------------+---------+
| InnoDB | rwlock: log0log.cc:838      | waits=2 |
| InnoDB | sum rwlock: buf0buf.cc:1460 | waits=3 |
+--------+-----------------------------+---------+
2 rows in set (0.02 sec)
~~~

 在 Debug版本下,通过命令 SHOW ENGINE INNODB MUTEX可以看到 latch的更多信息,如 图6-2所示 

![image.png](https://upload-images.jianshu.io/upload_images/13965490-071b1cd606dcfb63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过上述的例子可以看出,列Type显示的总是,列Name显示 latch的是的信 息以及所在源码的位置(行数)。列 Status比较复杂,在 Debug模式下,除了显示 os waits, 还会显示 count、 spin waits、 spin rounds、 os yields、 os wait times等信息。其具体含义见表6-2. 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9ef5143a7cb8af49.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上述所有的这些信息都是比较底层的,一般仅供开发人员参考。但是用户还是可以 通过这些参数进行调优。 相对于 latch的查看,lock信息就显得直观多了。用户可以通过命令 SHOW ENGINE INNODB STATUS及 information schema架构下的表 INNODB TRX、 INNODB LOCKS、 INNODB LOCK WAITS来观察锁的信息。这将在下节中进行详细的介绍。
