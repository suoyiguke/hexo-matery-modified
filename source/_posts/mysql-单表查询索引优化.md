---
title: mysql-单表查询索引优化.md
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
title: mysql-单表查询索引优化.md
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
1、数据准备
~~~
/*
Navicat MySQL Data Transfer

Source Server         : CentOS6.7--Clone
Source Server Version : 50554
Source Host           : 192.168.1.179:3306
Source Database       : db01

Target Server Type    : MYSQL
Target Server Version : 50554
File Encoding         : 65001

Date: 2017-12-15 14:58:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `article`
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `author_id` int(10) unsigned NOT NULL,
  `category` int(10) unsigned NOT NULL,
  `views` int(10) unsigned NOT NULL,
  `comments` int(10) unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of article
-- ----------------------------
INSERT INTO `article` VALUES ('1', '1', '1', '1', '1', '1', '1');
INSERT INTO `article` VALUES ('2', '2', '2', '2', '2', '2', '2');
INSERT INTO `article` VALUES ('3', '1', '1', '3', '3', '3', '3');

~~~

2、编写sql，查看sql执行计划
查询 category_id 为 1 且 comments 大于 1 的情况下，views 最多的 article_id。
~~~
EXPLAIN SELECT id,author_id from article where category = 1 and comments > 1 ORDER BY views DESC limit 0,1;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5b0dba1b0c951eaf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 很显然，type 是 ALL，即最坏的情况。Extra 里还出现了 Using filesort，也是最坏的情况。优化是必须的。
- 那么最简单的解决方案就是加索引了。好，我们来试一试。查询的条件里即 where 之后共使用了 category，comments，views 三个字段。那么来一个联合索引是最简单的了。

3、添加联合索引
~~~
ALTER TABLE `article` ADD INDEX x ( `category` , `comments`, `views` );
~~~

4、 查看索引情况
~~~
SHOW INDEX FROM article
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2c600f5bc44550b3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5、再次查看执行计划
~~~
EXPLAIN SELECT id,author_id from article where category = 1 and comments > 1 ORDER BY views DESC limit 0,1;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-38deac1c0f5bb349.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- type 变成了 range，这是可以忍受的。但是 extra 里使用 Using filesort 仍是无法接受的。
- 但是我们已经建立了索引，为啥没用呢？这是因为按照 BTree 索引的工作原理，先排序 category，如果遇到相同的 category 则再排序 comments，如果遇到相同的 comments 则再排序 views。`当 comments 字段在联合索引里处于中间位置时，因为 comments > 1 条件是一个范围值（所谓 range），MySQL 无法利用索引再对后面的 views 部分进行检索，即 range 类型查询字段后面的索引无效。`

6、删除索引，重新建立更合适的索引方案那么我们需要抛弃 comments，删除旧索引 
~~~
DROP INDEX x ON article;
~~~
然后建立新索引：
在这次的索引建立上，我们舍弃掉comments 字段，因为comments >1是范围条件
~~~
ALTER TABLE `article` ADD INDEX y ( `category` , `views` ) ;
~~~
接着再次查询新建立的y索引：
~~~
SHOW INDEX FROM article
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-de4894bc68375e57.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

7、再次查看执行计划
~~~
EXPLAIN SELECT id,author_id from article where category = 1 and comments > 1 ORDER BY views DESC limit 0,1;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-21e3591cc8cd5294.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
