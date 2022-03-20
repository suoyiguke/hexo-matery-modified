---
title: mysql-事务之使用savepoint部分回滚.md
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
title: mysql-事务之使用savepoint部分回滚.md
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
>  十年磨一剑

我们可以使用mysql中的savepoint保存点来实现事务的部分回滚~

基本用法如下
~~~
SAVEPOINT identifier
ROLLBACK [WORK] TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
~~~

1、使用 SAVEPOINT identifier 来创建一个名为identifier的回滚点

 2、ROLLBACK TO identifier，回滚到指定名称的SAVEPOINT，这里是identifier

3、 使用 RELEASE SAVEPOINT identifier 来释放删除保存点identifier


4、如果当前事务具有相同名称的保存点，则将删除旧的保存点并设置一个新的保存点。



5、回滚到SAVEPOINT语句返回以下错误，则表示不存在具有指定名称的保存点：

```
ERROR 1305 (42000): SAVEPOINT identifier does not exist
```

6、如果执行START TRANSACTION，COMMIT和ROLLBACK语句，则将删除当前事务的所有保存点。

###在mysql客户端实验一下

######准备数据
~~~
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mylock
-- ----------------------------
DROP TABLE IF EXISTS `mylock`;
CREATE TABLE `mylock`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mylock
-- ----------------------------
INSERT INTO `mylock` VALUES (1, 'a');
INSERT INTO `mylock` VALUES (2, 'b');
INSERT INTO `mylock` VALUES (3, 'c');
INSERT INTO `mylock` VALUES (4, 'd');

SET FOREIGN_KEY_CHECKS = 1;

~~~

进入mysql客户端操作下

######创建一个保存点，并回滚至之。看看数据情况
>mysql> set @@autocommit = 0;
Query OK, 0 rows affected (0.00 sec)
mysql> select * from mylock;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
|  4 | d    |
+----+------+
4 rows in set (0.02 sec)
mysql> INSERT INTO test.mylock(id, name) VALUES (5, 'e');
Query OK, 1 row affected (0.00 sec)
mysql> savepoint point_1; `创建保存点`
Query OK, 0 rows affected (0.00 sec)
mysql> INSERT INTO test.mylock(id, name) VALUES(6, 'f');
Query OK, 1 row affected (0.00 sec)
mysql> select * from mylock;
>+----+------+
>| id | name |
>+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
|  4 | d    |
|  5 | e    |
|  6 | f    |
+----+------+
6 rows in set (0.03 sec)
mysql> rollback to point_1;`回滚到指定保存点`
>Query OK, 0 rows affected (0.00 sec)
mysql> select * from mylock;`再次查询id=6的记录消失掉了`
+----+------+
| id | name |
>+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
|  4 | d    |
|  5 | e    |
+----+------+
5 rows in set (0.05 sec)



######一个保存点不删除则可以存在一个事务中被多次使用
![image.png](https://upload-images.jianshu.io/upload_images/13965490-55e40fc0fa760dc5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
######删除保存点示例
![image.png](https://upload-images.jianshu.io/upload_images/13965490-21c782143fc22968.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######覆盖保存点示例
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1620b1aeac338b6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######保存点失效示例
保存点因为提交事务和新开事务而失效，保存点只能使用在当前事务中
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b92cd405d9ac160e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######在spring中我们可以使用    @Transactional(propagation=Propagation.NESTED)
注解申明一个嵌套事务来使用保存点功能，达到事务的部分回滚目的
可以看看这篇文章，关于嵌套事务的https://www.jianshu.com/p/c6d4095f5833

######在jdbc里可以使用savepoint
我的这篇文章有涉及到 https://www.jianshu.com/p/db386858fde8

详细可以看看官网的使用
https://dev.mysql.com/doc/refman/5.7/en/savepoint.html





