---
title: mysql-字符集和字符校对规则-（1）.md
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
title: mysql-字符集和字符校对规则-（1）.md
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
> 天地有正气，杂然赋流形

###字符集和字符集较对规则
字符集 character： 定义mysql存储字符串的方式
较对规则 collation：定义mysql比较字符串的方式
> 字符集和较对规则是1对多的关系；我们可以使用 `	SHOW COLLATION LIKE 'utf8mb4%'` 来得到具体字符集对应的所有较对规则。

我们来看常用的utf8mb4字符集对应的所有较对规则
~~~
utf8mb4_general_ci	utf8mb4	45	Yes	Yes	1
utf8mb4_bin	utf8mb4	46		Yes	1
utf8mb4_unicode_ci	utf8mb4	224		Yes	8
utf8mb4_icelandic_ci	utf8mb4	225		Yes	8
utf8mb4_latvian_ci	utf8mb4	226		Yes	8
utf8mb4_romanian_ci	utf8mb4	227		Yes	8
utf8mb4_slovenian_ci	utf8mb4	228		Yes	8
utf8mb4_polish_ci	utf8mb4	229		Yes	8
utf8mb4_estonian_ci	utf8mb4	230		Yes	8
utf8mb4_spanish_ci	utf8mb4	231		Yes	8
utf8mb4_swedish_ci	utf8mb4	232		Yes	8
utf8mb4_turkish_ci	utf8mb4	233		Yes	8
utf8mb4_czech_ci	utf8mb4	234		Yes	8
utf8mb4_danish_ci	utf8mb4	235		Yes	8
utf8mb4_lithuanian_ci	utf8mb4	236		Yes	8
utf8mb4_slovak_ci	utf8mb4	237		Yes	8
utf8mb4_spanish2_ci	utf8mb4	238		Yes	8
utf8mb4_roman_ci	utf8mb4	239		Yes	8
utf8mb4_persian_ci	utf8mb4	240		Yes	8
utf8mb4_esperanto_ci	utf8mb4	241		Yes	8
utf8mb4_hungarian_ci	utf8mb4	242		Yes	8
utf8mb4_sinhala_ci	utf8mb4	243		Yes	8
utf8mb4_german2_ci	utf8mb4	244		Yes	8
utf8mb4_croatian_ci	utf8mb4	245		Yes	8
utf8mb4_unicode_520_ci	utf8mb4	246		Yes	8
utf8mb4_vietnamese_ci	utf8mb4	247		Yes	8
~~~

> 其中，`utf8mb4_general_ci`是utf8mb4的默认较对规则；而`utf8mb4_unicode_ci` 是基于标准的Unicode来排序和比较，能够在各种语言之间精确排序；大多数情况下我们不需要使用到这种根据具体语言的精确排序，所以推荐使用默认的utf8mb4_general_ci，因为它在比较和排序的时候更快。
 
######较对规则命名约定：
_ci 大小写不敏感
_cs 大小写敏感
_bin 二元比较时是基于字符编码的值而与language无关

######我们应该如何对较对规则进行选择？
从两个方面入手：

1、需要什么样的排序方式。是按语言（a，b，c）字母排序，还是按字符编码排序；

我们来看utf8mb4_bin和utf8mb4_general_ci在排序上的区别：
创建一个表，并导入一些数据
~~~
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for testcode
-- ----------------------------
DROP TABLE IF EXISTS `testcode`;
CREATE TABLE `testcode`  (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of testcode
-- ----------------------------
INSERT INTO `testcode` VALUES (1, 'd');
INSERT INTO `testcode` VALUES (2, 'b');
INSERT INTO `testcode` VALUES (3, 'a');
INSERT INTO `testcode` VALUES (4, 'c');
INSERT INTO `testcode` VALUES (5, '`');

SET FOREIGN_KEY_CHECKS = 1;

~~~
现在使用 `SELECT * FROM testcode ORDER BY name` 对name进行排序查询；可以看到\`符号在最后。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7fcc743b02b0f0ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
将name字段的比较规则修改为 `utf8mb4_bin` ;再次进行查询：

可以看到这次\`符号在第一位，处在a之前；
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aafbf8c2007584d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

原因很简单， `utf8mb4_bin` 是按字符编码进行排序的。而\`符号的ASCII码的十进制值为96，a为97；刚好在a的前面
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fbb658fbfed89f4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、是否区分大小写
我们在上面实验的基础上将小写b改为大写的B，此时的较对规则是默认的 utf8mb4_general_ci ；显然，这里的B就被看做为b了。即大小写不敏感
![image.png](https://upload-images.jianshu.io/upload_images/13965490-797d8a9b704516da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后将较对规则改为 utf8mb4_bin。再看看情况，这时B出现在第一行了。因为B的ASCII码是66，而b是98
![image.png](https://upload-images.jianshu.io/upload_images/13965490-de1defeb3b5da07c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###mysql中如何设置字符集和较对规则？

mysql的可以设置 服务器、库、表、列 级别的字符集和较对规则;
>但是要注意，虽说有这么几个设置字符集的地方。其实最终落脚点还是在`列级别`之上。像其它三个设置的地方只是提供了一种`若没有指定，则继承之的功能`;列继承表，表继承库，库继承服务器；只要我们显式的指定列的字符集和较对方式即可，这样就不用去管其它三个地方了。

还有一个额外的需要注意设置字符集和较对规则的地方：
`连接字符集和较对规则`

######服务器级别

查看当前的服务器级别的字符集和字符较对规则
~~~
SHOW VARIABLES LIKE 'character_set_server'
SHOW VARIABLES LIKE 'collation_server'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4512d5a246330c95.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在配置文件中指定服务器级别的字符编码和较对规则，当然不指定较对规则就使用字符集的默认较对规则
~~~
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
~~~
######库级别
查询当前库的字符集和较对规则
~~~
SHOW VARIABLES LIKE 'character_set_database'
SHOW VARIABLES LIKE 'collation_database'
~~~
######表级别
使用show create table 查看
~~~
mysql> show create table testcode;
+----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table    | Create Table                                                                                                                                                                                                         |
+----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| testcode | CREATE TABLE `testcode` (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.03 sec)
~~~

######字段级别

~~~
ALTER TABLE `test`.`testcode` 
MODIFY COLUMN `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL AFTER `id`;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-02fa92a99e995e76.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######连接字符集和较对规则
客户端在连接mysql服务时，必须将字符集统一：
character_set_client（客户端）、character_set_connection（连接）、character_set_results（返回结果） 三者必须统一

我们可以在配置文件中添加：
~~~
[mysqld]
init_connect='SET NAMES utf8mb4'
~~~
