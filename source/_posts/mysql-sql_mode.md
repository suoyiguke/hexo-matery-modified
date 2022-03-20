---
title: mysql-sql_mode.md
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
title: mysql-sql_mode.md
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
> 下则为河岳，上则为日星
###查询当前sql_mode

~~~
SELECT @@sql_mode
~~~


###几种sql_mode模式介绍

sql_mode模式是具体的几种 sql_mode值的集合，我们可以直接指定这个来方便达到使用多种sql_mode值的目的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7900f4bd6b13f04a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######ANSI模式

宽松模式，对插入数据进行校验，如果不符合定义类型或长度，对数据类型调整或截断保存，报warning警告。
~~~
SET SESSION sql_mode = 'ANSI';
SET GLOBAL sql_mode = 'ANSI';
~~~
######TRADITIONAL模式

严格模式，当向mysql数据库插入数据时，进行数据的严格校验，保证错误数据不能插入，报error错误。用于事物时，会进行事物的回滚。
~~~
SET SESSION sql_mode = 'TRADITIONAL';
SET GLOBAL sql_mode = 'TRADITIONAL';
~~~

######STRICT_TRANS_TABLES模式

严格模式，进行数据的严格校验，错误数据不能插入，报error错误。
~~~
SET SESSION sql_mode = 'STRICT_TRANS_TABLES';
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES';
~~~


######ORACLE模式
~~~
SET SESSION sql_mode = 'ORACLE';
SET GLOBAL sql_mode = 'ORACLE';
~~~
 PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,ORACLE,NO_KEY_OPTIONS,NO_TABLE_OPTIONS,NO_FIELD_OPTIONS,NO_AUTO_CREATE_USER


######MSSQL模式（sql server）
~~~
SET SESSION sql_mode = 'MSSQL';
SET GLOBAL sql_mode = 'MSSQL';
~~~
PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,MSSQL,NO_KEY_OPTIONS,NO_TABLE_OPTIONS,NO_FIELD_OPTIONS
###具体sql mode的值

######ANSI
1、REAL_AS_FLOAT
将real视为float的同义词。默认情况下，mysql将real视为double的同义词。

2、PIPES_AS_CONCAT
将`||` 符号视为字符串连接操作符 

3、ANSI_QUOTES
将`"`视为标识符引用字符(如`""`引用字符),而不是字符串引用字符。启用此模式后，您仍然可以使用`来引用标识符。启用ansi_quotes后，不能使用双引号来引用文字字符串，因为它们被解释为标识符。

>举个例子：若没有指定ansi_quotes，则可以这样 SELECT "11" ,这里将双引号内容被认为是字符串，查询会成功执行；若指定了ansi_quotes，则该查询报错。因为此时内容被认为是 字段名（类似于``）





4、IGNORE_SPACE
允许函数名和(字符)之间有空格。这导致内置函数名被视为保留字

5、ONLY_FULL_GROUP_BY 
对于GROUP BY聚合操作，如果在SELECT中的列，没有在GROUP BY中出现，那么将认为这个SQL是不合法的，因为列不在GROUP BY从句中



######TRADITIONAL
1、STRICT_TRANS_TABLES
为事务引擎启用严格的sql模式，并尽量为非事务引擎启用

2、STRICT_ALL_TABLES
为所有的存储引擎启用严格的sql模式

3、NO_ZERO_IN_DATE
在严格模式，不接受月或日部分为0的日期。如果使用IGNORE选项，我们为类似的日期插入'0000-00-00'。在非严格模式，可以接受该日期，但会生成警告。

4、NO_ZERO_DATE
在严格模式，不要将 '0000-00-00'做为合法日期。你仍然可以用IGNORE选项插入零日期。在非严格模式，可以接受该日期，但会生成警告

5、ERROR_FOR_DIVISION_BY_ZERO
在严格模式，在INSERT或UPDATE过程中，如果被零除(或MOD(X，0))，则产生错误(否则为警告)。如果未给出该模式，被零除时MySQL返回NULL。如果用到INSERT IGNORE或UPDATE IGNORE中，MySQL生成被零除警告，但操作结果为NULL。

6、NO_AUTO_CREATE_USER
防止GRANT自动创建新用户，除非还指定了密码。

7、NO_ENGINE_SUBSTITUTION
如果需要的存储引擎被禁用或未编译，那么抛出错误。不设置此值时，用默认的存储引擎替代，并抛出一个异常。


######其它的

1、PAD_CHAR_TO_FULL_LENGTH
默认情况下，检索时从char列值中删除尾随空格。如果启用了pad_char_to_full_length，则不会发生调整，检索到的char值会被填充到其全长。此模式不适用于varchar列，检索时会为这些列保留尾随空格。

2、NO_KEY_OPTIONS

不要在show create表的输出中打印mysql特定的索引选项
3、NO_TABLE_OPTIONS
不要在show create table的输出中打印mysql特定的表选项(如`engine`)，由此获得更加通用的脚本

4、NO_FIELD_OPTIONS
不要在show create表的输出中打印mysql特定的列选项

###sql_mode在数据迁移中的应用
如果mysql 与其它异构数据库之间有数据迁移的需求时，那么mysql中提供的数据库组合模式则会对数据迁移过程会有所帮助。对导出数据更容易导入目标。

1、 通过设置sql mode, 可以完成不同严格程度的数据校验，有效地保障数据准备性。
2、 通过设置sql model 为ansi 模式，来保证大多数sql符合标准的sql语法，这样应用在不同数据库之间进行迁移时，则不需要对业务sql 进行较大的修改。
3、 在不同数据库之间进行数据迁移之前，通过设置SQL Mode 可以使MySQL 上的数据更方便地迁移到目标数据库中。

~~~
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';
~~~

###修改配置的方式
~~~
[mysqld]
sql_mode=STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION
~~~


** 问题**
1、Err] 3065 - Expression #1 of ORDER BY clause is not in SELECT list, references column 'iam.biz_patient_sign_pdf.id' which is not in SELECT list; this is incompatible with DISTINCT 
因为order by的字段不在select里出现
~~~
set global sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
~~~

###版本

5.5的sql mode 为空
5.6的sql mode 比较宽松

5.7的sql mode 比较严格

在一个全新的业务中强烈建议将sql mode配置为非常严格的模式。让一些
非法值不能插入。
但是要注意老业务千万不要再动这个值。



 


