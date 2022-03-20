---
title: mysql-innodb引擎文件.md
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
title: mysql-innodb引擎文件.md
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
###文件
我在test_innodb库类创建了一张test1表，那么打开库对应的文件夹下可以发发现 


![image.png](https://upload-images.jianshu.io/upload_images/13965490-a2a84def272d2a20.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######xxx.frm 文件
1、frm文件是一种表结构定义文件。无论采用何种存储引擎，mysql都有一个以frm为后缀名的文件，这个文件记录了该表的表结构定义。

2、frm还用来存放视图的定义，如用户定义了一个视图，则该frm文件就是一个普通文本文件，可以使用文本编辑器查看；如下，定义一个test_st视图
~~~
CREATE ALGORITHM = UNDEFINED DEFINER = `root`@`%` SQL SECURITY DEFINER VIEW `test_innodb`.`test_st` AS select `test1`.`id` AS `id`,`test1`.`name` AS `name` from `test1`;
~~~

然后到库目录下查看
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c5f6a1d169cccd90.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用motepad++可以查看如下：
>TYPE=VIEW
query=select `test_innodb`.`test1`.`id` AS `id`,`test_innodb`.`test1`.`name` AS `name` from `test_innodb`.`test1`
md5=b97409fe07e6783c6a470df7a92c566e
updatable=1
algorithm=0
definer_user=root
definer_host=%
suid=2
with_check_option=0
timestamp=2020-04-24 07:26:34
create-version=1
source=SELECT\n	* \nFROM\n	test1
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_general_ci
view_body_utf8=select `test_innodb`.`test1`.`id` AS `id`,`test_innodb`.`test1`.`name` AS `name` from `test_innodb`.`test1`



######xxx.ibd 文件

1、innodb表中保存数据和索引的文件，如果数据有100万行。那么ibd文件也会非常的大。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f35b79db6c5a78cd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们可以通过sql来得到具体的表数据和索引大小
~~~
SELECT
    a.table_schema ,
    a.table_name ,
    concat(round(sum(DATA_LENGTH / 1024 / 1024) + sum(INDEX_LENGTH / 1024 / 1024) ,2) ,'MB') total_size ,
    concat(round(sum(DATA_LENGTH / 1024 / 1024) , 2) ,'MB') AS data_size ,
    concat(round(sum(INDEX_LENGTH / 1024 / 1024) , 2) ,'MB') AS index_size
FROM
    information_schema. TABLES a
WHERE
    a.table_schema = 'test'
AND a.table_name = 'tb_box';
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-03ca2246b7d6e820.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 从ibd 文件可以得出，mysql表数据越是存储到该文件的。数据越多则ibd文件越大！ 因此为了查询性能，分表其实就是分割ibd文件。


2、表分区生成的分区文件也是 ibd格式
![image.png](https://upload-images.jianshu.io/upload_images/13965490-34a89bb6a48b761e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、ibd文件在数据库频繁进行增加删除后会产生碎片，这些碎片是可以手动优化的，是一种空间浪费
xxx

######ibdata文件
ibdata文件也是存放innodb数据的文件，之所以用两种文件来存放innodb的数据，是因为innodb的数据存储方式能够通过配置来决定是使用共享表空间存放存储数据，还是用独享表空间存放存储数据。

>独享表空间存储方式使用.ibd文件，并且每个表一个ibd文件
共享表空间存储方式使用.ibdata文件，所有表共同使用一个ibdata文件
