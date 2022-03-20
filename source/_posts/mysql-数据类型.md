---
title: mysql-数据类型.md
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
title: mysql-数据类型.md
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



3、int(4) unsigned zerofill 填充0

alter table  change column a a int(4) unsigned zerofill; 


 int(4)的4代表显示宽度为4；
unsigned 无符号；
zerofill 填充0,只是一种显示属性而不是存储属性；重来没有用到过。
那么存储1就将显示为 0001；


4、auto_increment

查询上一层自增值 select last_insert_id();
auto_increment的数据类型一定使用bigint（8字节）而不是int（4字节，21亿很容易达到）；

自增值回溯的问题：4这个记录删除了，那么以后永远不会再出现4这条记录。但是数据库重启后4这条记录又会重新出现！

5.7的auto_increment属性并不是持久化的， 他是通过查询z表的最大id再+1得到的，mysql每次重启都会去查询一次最大自增值然后加1，这样的结果会被直接当作自增的最大值：
~~~
select max(auto_increment column) + 1 from z
~~~
到现在为止5.7版本的`自增值回溯的问题`是解决不了的，只有在8.0才能解决。8.0实现了自增值持久化。


mysql5.7的演示如下：
~~~
(root@localhost) [test]>create table t(id bigint(11) auto_increment primary key );
Query OK, 0 rows affected (0.01 sec)

(root@localhost) [test]>insert into t values(null);
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>insert into t values(null);
Query OK, 1 row affected (0.01 sec)

(root@localhost) [test]>insert into t values(null);
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>select * from t;
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.00 sec)

(root@localhost) [test]>delete from t where id =3;
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>shutdown
    -> ;
Query OK, 0 rows affected (0.00 sec)
~~~
重启mysql后，再次执行自增的insert。id=3这条记录再次出现！
~~~
(root@localhost) [test]>select * from t;
+----+
| id |
+----+
|  1 |
|  2 |
+----+
2 rows in set (0.00 sec)

(root@localhost) [test]>insert into t values(null);
Query OK, 1 row affected (0.01 sec)

(root@localhost) [test]>select * from t;
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
+----+
3 rows in set (0.00 sec)

(root@localhost) [test]>

~~~



###INT类型总结
1、推荐不要使用UNSIGNED 无符号；范围本质上没有大的改变，数据范围虽然是*2但是却可以看成一个级别的，UNSIGNED 可能会有溢出现象发生。
2、自增INT类型主键建议使用BIGINT。

###数字类型
1、请一定使用DECIMAL，高精度，准确性没有任何的问题。
2、FLOAT和DOUBLE的M*G/G不一定等于M；如果进行数据汇总(sum求和)那肯定有问题的。
3、DECIMAL(M,D)中  显示M位的整数，D表示小数点后面的位数。

介绍一些函数
1、select floor(1.5); 向下取整，输出1; select floor(-1.5);输出-2；
2、select FLOOR(i+RAND()*(j-i)); 取i到j之间的随机值；如select FLOOR(1+RAND()*(100-1)); 
3、select repeat('a',3); 重复a字母3次；
   填充varchar(127)变长字段，就是这样做：select repeat('a',floor(1+rand()*127)); 


###字符类型
![image.png](https://upload-images.jianshu.io/upload_images/13965490-67b1e5eb1f9679ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、char(n)、varchar(n) 的n表示字符，其它都是字节。
2、mysql中用的最多的还是varchar
3、select length('我'); 输出占用字节数。select char_length('我');输出占用字符。

4、表默认字符集设置
默认是latin1，我们要改为utf8mb4
~~~
[mysqld]
character_set_server=utf8mb4
~~~
重启后mysql建立的每张表默认的字符集都是uf8mb4了。
~~~
(root@localhost) [test]>create table zz ( a int(11) );
Query OK, 0 rows affected (0.01 sec)

(root@localhost) [test]>show create table zz;
+-------+----------------------------------------------------------------------------------------+
| Table | Create Table                                                                           |
+-------+----------------------------------------------------------------------------------------+
| zz    | CREATE TABLE `zz` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 |
+-------+----------------------------------------------------------------------------------------+
1 row in set (0.02 sec)
~~~

>字段、表、库字符集都设置为utf8mb4就行，设置为latin1省空间的思想没什么必要。


5、修改表、列的字符集为utf8mb4

使用
~~~
alter table  t charset =utf8mb4;
~~~
修改的只是table的字符集，而之前已经创建的列的字符集还是旧的。想要修改旧字段的类型，请使用这个，注意这个语句的代价非常昂贵，会锁表。
~~~
alter table t convert to character set utf8mb4;
~~~
>从gbk  convert 到utf8mb4是可以的，但是反过来从utf8mb4到gbk  就会有问题。utf8mb4范围要比gbk大。

6、show charset;查看mysql支持的字符集，utf8mb4  Maxlen =4，代表utf8mb4下最大的字符占用4个字节。
~~~
(root@localhost) [test]>show charset;
+----------+---------------------------------+---------------------+--------+
| Charset  | Description                     | Default collation   | Maxlen |
+----------+---------------------------------+---------------------+--------+
| big5     | Big5 Traditional Chinese        | big5_chinese_ci     |      2 |
| dec8     | DEC West European               | dec8_swedish_ci     |      1 |
| cp850    | DOS West European               | cp850_general_ci    |      1 |
| hp8      | HP West European                | hp8_english_ci      |      1 |
| koi8r    | KOI8-R Relcom Russian           | koi8r_general_ci    |      1 |
| latin1   | cp1252 West European            | latin1_swedish_ci   |      1 |
| latin2   | ISO 8859-2 Central European     | latin2_general_ci   |      1 |
| swe7     | 7bit Swedish                    | swe7_swedish_ci     |      1 |
| ascii    | US ASCII                        | ascii_general_ci    |      1 |
| ujis     | EUC-JP Japanese                 | ujis_japanese_ci    |      3 |
| sjis     | Shift-JIS Japanese              | sjis_japanese_ci    |      2 |
| hebrew   | ISO 8859-8 Hebrew               | hebrew_general_ci   |      1 |
| tis620   | TIS620 Thai                     | tis620_thai_ci      |      1 |
| euckr    | EUC-KR Korean                   | euckr_korean_ci     |      2 |
| koi8u    | KOI8-U Ukrainian                | koi8u_general_ci    |      1 |
| gb2312   | GB2312 Simplified Chinese       | gb2312_chinese_ci   |      2 |
| greek    | ISO 8859-7 Greek                | greek_general_ci    |      1 |
| cp1250   | Windows Central European        | cp1250_general_ci   |      1 |
| gbk      | GBK Simplified Chinese          | gbk_chinese_ci      |      2 |
| latin5   | ISO 8859-9 Turkish              | latin5_turkish_ci   |      1 |
| armscii8 | ARMSCII-8 Armenian              | armscii8_general_ci |      1 |
| utf8     | UTF-8 Unicode                   | utf8_general_ci     |      3 |
| ucs2     | UCS-2 Unicode                   | ucs2_general_ci     |      2 |
| cp866    | DOS Russian                     | cp866_general_ci    |      1 |
| keybcs2  | DOS Kamenicky Czech-Slovak      | keybcs2_general_ci  |      1 |
| macce    | Mac Central European            | macce_general_ci    |      1 |
| macroman | Mac West European               | macroman_general_ci |      1 |
| cp852    | DOS Central European            | cp852_general_ci    |      1 |
| latin7   | ISO 8859-13 Baltic              | latin7_general_ci   |      1 |
| utf8mb4  | UTF-8 Unicode                   | utf8mb4_general_ci  |      4 |
| cp1251   | Windows Cyrillic                | cp1251_general_ci   |      1 |
| utf16    | UTF-16 Unicode                  | utf16_general_ci    |      4 |
| utf16le  | UTF-16LE Unicode                | utf16le_general_ci  |      4 |
| cp1256   | Windows Arabic                  | cp1256_general_ci   |      1 |
| cp1257   | Windows Baltic                  | cp1257_general_ci   |      1 |
| utf32    | UTF-32 Unicode                  | utf32_general_ci    |      4 |
| binary   | Binary pseudo charset           | binary              |      1 |
| geostd8  | GEOSTD8 Georgian                | geostd8_general_ci  |      1 |
| cp932    | SJIS for Windows Japanese       | cp932_japanese_ci   |      2 |
| eucjpms  | UJIS for Windows Japanese       | eucjpms_japanese_ci |      3 |
| gb18030  | China National Standard GB18030 | gb18030_chinese_ci  |      4 |
+----------+---------------------------------+---------------------+--------+
41 rows in set (0.00 sec)
~~~

7、select hex('我');  将字符串转为16进制的值。可以看到直接使用16进制insert也是可以的。

~~~
(root@localhost) [test]>select hex('我');
+------------+
| hex('我')  |
+------------+
| E68891     |
+------------+
1 row in set (0.00 sec)

(root@localhost) [test]>select 0xE68891;
+----------+
| 0xE68891 |
+----------+
| 我       |
+----------+
1 row in set (0.00 sec)

(root@localhost) [test]>insert into zz values (1,0xE68891);
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>select * from zz;
+------+-------+
| a    | cloum |
+------+-------+
|    1 | 我    |
+------+-------+
1 row in set (0.01 sec)
~~~

8、select cast(123 as char(10)); 类型转换函数

我想知道'我'在gbk、utf8、utf8mb4 下占用字节分别是多少。
~~~
(root@localhost) [test]>select length(cast('我' as char(1) charset gbk ));
+---------------------------------------------+
| length(cast('我' as char(1) charset gbk ))  |
+---------------------------------------------+
|                                           2 |
+---------------------------------------------+
1 row in set (0.00 sec)

(root@localhost) [test]>select length(cast('我' as char(1) charset utf8 ));
+----------------------------------------------+
| length(cast('我' as char(1) charset utf8 ))  |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.00 sec)

(root@localhost) [test]>select length(cast('我' as char(1) charset utf8mb4 ));
+-------------------------------------------------+
| length(cast('我' as char(1) charset utf8mb4 ))  |
+-------------------------------------------------+
|                                               3 |
+-------------------------------------------------+

~~~

9、collation 排序规则

情景模式：用户名不区分大小写。
collation  默认的utf8mb4_general_ci   也是不区分大小写的。
~~~
(root@localhost) [test]>select 'yinkai'='YinKai';
+-------------------+
| 'yinkai'='YinKai' |
+-------------------+
|                 1 |
+-------------------+
1 row in set (0.00 sec)
~~~
>密码也不区分大小写

如果你需要区分大小写的话，collation 设置为utf8mb4_bin
~~~
create table t (a varchar(10) collate utf8mb4_bin ,unique key(a));
~~~

10、select md5('12345678');
md5的基础上再加盐会比较安全。

select md5(concat('aaa','baidu'));


11、varchar和varbinary的区别

- varchar有字符集的概念，varbinary没有字符集的概念，它存的是16进制数据；
- varchar的N是字符数，varbinary的N是字节数；

utf8mb4下 varchar 插入gbk的'我'的十六进制：CED2报错：`Incorrect string value`。表明在utf8mb4下找不到CED2对应的字符。utf8mb4下的'我'对应的十六进制为E68891，这样插入才能成功。
~~~
(root@localhost) [dbt3]>use test;
Database changed
(root@localhost) [test]>show create table zz;
+-------+------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                           |
+-------+------------------------------------------------------------------------------------------------------------------------+
| zz    | CREATE TABLE `zz` (
  `a` int(11) DEFAULT NULL,
  `cloum` char(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 |
+-------+------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

(root@localhost) [test]>insert into zz values(2,'我');
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>select hex(cast('我' as char(1) charset gbk ));
+------------------------------------------+
| hex(cast('我' as char(1) charset gbk ))  |
+------------------------------------------+
| CED2                                     |
+------------------------------------------+
1 row in set (0.00 sec)

(root@localhost) [test]>insert into zz values(2,0xCED2);
ERROR 1366 (HY000): Incorrect string value: '\xCE\xD2' for column 'cloum' at row 1
(root@localhost) [test]>select hex(cast('我' as char(1) charset UTF8MB4 ));
+----------------------------------------------+
| hex(cast('我' as char(1) charset UTF8MB4 ))  |
+----------------------------------------------+
| E68891                                       |
+----------------------------------------------+
1 row in set (0.00 sec)

(root@localhost) [test]>insert into zz values(2,0xE68891);
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>select * from zz;
+------+-------+
| a    | cloum |
+------+-------+
|    1 | 我    |
|    2 | 我    |
|    2 | 我    |
+------+-------+
3 rows in set (0.00 sec)
~~~
当然，若是varbinary可以直接插入：
~~~

(root@localhost) [test]>create table zzz(a varbinary(8));
Query OK, 0 rows affected (0.01 sec)

(root@localhost) [test]>insert zzz values(0xE68891);
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>insert zzz values(0xCED2);
Query OK, 1 row affected (0.01 sec)

(root@localhost) [test]>select * from zzz;
+------+
| a    |
+------+
| 我   |
| ϒ     |
+------+
~~~

12、select concat_ws('.','a','b','c');
使用自定义字符连接字符串

13、右填充 select rpad('aaa',8,'.'); 
左填充 select lpad('aaa',8,'.'); 

###字符串类型 -  ENUM & SET

- 字符串类型--集合类型
- ENUM 类型最多允许65536个值
- SET 类型最多允许65个值
- 通过sql_mode 参数可以用于约束检查

###日期时间类型

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1a8b28eb627ab93d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- DATE、YEAR、TIME 用的比较少
- DATETIME和TIMESTAMP存储完整日期时间比较多

- 有人使用int存时间，有人使用TIMESTAMP存时间。
- 用int类型也许会块那么一点点。但是实在没必要啦。每次查询都要转换一下。
- TIMESTAMP到了2038年就用不了了，优点是跨时区的。
- TIMESTAMP的值会根据时区来调整。如 set time_zone='+0:00'; 这样now()的TIMESTAMP就会慢8小时。

~~~
(root@localhost) [test]>insert t1 values(now(),now());
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>set time_zone='+0:00';
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [test]>select * from t1;
+---------------------+---------------------+
| a                   | b                   |
+---------------------+---------------------+
| 2021-05-30 00:29:41 | 2021-05-29 16:29:41 |
+---------------------+---------------------+
1 row in set (0.00 sec)


~~~
###日期函数
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5142ce9e7eb5e2a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、带上毫秒
~~~
(root@localhost) [test]>select now(6);
+----------------------------+
| now(6)                     |
+----------------------------+
| 2021-05-30 00:22:56.987966 |
+----------------------------+
1 row in set (0.00 sec)
~~~



2、now() 和sysdate()的区别
 - now 执行sql的时间
- sysdate 执行函数的时间
~~~
(root@localhost) [test]>select now(),sysdate(),sleep(3),now(),sysdate();
+---------------------+---------------------+----------+---------------------+---------------------+
| now()               | sysdate()           | sleep(3) | now()               | sysdate()           |
+---------------------+---------------------+----------+---------------------+---------------------+
| 2021-05-30 00:25:45 | 2021-05-30 00:25:45 |        0 | 2021-05-30 00:25:45 | 2021-05-30 00:25:48 |
+---------------------+---------------------+----------+---------------------+---------------------+
1 row in set (3.00 sec)

~~~

3、注意使用data_format在等号左边时会导致索引失效。当然我们可以使用5.7虚拟列/8.0函数索引解决。
所以建议在等号右边进行format操作
![image.png](https://upload-images.jianshu.io/upload_images/13965490-06e84cb46478c23d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###大对象
图片、视频只存地址就行了。
因为一个页能存更多的记录数那么性能就越好。

这种大对象都有当都的服务来做 S3


###JSON类型
5.7支持，5.6不支持JSON，但是可以使用BLOB。
有些字段是不确定的，如淘宝的商品有那么多的属性。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-41e21183c63350ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- BLOB没有对JSON进行规范
- BLOB没有JSON相应函数，JSON可以直接通过一些函数直接得到具体某个title下的数据
- 结合5.7的函数索引，提升JSON查询性能


~~~
(root@localhost) [test]>create table c (a json);
Query OK, 0 rows affected (0.01 sec)

(root@localhost) [test]>insert into c values('{"name":"yinkai","age":24}');
Query OK, 1 row affected (0.05 sec)

(root@localhost) [test]>select * from c;
+-------------------------------+
| a                             |
+-------------------------------+
| {"age": 24, "name": "yinkai"} |
+-------------------------------+
1 row in set (0.00 sec)

(root@localhost) [test]>select a->"$.name" from c;
+-------------+
| a->"$.name" |
+-------------+
| "yinkai"    |
+-------------+
1 row in set (0.00 sec)

(root@localhost) [test]>select a->>"$.name" from c;
+--------------+
| a->>"$.name" |
+--------------+
| yinkai       |
+--------------+
1 row in set (0.00 sec)

(root@localhost) [test]>

~~~

~~~
(root@localhost) [test]>insert into c values('{"name":"yinkai","age":24,"ch":{"a":"A"}}');
Query OK, 1 row affected (0.00 sec)

(root@localhost) [test]>select a->>"$.ch.a" from c;
+--------------+
| a->>"$.ch.a" |
+--------------+
| NULL         |
| A            |
+--------------+
2 rows in set (0.00 sec)
~~~

###NULL类型
所有字段都应该是NOT NULL，不允许NULL的存在（姜老师推荐）

- NULL 在其它统计的时候会影响统计结果
- NULL 会导致索引失效

~~~
(root@localhost) [test]>select 1=NULL;
+--------+
| 1=NULL |
+--------+
|   NULL |
+--------+
1 row in set (0.00 sec)

(root@localhost) [test]>select NULL is NULL;
+--------------+
| NULL is NULL |
+--------------+
|            1 |
+--------------+
1 row in set (0.10 sec)

~~~




