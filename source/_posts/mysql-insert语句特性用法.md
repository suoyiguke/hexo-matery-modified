---
title: mysql-insert语句特性用法.md
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
title: mysql-insert语句特性用法.md
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
>学如逆水行舟，不进则退

之前学习mysql的时候都是零敲碎打。这次尝试系统性学习insert语句的用法


######使用IGNORE修饰符

插入或忽略。如果使用IGNORE修饰符，则执行INSERT语句时发生的主键冲突或唯一索引冲突错误将被忽略。如果没有出现冲突，则插入到表中。注意需要在表中建立 `UNIQUE索引`或 `PRIMARY KEY` 主键，因为mysql就是通过它们的唯一特性来进行判断到底是进行插入还是忽略

![image.png](https://upload-images.jianshu.io/upload_images/13965490-479a7391735cdc42.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

具体使用：
insert `ignore` into test(a,b,c,d) values('a1','b1','c1','d1');

###### INSERT ... ON DUPLICATE KEY UPDATE 语法
插入或更新，和ignore一样 需要表中有建立`UNIQUE 索引`或`PRIMARY KEY`。通过它们的唯一特性来判断当前操作是插入还是更新。若不存在则插入，若已经存在则更新

![image.png](https://upload-images.jianshu.io/upload_images/13965490-2b1e9c4c3566ee91.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>insert into test(a,b,c,d) values('a1','b1','c1','d1') `ON DUPLICATE KEY UPDATE` a='a2',b='b2',c='c2',d='d2';


 ON DUPLICATE KEY UPDATE 插入或更新语句的 Affected rows返回值有个规律如下：
> 如果行作为新记录被插入，则受影响行的值为1；如果原有的记录被更新，则受影响行的值为2，如果更新的数据和已有的数据一模一样，则受影响的行数是0。

######insert 插入多行
~~~
INSERT INTO tbl_name (a,b,c) VALUES(1,2,3),(4,5,6),(7,8,9);
~~~

###### INSERT ... SELECT语法
 INSERT ... SELECT能够将一张表中的数据复制到另一张表中
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c7a58e8e1b138bb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
具体使用
>insert into test2(id,a,b,c,d) `select  * from test`;


