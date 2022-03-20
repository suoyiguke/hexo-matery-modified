---
title: mysql-索引长度、区分度和前缀索引.md
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
title: mysql-索引长度、区分度和前缀索引.md
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
###好的索引
1、查询频繁 2、 区分度高 3、长度小 4、尽量能覆盖常用查询字段
###

###索引长度的重要性
索引长度直接影响索引文件的大小，影响增删改的速度，并间接影响查询速度（占用内存多）

针对列的值，从左往右截取部分来来建立索引。即是使用`前缀索引`
①、截的越短，重复读越高，区分度就越小，索引效果并不好
②、截的越长，重复读越低，区分度越高。索引效果越好，但是需要更多的空间存储索引文件。增删改变慢。

所以我们需要在 区分度+长度 两者行取得一个平衡。我们可以截取不同的长度，并测试其区分度。

###使用前缀索引
1、语法：index(field(10))，使用字段值的前10个字符建立索引，默认是使用字段的全部内容建立索引。
前提：前缀的标识度高。比如密码就适合建立前缀索引，因为密码几乎各不相同。
`实操的难度`：在于前缀截取的长度。

2、在navicat中创建前缀索引
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5d27d854fa013943.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###区分度计算

>我们可以利用selectcount(distinct left(password,prefixLen))/count(*); 通过从调整prefixLen的值（从1自增）查看不同前缀长度的一个平均匹配度，接近1时就可以了（表示一个密码的前prefixLen个字符几乎能确定唯一一条记录）


下面对前缀索引进行下实践，建立一张表syfg。里面的password字段添加了一个  `INDEX idx_password(password(10)) USING BTREE` 索引
~~~
CREATE TABLE `test`.`syfg`  (
  `id` int(11) NOT NULL,
  `a` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `b` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `c` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `d` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `password` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_password`(`password`(10)) USING BTREE COMMENT '密码前缀索引'
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

INSERT INTO `test`.`syfg`(`id`, `a`, `b`, `c`, `d`, `passwrod`) VALUES (1, 'a', 'b', 'c', 'd', '202cb962ac59075b964b07152d234b70');
INSERT INTO `test`.`syfg`(`id`, `a`, `b`, `c`, `d`, `passwrod`) VALUES (2, 'a1', 'b1', 'c1', 'd1', 'caf1a3dfb505ffed0d024130f58c5cfa');

~~~

执行下列语句，数值越接近于1就越好。根据这个值调整前缀索引长度。
~~~
select count(distinct left(password,10))/count(*) FROM syfg
~~~

需要经过反复修改截取位数。进行反复的测试，直到这个区分度接近1。这样前缀索引的性能才是最好的时候。


###关于前缀索引的特定情况优化设计
比如存储url的列，他们的前7个8个字符总是相同的。若对其设置前缀索引需要截取更大的空间才能保证一定的区分度。这样建立的索引效率非常低。
https://www.bilibili.com
https://www.baidu.com

1、所以我们可以将之倒过来存储并建立前缀索引，这样区分度会比较轻易提高
mysql中的字符串反转使用REVERSE()函数
~~~
SELECT REVERSE('https://www.baidu.com')
~~~
2、或者可以使用crc32()函数将url构造为一个伪hash列，转成整型。降低索引的长度，从而提高查询效率。
具体使用可以看看这个 https://www.jianshu.com/p/93d91f5192a0

###前缀索引缺陷

前缀索引是一种能使索引更小、更快的有效办法，但另一方面也有其缺点:MySQL无法使用前缀索引做ORDER BY和GROUP BY，也无法使用前缀索引做覆盖扫描。

###场景

一个常见的场景是针对很长的十六进制唯一ID使用前缀索引。在前面的章节中已经讨

论了很多有效的技术来存储这类ID信息，但如果使用的是打包过的解决方案，因而无法修改存储结构，那该怎么办?例如使用vBulletin或者其他基于MySQL的应用在存储网站的会话（SESSION）时，需要在一个很长的十六进制字符串上创建索引。此时如果采用长度为8的前缀索引通常能显著地提升性能，并且这种方法对上层应用完全透明。

###后缀索引(suffix index）
有时候也有用途（例如，找到某个域名的所有电子邮件地址)。MySQL原生并不支持反向索引，但是可以把字符串反转后存储，并基于此建立前缀索引。可以通过触发器来维护这种索引。
