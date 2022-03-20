---
title: mysql-字段压缩和表压缩还有其它的.md
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
title: mysql-字段压缩和表压缩还有其它的.md
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
压缩的实质就是降低网络带宽的占用和磁盘存储空间的占用，或者由于主机上存在大数据量的sql操作，而导致主从同步延迟时也可使用压缩，看看能不能缓解延迟。

代价就是要用一定的cpu资源来交换。如果数据库机器的CPU负载已经很高或者网络带宽够用且磁盘空间也充足，就不太建议再开压缩了


mysql可以在 连接、字段、表三个维度上进行压缩
###使用压缩协议连接


mysql压缩协议适合的场景是mysql的服务器端和客户端之间传输的数据量很大，或者可用带宽不高的情况，典型的场景有如下两个：
a、查询大量的数据，带宽不够（比如导出数据的时候）

~~~
##普通连接
mysql  -hlocalhost -P666 -uroot -p123456 --compress
## 导出数据时
mysqldump -hlocalhost -P666 -uroot -p123456 -default-character-set=utf8  --compress --single-transaction test test > test.sql
~~~
b、复制的时候binlog量太大导致主从同步延迟。可以看到，开启slave_compressed_protocol=ON 后，带宽会得到了很大的压缩（节省了2/3的带宽），在跨机房同步的时候，可以避免专线的过高占用。




###压缩目标列
写入的时候调用COMPRESS函数对那个列的内容进行压缩，然后存放到对应的列。读取的时候，使用UNCOMPRESSED函数对压缩的内容进行解压缩。适用针对mysql中某个列或者某几个列数据量特别大，一般都是varchar、text、char等数据类型。

mysql的压缩函数COMPRESS压缩一个字符串，然后返回一个二进制串。使用该函数需要mysql服务端支持压缩，否则会返回NULL，压缩字段最好采用varbinary或者blob字段类型保存。使用UNCOMPRESSED函数对压缩过的数据进行解压。注意，采用这种方式需要在业务侧做少量改造。压缩后的内容存储方式如下：a、空字符串就以空字符串存储 b、非空字符串存储方式为前4个bype保存未压缩的字符串，紧接着保存压缩的字符串

压缩
SELECT COMPRESS(REPEAT('a',1000))
 解压
select UNCOMPRESS( COMPRESS(REPEAT('a',1000))) 
查询压缩情况，判断压缩效率
SELECT UNCOMPRESSED_LENGTH( COMPRESS(REPEAT('a',1000)))  '原字符串长度', LENGTH( COMPRESS(REPEAT('a',1000)))  '压缩后字符长度', UNCOMPRESS( COMPRESS(REPEAT('a',1000))), COMPRESS(REPEAT('a',1000))



测试下，创建表如下。其中signed_data和timestamp两个字段需要进行压缩
~~~
CREATE TABLE `test`.`test`  (
  `id` bigint(0) NOT NULL,
  `base64_source_data` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `source_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cert_id` varchar(36) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `signed_data` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `timestamp` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

~~~
执行insert
~~~
INSERT INTO `test`(`id`, `base64_source_data`, `source_data`, `cert_id`, `signed_data`, `timestamp`) VALUES (222, 'dnZ2dg==', 'vvvv','16a20401-cb8d-411f-82f1-890c819200b1',  COMPRESS('MIIBiQYKKoEcz1UGAQQCAqCCAXkwggF1AgEDMQwwCgYIKoEcz1UBgxEwFAYKKoEcz1UGAQQCAaAGBAR2dnZ2MYIBSjCCAUYCAQEwcTBiMQswCQYDVQQGEwJDTjEkMCIGA1UECgwbTkVUQ0EgQ2VydGlmaWNhdGUgQXV0aG9yaXR5MS0wKwYDVQQDDCRORVRDQSBTTTIgVEVTVDAxIGFuZCBFdmFsdWF0aW9uIENBMDECCxD1fwFc4urjNhs9MAoGCCqBHM9VAYMRoGowGQYJKoZIhvcNAQkDMQwGCiqBHM9VBgEEAgEwHAYJKoZIhvcNAQkFMQ8XDTIwMTIyNTA4MDMyMlowLwYJKoZIhvcNAQkEMSIEIMldsBXsFf91Z/Wy7ykrKrUutsd/RtiGOn0MAGqO6QhdMA0GCSqBHM9VAYItAQUABEcwRQIhAIiFZZhN9JoFO2n9+0mLU2jPEuUlkdgTgMLw1PsCCodNAiB1qWesqwUkp2DIMETnelEHQq4aC1w4itBkyUJdBOmb3g=='), COMPRESS('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'));
~~~

进行查询

SELECT UNCOMPRESSED_LENGTH(timestamp) '原字符串长度', LENGTH(timestamp) '压缩后字符串长度',UNCOMPRESS(timestamp)'压缩后大小' from test;
| 原字符串长度 | 压缩后字符串长度 | 压缩后大小                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
|         5120      |             3334           |  MIIO+gYJKoZIhvcNAQcCoIIO6zCCDucCAQMxD...

压缩率0.65，比较高了。针对text、char、varchr、blob等，如果里面重复的数据越多压缩效果就越好。


###创建压缩表
创建表时指定ROW_FORMAT=COMPRESSED 
~~~
CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint DEFAULT NULL,
  `book_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `zz` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `gg` varchar(255) DEFAULT NULL,
  `mj` enum('one','two','three','4') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=762475 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED 
~~~
