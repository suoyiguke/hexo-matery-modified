---
title: mysql-事务的ACID四大特性和四大事务隔离级别.md
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
title: mysql-事务的ACID四大特性和四大事务隔离级别.md
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
> 苹果越分享越少，知识越分享越多

###事务的ACID四大特性
1、 原子性（Atomicity）：事务作为一个整体被执行，包含在事务中的对数据库的操作要么全部被执行，要么全部都不执行

事务作为一个整体被执行，包含在事务中的对数据库的操作要么全部被执行，要么全部都不执行。 比如，InnoDB支持事务，在InnoDB事务内如果执行了一条插入多个值的INSERT语句“INSERT INTO t VALUES('b1'),('b2'), ('b3'),('b4'),('b5'),('b6');”只要其中一个值插入失败，那么整个事务就失败了。而对于MyISAM引擎的表，它不支持事务，那么在出 错之前的值是可以被正常插入到表中的。



2、一致性（Consistency）：事务应确保数据库的状态从一个一致状态转变为另一个一致状态。一致状态的含义是数据库中的数据应满足约束

3、 隔离性（Isolation）：多个事务并发执行时，一个事务的执行不应影响其他事务的执行。
可重复读比读已提交的级别更满足隔离性，因为在“读已提交”中同一事务两次读可能结果不通，受其它事务的提交影响

4、持久性（Durability）：已被提交的事务对数据库的修改应该被永久保存在数据库中。


###四种事务隔离级别
1、Read uncommitted 读未提交
《高性能mysql》中对 Read uncommitted 级别的描述
![image.png](https://upload-images.jianshu.io/upload_images/13965490-68da30f389fd637c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 简称 RU 级别
- 在该级别事务中的对数据的修改，即使没有提交，对其他事务也是可见的
- 在该级别下会出现 脏读、不可重复度、幻读、更新丢失的事务并发问题
- 将当前会话设置成  Read uncommitted 级别
~~~
set session transaction isolation level read uncommitted;
~~~



2、Read committed 读已提交
《高性能mysql》中对 Read committed 级别的描述
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d0da3a16ae1a1874.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 简称 RC 级别
- 该级别解决了脏读的问题。但是事务中会读到其他事务已提交的数据，无法保证`读一致性`，会造成不可重复读的问题。
- 在该级别下会出现 不可重复读、幻读、更新丢失 的事务并发问题
- 将当前会话设置成  Read committed
~~~
set session transaction isolation level read committed;
~~~


3、Repeatable read [rɪˈpiːtəbl]  可重复读
《高性能mysql》中对 Repeatable read 级别的描述
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fbf60963aad8b31b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 简称 RR 级别
- RR 是 mysql的默认隔离级别
- 该隔离级别下mysql的 innodb引擎 使用 `MVCC机制`保证了事务中的`快照读一致性`。不能完全杜绝幻读，还是会出现一个幻读的情况。当我们是用insert`（当前读）` 时会出现幻读
- 该级别下会出现 幻读、更新丢失 的事务并发问题；
- 将当前会话设置成  Repeatable Read
~~~
 set session transaction isolation level repeatable read;
~~~

关于mysql中的mvcc机制，我的这篇文章有讲https://www.jianshu.com/p/5f841f3fc288

4、Serializable 串行化
《高性能mysql》中对 Serializable 级别的描述
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7f598eaefcf8d19c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 强制事务`串行执行`、对表的任何操作都会上锁，可能导致大量超时和锁竞争
- 在该隔离级别下不会出现所有的事务并发问题
- 将当前会话设置成  Serializable
~~~
set session transaction isolation level serializable ;
~~~


##事务隔离级别和事务并发问题的关系
|  事务隔离级别   | 事务并发问题  |
|  ----  | ----  |
| Read uncommitted | 脏读、幻读、不可重复读、更新丢失 |
| Read committed | 脏读、幻读、更新丢失 |
| Repeatable read | 幻读、更新丢失 |
| Read committed | 无 |
关于事务并发问题，我这篇文章有讲
https://www.jianshu.com/p/dcd0be7573ac

##命令
- 设置全局的隔离级别，最好重启服务应用更改
~~~
set global transaction isolation level read committed; //全局的
~~~
- 查询全局和当前会话的事务隔离级别
~~~
SELECT @@global.tx_isolation, @@tx_isolation;
~~~
