---
title: url字段上的索引设计和查询.md
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
title: url字段上的索引设计和查询.md
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
###方案1，使用哈希索引+触发器/虚拟列/函数索引实现优化

###5.6
~~~
SELECT
	id 
FROM
	url 
WHERE
	url = "http://wrw.mysq1.com" 
	AND ur1_crc = CRC32( "http://ww.mysql.com" );
~~~
这样做的性能会非常高，因为MySQL优化器会使用这个选择性很高而体积很小的基于url_crc列的索引来完成查找（在上面的案例中，索引值为1560514994)。即使有多个记录有相同的索引值，查找仍然很快，只需要根据哈希值做快速的整数比较就能找到索引条目，然后一一比较返回对应的行。另外一种方式就是对完整的URL字符串做索引，那样会非常慢。
这样实现的缺陷是需要维护哈希值。可以手动维护，也可以使用触发器实现。下面的案例演示了触发器如何在插入和更新时维护url_crc列。首先创建如下表:
~~~
CREATE TABLE pseudohash(
id int unsigned NOT NULL auto_increment,url varchar(255)NOT NULL,
url_crc int unsigned NOT NULL DEFAULT o,PRIMARY KEY(id)
);
~~~
然后创建触发器。先临时修改一下语句分隔符，这样就可以在触发器定义中使用分号:
~~~
DELIMITER //
CREATE TRIGGER pseudohash_crc_ins BEFORE INSERT ON pseudohash FOR EACH ROW BEGINSET NEW.url_crc=crc32(NEW.ur1);
END;
l/
CREATE TRIGGER pseudohash_crc_upd BEFORE UPDATE ON pseudohash FOR EACH ROW BEGINSET NEw.url_crc=crc32(NEW.url);
END;
//
DELIMITER ;
~~~



###hash函数选用
如果采用这种方式，记住不要使用SHA1()和MD5()作为哈希函数。因为这两个函数计算出来的哈希值是非常长的字符串，会浪费大量空间，比较时也会更慢。SHA1()和MD5()是强加密函数，设计目标是最大限度消除冲突，但这里并不需要这样高的要求。简单哈希函数的冲突在一个可以接受的范围，同时又能够提供更好的性能。

如果数据表非常大，CRC32()会出现大量的哈希冲突，则可以考虑自己实现一个简单的64位哈希函数。这个自定义函数要返回整数，而不是字符串。一个简单的办法可以使用MD5()函数返回值的一部分来作为自定义哈希函数。这可能比自己写一个哈希算法的性能要差（参考第7章)，不过这样实现最简单:
~~~
-- 19
SELECT
	LENGTH( CONV ( RIGHT ( MD5 ( 'https://www.souhu.com' ), 16 ), 16, 10 ) );
-- 10
SELECT
	LENGTH( crc32( 'https://www.souhu.com' ) )
~~~
处理哈希冲突。当使用哈希索引进行查询的时候，必须在WHERE子句中包含常量值:
~~~
- mysq1> SELECT id_ FROM url WHERE url_crc=CRC32("http:/ /wnwn .mysq1.com")
->AND ur1="http://we .mysql.com";
~~~
一旦出现哈希冲突，另一个字符串的哈希值也恰好是1560514994，则下面的查询是无法正确工作的。
~~~
mysql> SELECT id FROM url NHERE url_crc=CRC32("http://warns.mysq1.com");
~~~

因为所谓的“生日悖论”生5，出现哈希冲突的概率的增长速度可能比想象的要快得多。CRC32()返回的是32位的整数，当索引有93 000条记录时出现冲突的概率是1%。例如我们将/usr/share/dict/words中的词导入数据表并进行CRC32()计算,最后会有98 569行。这就已经出现一次哈希冲突了，冲突让下面的查询返回了多条记录:
 SELECT word,crc FROM words wHERE crc = CRC32( 'gnu"); 返回多条数据


正确的写法应该如下: SELECT word,crc FRON words MHERE crc = CRC32( ' gnu ')AND word = "gnu'

要避免冲突问题，必须在WHERE条件中带入哈希值和对应列值。如果不是想查询具体值，例如只是统计记录数（不精确的)，则可以不带入列值，直接使用CRC32()的哈希值查询即可。还可以使用如FNV64()函数作为哈希函数，这是移植自Percona Server的函数，可以以插件的方式在任何MySQL版本中使用，哈希值为64位，速度快，且冲突比CRC32()要少很多。





###5.7
5.7已经有虚拟列的特性。已经不用再使用触发器实现了。
直接定义默认值为crc32(`url`)的虚拟列就行
~~~
CREATE TABLE `url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(255) NOT NULL,
  `ur1_crc` bigint(20) unsigned GENERATED ALWAYS AS (conv(right(md5(`url`),16),16,10)) VIRTUAL NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hash_url` (`ur1_crc`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8

insert into url (`name`,url)  values('yinxuan','https://www.souhu.com')

EXPLAIN SELECT
	* 
FROM
	url 
WHERE
	url = 'https://www.souhu.com' 
	AND ur1_crc = CONV ( RIGHT ( MD5 ( 'https://www.souhu.com' ), 16 ), 16, 10 )

~~~

###8.0
8.0直接引入了函数索引的特性，我们连虚拟列都不用建立了。

~~~
CREATE TABLE `url` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hash_url` ((conv(right(md5(`url`),16),16,10)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8

insert into url (`name`,url)  values('yinxuan','https://www.souhu.com')


EXPLAIN SELECT
	* 
FROM
	url 
WHERE
	CONV ( RIGHT ( MD5 ( url ), 16 ), 16, 10 ) = CONV ( RIGHT ( MD5 ( 'https://www.souhu.com' ), 16 ), 16, 10 ) 
	AND url = 'https://www.souhu.com'
~~~

###方案2
将url字符串倒转存入。这样结合前缀索引的特性。区分度一下子提高很多
