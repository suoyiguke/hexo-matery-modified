---
title: mysql-参数调优(5)之AUTO_INCREMENT主键自增优化参数之innodb_autoinc_lock_mode.md
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
title: mysql-参数调优(5)之AUTO_INCREMENT主键自增优化参数之innodb_autoinc_lock_mode.md
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
###AUTO_INCREMENT初始值和步长相关操作
查看mysql的递增初始值和步长
~~~
SHOW VARIABLES LIKE 'auto_inc%'; 
~~~

查看表的当前递增值和步长
~~~
 SELECT auto_increment FROM information_schema.tables where table_schema='test' and table_name='id_lock';
~~~
mysql只能对mysql实例级别修改，不能对表修改
~~~
SET @@auto_increment_increment=3; -- 将自增长步长设置为3
SET @@auto_increment_offset=4; -- 将自增长开始值设置为4
~~~


###mysql中AUTO_INCREMENT的主键字段在什么时候会触发递增？
在执行insert语句之后，而不是在insert语句所在事务提交之后。这样可以提高主键生成在并发下的性能。我们可以做个实验了验证。

事务A
~~~
mysql> set @@autocommit =1;  step1
Query OK, 0 rows affected (0.00 sec) 
mysql> INSERT INTO `test`.`id_lock`(`id`) VALUES (NULL); step2
Query OK, 1 row affected (0.13 sec)
mysql> INSERT INTO `test`.`id_lock`(`id`) VALUES (NULL); step6
Query OK, 1 row affected (0.00 sec)
mysql> select * from id_lock; step7
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.03 sec)

mysql> 
~~~
事务B
~~~
mysql> set @@autocommit = 1; step3
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO `test`.`id_lock`(`id`) VALUES (NULL); step4
Query OK, 1 row affected (0.00 sec)
mysql> select * from id_lock; step5
+----+
| id |
+----+
|  2 |
+----+
1 row in set (0.03 sec)

mysql> 
~~~
可以看到，事务A和B都没有commit ，它们的自增当前值互相受影响。有点像RU读未提交的隔离级别下出现的"脏读"。然而这里允许读到已经其它事务未提交的自增当前值。这样做是为了性能考虑。所以若有些insert被回滚没有生效，就会导致记录不是连续的，中间有个别空缺不连续。

###自增主键存在的性能问题
对于高并发工作负载，在InnoDB中按主键顺序插入可能会造成明显的争用。

1、主键上界（自增的当前值）会成为”热点”，因为所有的插入都发生在这里，所以并发插入可能导致间隙锁竞争。
2、另一个热点可能是AUTO_INCREMENT锁机制：如果遇到这个问题，则可能需要考虑重新设计表或者应用，或者更改innodb_autoinc_lock_mode配置。
######AUTO-INC Locking机制
自增长在数据库中是非常常见的一种属性，也是很多DBA或开发人员首选的主键方式。在InnoDB存储引擎的内存结构中，对每个含有自增长值的表都有一个自增长计数器。当对含有自增长的计数器的表进行插入操作时，这个计数器会被初始化，执行如下的语句来得到计数器的值：
~~~
select max(auto_inc_col) from t for update;
~~~
插入操作会依据这个自增长的计数器值加1赋予自增长列。这个实现方式称为AUTO-INC Locking。这种锁其实是采用一种特殊的`表锁`机制，为了提高插入的性能，锁不是在一个事务完成后才释放，而是在完成对自增长值插入的SQL语句后立即释放。（这个结论上文已经做了验证）

虽然AUTO-INC Locking从一定程度上提高了并发插入的效率，但还是存在一些性能上的问题，优化还远远不够。
>1、首先，对于有自增长值的列的并发插入性能较差，事务必须等待前一个插入的完成，虽然不用等待事务的完成。
2、其次，对于INSERT….SELECT的大数据的插入会影响插入的性能，因为另一个事务中的插入会被阻塞。

######mutex互斥量机制
从MySQL 5.1.22版本开始，InnoDB存储引擎中提供了一种轻量级`互斥量`的自增长实现机制，这种机制大大提高了自增长值插入的性能。并且从该版本开始，InnoDB存储引擎提供了一个参数`innodb_autoinc_lock_mode`来控制自增长的模式，该参数的默认值为1。在继续讨论新的自增长实现方式之前，需要对自增长的插入进行分类。插入操作可以根据` 是否能确定得到插入行数` 分为下面四个类别：

>1、insert-like：指所有的插入语句，如INSERT、REPLACE、INSERT…SELECT，REPLACE…SELECT、LOAD DATA等。
2、simple inserts：指能在插入前就确定插入行数的语句，这些语句包括INSERT、REPLACE等。需要注意的是：simple inserts不包含INSERT…ON DUPLICATE KEY UPDATE、INSERT IGNORE这类SQL语句。
3、bulk inserts：指在插入前不能确定得到插入行数的语句，如INSERT…SELECT，REPLACE…SELECT，LOAD DATA、INSERT IGNORE。
4、mixed-mode inserts：混合的，指插入中有一部分的值是自增长的，有一部分是确定的主键值（不会触发自镇长）。如INSERT INTO t1(c1,c2) VALUES(1,’a’),(2,’a’),(null,’a’)；也可以是指INSERT…ON DUPLICATE KEY UPDATE这类SQL语句。

###innodb_autoinc_lock_mode参数
接下来分析参数innodb_autoinc_lock_mode以及各个设置下对自增长的影响，其总共有三个有效值可供设定，即0、1、2，具体说明如下：
~~~
0, traditional
1, consecutive
2, interleaved
~~~

0：这是MySQL 5.1.22版本之前自增长的实现方式，即通过表锁的AUTO-INC Locking方式，因为有了新的自增长实现方式，0这个选项不应该是新版用户的首选了。

>①、这种模式下，所有的insert语句在开始时都会获得一个表锁AUTO-INC Locking。该锁会一直持有到insert语句执行结束才会被释放。
②、对于一条insert插入多个行记录的语句，他保证了同一条语句插入的行记录的自增ID是连续的。
③、这个锁并不是事务级别的锁。在这种模式下，主从复制时，基于语句复制模式下，主和从的同一张表的同一个行记录的自增ID是一样的。这种模式下，表的并发性最低。（性能最差，但主从下不会导致id不一致）


1：这是该参数的默认值，对于”simple inserts”，该值会用互斥量（mutex）去对内存中的计数器进行累加的操作。

>①、这种模式下，insert语句在开始时会获得一个表锁AUTO-INC Locking, `simple insert在获取到需要增加的ID的量后，autoinc_lock就会被释放,不必等到语句执行结束`。
②、但对于bulk insert，自增锁会被一直持有直到语句执行结束才会被释放。
③、这种模式仍然保证了同一条语句插入的行记录的自增ID是连续的。这种模式下的主从复制表现跟traditional模式下一样，也不会导致主从id不一致，但是性能会有所提高。
④、需要注意的是，如果已经使用AUTO-INC Locing方式去产生自增长的值，而这时需要再进行”simple inserts”的操作时，还是需要等待AUTO-INC Locking的释放。

2：在这个模式下，对于所有的插入操作”INSERT-LIKE”自增长值的产生都是通过互斥量，而不是AUTO-INC Locking的方式。不管什么情况都使用轻量级互斥的锁。

>①、显然，`innodb_autoinc_lock_mode=2 是性能最高的方式`。然而，这会带来一定的问题。
②、因为并发插入的存在，在每次插入时，自增长的值可能不是连续的。
③、此外，最重要的是，基于Statement的主从复制会出现问题。因此，使用这个模式，任何时候都应该使用Row方式。这样才能保证最大的并发性能及主从数据的一致。
（innodb_autoinc_lock_mode=2 性能最好，代价是自增值可能不连续。而且会让基于Statement的主从复制出现id不一致问题，此时需使用Row的方式）

~~~
SHOW VARIABLES LIKE 'innodb_autoinc_lock_mode'
[mysqld]
innodb_autoinc_lock_mode = 2
~~~

###总结
1、innodb  row复制时，可将innodb_autoinc_lock_mode设置为2，这时可在所有insert情况下表获得最大并发度。
2、innodb statement复制时，可将innodb_autoinc_lock_mode设置为1，保证复制安全的同时，获得简单insert语句的最大并发度。
3、myisam引擎情况下，无论什么样自增id锁都是表级锁，设置innodb_autoinc_lock_mode参数无效。

4、mysql 5.7默认AUTO_INCREMENT为1，我们将之设置为2可以提高性能。当然mysql8中已经默认是2了
