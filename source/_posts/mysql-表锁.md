---
title: mysql-表锁.md
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
title: mysql-表锁.md
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

表锁：偏向于MyISAM存储引擎，开销小，加锁快；无死锁，锁定粒度大，发生冲突概率高。并发度小。  

###使用
- 锁表命令：
~~~
lock table tablename read,tablename2 write;  
~~~
- 解锁命令：
~~~
unlock tables;  
~~~
- 查看锁：
~~~
show open tables；
~~~

 MyISAM在执行查询语句（SELECT）前，会自动给涉及的所有表加读锁，在执行增删改操作之前，会自动给涉及的表加写锁。  MySQL的表级锁有两种模式：  
- 表共享读锁（Table Read Lock）  
- 表独占写锁(Table Write Lock)    

结合上表，所以对MyISAM表进行操作，会有一下情况：  
1、对MyISAM表的读操作（加读锁），不会阻塞其他进程对同一个表的读请求，但会阻塞对同一个表的写请求，只有当读锁释放后，才会执行其他进程的写操作 
 2、对MyISAM表的写操作（加写锁），会阻塞其他进程对同一表的读和写操作，只有当写锁释放后，才会执行其他进程的读写操作  


###加上表锁之后，关闭了客户端。怎么才能解锁？
解决方案：
1.查询所有进程
show full processlist ;

2.关闭锁死进行，kill + id
 KILL 168;


###试验
1、准备数据
~~~
create table mylock(
id int not null primary key auto_increment,
name varchar(20)
)engine myisam;

insert into mylock(name) values('a');
insert into mylock(name) values('b');
insert into mylock(name) values('c');
insert into mylock(name) values('d');
insert into mylock(name) values('e');
~~~
2、表级读锁实验；先开启sessionA，后开启sessionB
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8fb4b7c2bd1daca6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

读锁：自己可读、写报错；别的session也可读，写阻塞


3、查看表锁情况
~~~
 show open tables;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f14c4330a8b275ca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、解锁
![image.png](https://upload-images.jianshu.io/upload_images/13965490-62127fae9c005628.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5、表级读锁实验；
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c00a19cc21fc1500.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
写锁：自己可读可写。别的session 读写全阻塞


###如何分析表锁定
使用这个命令
~~~
show STATUS like 'table%'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cb980eb2013e330d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- Table_locks_immediate：产生表锁的次数
- Table_locks_waited 出现表锁等待的次数，此值高说明存在较高的表锁竞争
