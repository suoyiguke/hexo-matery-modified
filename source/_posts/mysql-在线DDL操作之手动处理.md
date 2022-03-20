---
title: mysql-在线DDL操作之手动处理.md
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
title: mysql-在线DDL操作之手动处理.md
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
###手动将表存为旧表，新创建一个新表来接收数据`原子性修改，不阻塞业务`
>一种不会出现业务抖动的方式
~~~
 DROP TABLE IF EXISTS my_summary_new, my_summary_old;
 CREATE TABLE my_summary_new LIKE my_summary; 
 RENAME TABLE my_summary TO my_summary_old, my_summary_new TO my_summary;
~~~
###手动修改字段数据类型`阻塞业务`


####案例1，将book表的book_name字段字符长度30改为40

表结构如下
~~~
CREATE TABLE `test`.`book`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `book_name` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 187018 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
~~~

具体操作步骤如下


1、创建临时表作为修改之后的表

create table book_tmp like book; 然后再基础上修改，或者直接创建
~~~
CREATE TABLE `test`.`book_tmp`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `book_name` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 187018 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
~~~
2、给原表加上读锁，保证之后不会再对原表有任何的数据修改

flush table WITH  read lock; （这个操作会给所有表加读锁！）
![image.png](https://upload-images.jianshu.io/upload_images/13965490-927ecefa2826ced5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、将book表的frm文件用book_tmp表的frm文件覆盖
注意以防万一，现备份好原来的frm文件！
4、 刷新表结构，之后修改就生效了

FLUSH tables;

5、最后别忘了解锁
unlock tables; 


####案例2，将book表的book_name字段的数据类型从char改为tinytext


依葫芦画瓢，替换frm和fluash表后直接让mysql宕机了！因此种方法对于修改列数据类型是无效的！

####案例3，将char修改为varchar
可以，但是修改后的值会出现多余类似空格的字符！


>这种方式局限性很大，最好不要使用。会出现一些意想不到的问题。推荐使用工具pt-online-schema-change 来完成在线DDL。
