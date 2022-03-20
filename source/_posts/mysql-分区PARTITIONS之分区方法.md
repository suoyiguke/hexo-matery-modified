---
title: mysql-分区PARTITIONS之分区方法.md
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
title: mysql-分区PARTITIONS之分区方法.md
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
> `分区依据的字段必须是主键/唯一索引的组成部分`，分区是为了快速定位数据，因此该字段的搜索频次较高应作为强检索字段，否则依照该字段分区毫无意义。

联合分区键作为分区键只能保证在分区内唯一，不能实现全局唯一；
dbt3.orders。
如何实现全全局唯一？


mysql为我们提供的分区方法有下列几种
一、range、list 
二、hash、key
三、columns

######RANGE 分区：

按照数据大小范围分区（将数据使用某种条件，分散到不同的分区中）。如下，按文章的发布时间将数据按照2018年8月、9月、10月分区存放：

~~~
create table article_range(
	id int auto_increment,
	title varchar(64),
	content text,
	created_time int,	-- 发布时间到1970-1-1的毫秒数
	PRIMARY KEY (id,created_time)	-- 要求分区依据字段必须是主键的一部分
)charset=utf8
PARTITION BY RANGE(created_time)(
	PARTITION p201808 VALUES less than (1535731199),	-- select UNIX_TIMESTAMP('2018-8-31 23:59:59')
	PARTITION p201809 VALUES less than (1538323199),	-- 2018-9-30 23:59:59
	PARTITION p201810 VALUES less than (1541001599)	-- 2018-10-31 23:59:59
);
~~~

插入和查询，可以看出来这个WHERE created_time = 1535731180的查询只是去`p201808`分区去找
~~~
insert into article_range values(null,'MySQL优化','内容示例',1535731180);
flush tables;
EXPLAIN SELECT * FROM `article_range` WHERE created_time = 1535731180
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e481ee836de92ab8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、分区字段：表示要按照哪个字段进行分区，可以是一个字段名，也可以是对某个字段进行表达式运算如year(create_time)，使用range最终的值必须是数字

2、分区名称: 要保证不同，也可以采用 p0、p1、p2 这样的分区名称，

3、less than : 表示小于
Value : 表示要小于某个具体的值，如 less than (10) 那么分区字段的值小于10的都会被分到这个分区

4、maxvalue: 表示一个最大的值

注意：range 对应的分区键值必须是数字值，可以使用range columns(分区字段) 对非int型做分区，如字符串，对于日期类型的可以使用year()、to_days()、to_seconds()等函数


######LIST 分区：

也是一种条件分区，按照列表值分区（in (值列表)）。这里是使用`状态` 字段来进行分区的。

~~~
create table article_list(
	id int auto_increment,
	title varchar(64),
	content text,
	status TINYINT(1),	-- 文章状态：0-草稿，1-完成但未发布，2-已发布
	PRIMARY KEY (id,status)	-- 要求分区依据字段必须是主键的一部分
)charset=utf8
PARTITION BY list(status)(
	PARTITION writing values in(0,1),	-- 未发布的放在一个分区	
	PARTITION published values in (2)	-- 已发布的放在一个分区
);
~~~

插入数据和查询
~~~
insert into article_list values(null,'mysql优化','内容示例',0);
flush tables;
EXPLAIN SELECT * FROM article_list WHERE status = 1
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-a018c39366e9bd3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
WHERE status = 1查询只扫描 writing分区，而不是扫描所有分区。这对性能来讲肯定是有帮助的！

######HASH分区：

相同的输入得到相同的输出。输出的结果跟输入是否具有规律无关。`仅适用于整型字段`；Hash分区的意义主要用于确保数据在预先确定数目的分区中追求`平均分配`。Hash分区会自动根据列计算需要插入的数据分布与那个分区。其使用的是hash分区键，然后根据分区的数量计算需要操作的分区。对于开发人员而言，要做的事情只是基于将要被哈希的列值指定一个表达式，以及指定被分区的表将要被分割的分区数量。具体使用如下：

~~~
CREATE TABLE shareniu_range3 ( id INT NOT NULL, NAME VARCHAR ( 50 ), age INT ) PARTITION BY HASH ( id ) PARTITIONS 3;
EXPLAIN SELECT * FROM shareniu_range3 WHERE id = 1
~~~

使用注意事项：

（1） 由于哈希分区每次更新、插入、删除一行数据，这个表达式都需要去计算一次，那就意味着非常复杂的表达式可能引擎性能的问题。尤其是在执行批量插入语句的时候。

（2） 最有效的哈希函数是只针对单个列进行计算，这个列的值最好随着列值进行增加，比如上述例子中使用的是int类型的列，这样哈希之后的数据分布的更加的均匀。因为这考虑了在分区范围内的修建，也就是说表达式值和他基于的列的值变化越接近，就更有效地使用该表达式进行哈希分区。

######线性Hash分区
线性哈希分区在partition by子句中添加`linear`关键字即可。线性哈希分区的优点在于 增加、删除、合并和拆分分区将变得更加快捷。有利于处理及其大量的数据的表，缺点在于数据可能分布的不太均匀。
~~~
CREATE TABLE shareniu_range3 ( id INT NOT NULL, NAME VARCHAR ( 50 ), age INT ) PARTITION BY LINEAR HASH ( id ) PARTITIONS 3;
EXPLAIN SELECT * FROM shareniu_range3 WHERE id = 1
~~~


######KEY分区
和hash(field)的性质一样，只不过key是`处理字符串`的，比hash()多了一步从字符串中计算出一个整型在做取模操作。
~~~
create table article_key(
	id int auto_increment,
	title varchar(64),
	content text,
	PRIMARY KEY (id,title)	-- 要求分区依据字段必须是主键的一部分
)PARTITION by KEY(title) PARTITIONS 10
~~~

######columns分区
COLUMN分区是5.5开始引入的分区功能，只有RANGE COLUMN和LIST COLUMN这两种分区；支持整形、日期、字符串；RANGE和LIST的分区方式非常的相似。


>COLUMNS和RANGE和LIST分区的区别
1、针对日期字段的分区就不需要再使用函数进行转换了，例如针对date字段进行分区不需要再使用YEAR()表达式进行转换。
2、COLUMN分区支持多个字段作为分区键但是不支持表达式作为分区键。

RANGE COLUMNS和LIST COLUMNS分区其实是RANG和LIST分区的升级，所以可以直接使用COLUMN分区。注意COLUMNS分区不支持timestamp字段类型。

>COLUMNS支持的类型
整形支持：tinyint,smallint,mediumint,int,bigint;不支持decimal和float
时间类型支持：date,datetime
字符类型支持：char,varchar,binary,varbinary;不支持text,blob


比如： 日期COLUMNS分区
~~~
CREATE TABLE members (
    id INT,
    joined DATE NOT NULL
)
PARTITION BY RANGE COLUMNS(joined) (
    PARTITION a VALUES LESS THAN ('1960-01-01'),
    PARTITION b VALUES LESS THAN ('1970-01-01'),
    PARTITION c VALUES LESS THAN ('1980-01-01'),
    PARTITION d VALUES LESS THAN ('1990-01-01'),
    PARTITION e VALUES LESS THAN MAXVALUE
);

insert into members(id,joined) values(1,'1950-01-01'),(1,'1960-01-01'),(1,'1980-01-01'),(1,'1990-01-01');

EXPLAIN SELECT * FROM members where joined = '1950-01-01'
~~~



