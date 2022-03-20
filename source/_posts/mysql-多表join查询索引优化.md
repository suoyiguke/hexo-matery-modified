---
title: mysql-多表join查询索引优化.md
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
title: mysql-多表join查询索引优化.md
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
## 数据准备
~~~
CREATE TABLE IF NOT EXISTS `class` (
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
`card` int(10) unsigned NOT NULL,
PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `book` (
`bookid` int(10) unsigned NOT NULL AUTO_INCREMENT,
`card` int(10) unsigned NOT NULL,
PRIMARY KEY (`bookid`)
);

insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into class(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));
insert into book(card) values(floor(1+(RAND()*20)));

~~~
##两表关联
### 左连接优化
1、一个左连接查询
~~~
explain select * from class left join book on class.card = book.card;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-069f73edc46f65d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
两个select的type都是ALL

2、在右表book表的card字段上建立索引
~~~
ALTER TABLE `book` ADD INDEX y ( `card`);
~~~

3、查看索引情况
~~~
SHOW INDEX FROM book
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-331538d7349eeaae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、再次查看执行计划
~~~
explain select * from class left join book on class.card = book.card;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0a6526cdad213b43.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

往左连接的右表上加索引效果非常理想！

5、删除旧索引，在class表上加上新索引。

~~~
DROP INDEX y ON book;
ALTER TABLE `class` ADD INDEX x ( `card`);
~~~

查询索引情况
~~~
SHOW INDEX FROM book
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c0fc0df003fb6f0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6、再次查看执行计划
~~~
explain select * from class left join book on class.card = book.card;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5e0284d094f1a460.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在left join的左表class添加索引，效果并不理想！

###右连接优化

1、接着上面的操作，class表里添加了索引。
~~~
SHOW INDEX FROM class
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-11026d1226665151.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看执行计划
~~~
explain select * from class right join book on class.card = book.card;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4f3ca363c4c029cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、将class表和table表调换位置，再次查看执行计划

~~~
explain select * from book right join class on class.card = book.card;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-21c709c207315623.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


##三表关联
1、在上面的表结构和基础上，继续创建一个phone表
~~~
CREATE TABLE IF NOT EXISTS `phone` (
`phoneid` int(10) unsigned NOT NULL AUTO_INCREMENT,
`card` int(10) unsigned NOT NULL,
PRIMARY KEY (`phoneid`)
) engine = innodb;
~~~
2、book、phone 两表添加索引
~~~
ALTER TABLE `book` ADD INDEX y ( `card`);
ALTER TABLE `phone` ADD INDEX z ( `card`);
~~~
3、查看执行计划

~~~
 explain select * from class left join book on class.card=book.card left j
oin phone on book.card = phone.card;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-da96b6e156ebf13d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 后 2 行的 type 都是 ref 且总 rows 优化很好，效果不错。因此索引最好设置在需要经常查询的字段中
- join的优化：
1、小表驱动大表；left join的小表放到左边；因此这里使用class驱动book再是phone ；
2、尽可能减少join语句中的NestedLoop的循环总次数；
3、优先优化NestedLoop的内层循环；
4、保证join语句中`“被驱动表”`上join条件字段已经被索引（key字段非NULL）；
5、当无法保证`“被驱动表”`的join条件字段被索引且内存资源充足的前提下，不要太吝惜JoinBuffer的设置；修改my.conf文件

##结论
 - 多表join添加索引原则：左连接加右表，右连接加左表
 - 不要添加多余的索引

![image.png](https://upload-images.jianshu.io/upload_images/13965490-06369014bec97c82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
