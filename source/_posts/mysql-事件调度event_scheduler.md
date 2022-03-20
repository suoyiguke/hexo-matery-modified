---
title: mysql-事件调度event_scheduler.md
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
title: mysql-事件调度event_scheduler.md
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
mysql自身提供了定时调度的功能


###开启关闭
MySQL事件调度器event_scheduler负责调用事件，它默认是关闭的。这个调度器不断地监视一个事件是否要调用， 要创建事件，必须打开调度器。
查看调度器开启状态
~~~
 show variables like '%event_scheduler%'; 
~~~
开启事件调度器，通过命令行，可通过如下任何一个命令行
~~~
SET GLOBAL event_scheduler = ON; 
SET @@global.event_scheduler = ON; 
SET GLOBAL event_scheduler = 1; 
SET @@global.event_scheduler = 1;
~~~

通过配置文件my.cnf
~~~
[mysqld]
event_scheduler = 1 #或者ON 
~~~

查看调度器线程，可以看到event_scheduler是一个Daemon守护线程
~~~
 show processlist; 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0f426a2748e1d9db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###创建语法


1、schedule:时间调度，用于指定事件何时发生或者多久发生一次，分别对应下面两个字句
①AT字句：用于指定事件在某个时刻发生。其中，timestamp表示一个具体的时间点，后面可以加一个时间间隔，表示在这个时间间隔后事件发生；interval表示这个时间间隔，由一个数值和单位构成；quantity是间隔时间的数值
②EVERY字句：用于表示事件在指定时间区间每隔多长时间发生一次。其中，STARTS子句用于指定开始时间，ENDS子句用于指定结束时间

2、ON COMPLETION [NOT] PRESERVE ：表示当事件不会再发生的情况下，删除事件（注意特定时间执行的事件，如果设置了该参数，执行完毕后，事件将被删除，不想删除的话可以设置成ON COMPLETION PRESERVE）；

3、ENABLE：表示系统将执行这个事件；DISENABLE:不执行这个事件

4、指定事件启动时所要求执行的代码。如果包含多条语句，可以使用BEGIN…END复合结构


###创建事件实例
创建一张表进行测试
~~~
CREATE TABLE events_list ( event_name VARCHAR ( 20 ) NOT NULL, event_started TIMESTAMP NOT NULL );
~~~

1、立即执行的事件
~~~
create event event_now 
on schedule 
at now() 
do insert into events_list values('event_now', now()); 
~~~
2、每秒钟执行
~~~
CREATE event event_second
ON SCHEDULE 
EVERY 1 SECOND
DO insert into events_list values('event_second', now()); 
~~~
2、每分钟执行
~~~
create event test.event_minute 
on schedule 
every 1 minute  
do insert into events_list values('event_minute', now()); 
~~~


###开启和关闭事件
1、关闭事件
~~~
ALTER EVENT event_name ON COMPLETION PRESERVE DISABLE;  
~~~

2、开启事件

~~~
ALTER EVENT event_name ON  COMPLETION PRESERVE ENABLE;
~~~

###查看存在的事件
查看当前所在库的事件
~~~
SHOW EVENTS;
~~~

查看所有事件
~~~
SELECT * FROM mysql.EVENT;
~~~


>1、默认创建事件存储在当前库中，也可显示指定事件创建在哪个库中通过show events只能查看当前库中创建的事件事件执行完即释放，如立即执行事件，执行完后，事件便自动删除，多次调用事件或等待执行事件可以查看到;
2、如果两个事件需要在同一时刻调用，mysql会确定调用他们的顺序，如果要指定顺序，需要确保一个事件至少在另一个事件1秒后执行;
3、对于递归调度的事件，结束日期不能在开始日期之前。
select可以包含在一个事件中，然而他的结果消失了，就好像没执行过。
