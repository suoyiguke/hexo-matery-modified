---
title: mysql-各种数据类型与数据长度关系.md
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
title: mysql-各种数据类型与数据长度关系.md
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
1、decimal

decimal(8,2) 表示总位数是8，整数位6，小数位2；隐式包含四舍五入的功能，当插入数据为999999.975时，实际数据为999999.98

~~~
DROP TABLE IF EXISTS `ip`;
CREATE TABLE `ip`  (
  `price` decimal(8, 2) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
INSERT INTO `ip` VALUES (123456.22);
SET FOREIGN_KEY_CHECKS = 1;
##############
UPDATE `test`.`ip` SET `price` = 999999.975 WHERE `price` = 123456.22 LIMIT 1;
SELECT * FROM ip limit 1
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-17d9b0f24a40a89f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、char(10)、varchar(10)

>字符长度是字符数而不是字节数

~~~
CREATE TABLE `test`.`Untitled`  (
  `str` char(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
###########

~~~

1、char是定长的，如果超过长度则update/insert执行报错 data too long
~~~
UPDATE `test`.`ip` SET `str` = 'yinkai' WHERE `str` = 'yinka' ;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c8e05dcab2621941.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、再来看看varchar(10)
