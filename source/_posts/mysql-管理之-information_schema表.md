---
title: mysql-管理之-information_schema表.md
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
title: mysql-管理之-information_schema表.md
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
######查看information_schema表中所有的子表
SHOW TABLES FROM information_schema
~~~
CHARACTER_SETS
COLLATIONS
COLLATION_CHARACTER_SET_APPLICABILITY
COLUMNS
COLUMN_PRIVILEGES
ENGINES
EVENTS
FILES
GLOBAL_STATUS
GLOBAL_VARIABLES
KEY_COLUMN_USAGE
OPTIMIZER_TRACE
PARAMETERS
PARTITIONS
PLUGINS
PROCESSLIST
PROFILING
REFERENTIAL_CONSTRAINTS
ROUTINES
SCHEMATA
SCHEMA_PRIVILEGES
SESSION_STATUS
SESSION_VARIABLES
STATISTICS
TABLES
TABLESPACES
TABLE_CONSTRAINTS
TABLE_PRIVILEGES
TRIGGERS
USER_PRIVILEGES
VIEWS
INNODB_LOCKS
INNODB_TRX
INNODB_SYS_DATAFILES
INNODB_FT_CONFIG
INNODB_SYS_VIRTUAL
INNODB_CMP
INNODB_FT_BEING_DELETED
INNODB_CMP_RESET
INNODB_CMP_PER_INDEX
INNODB_CMPMEM_RESET
INNODB_FT_DELETED
INNODB_BUFFER_PAGE_LRU
INNODB_LOCK_WAITS
INNODB_TEMP_TABLE_INFO
INNODB_SYS_INDEXES
INNODB_SYS_TABLES
INNODB_SYS_FIELDS
INNODB_CMP_PER_INDEX_RESET
INNODB_BUFFER_PAGE
INNODB_FT_DEFAULT_STOPWORD
INNODB_FT_INDEX_TABLE
INNODB_FT_INDEX_CACHE
INNODB_SYS_TABLESPACES
INNODB_METRICS
INNODB_SYS_FOREIGN_COLS
INNODB_CMPMEM
INNODB_BUFFER_POOL_STATS
INNODB_SYS_COLUMNS
INNODB_SYS_FOREIGN
INNODB_SYS_TABLESTATS
~~~


1、SCHEMATA表：提供了当前mysql实例中所有数据库的信息。是show databases的结果取之此表。

2、TABLES表：提供了关于数据库中的表的信息（包括视图）。详细表述了某个表属于哪个schema，表类型，表引擎，创建时间等信息。是show tables from schemaname的结果取之此表。

3、COLUMNS表：提供了表中的列信息。详细表述了某张表的所有列以及每个列的信息。是show columns from schemaname.tablename的结果取之此表。

4、STATISTICS表：提供了关于表索引的信息。是show index from schemaname.tablename的结果取之此表。

5、USER_PRIVILEGES（用户权限）表：给出了关于全程权限的信息。该信息源自mysql.user授权表。是非标准表。

6、SCHEMA_PRIVILEGES（方案权限）表：给出了关于方案（数据库）权限的信息。该信息来自mysql.db授权表。是非标准表。

7、TABLE_PRIVILEGES（表权限）表：给出了关于表权限的信息。该信息源自mysql.tables_priv授权表。是非标准表。

8、COLUMN_PRIVILEGES（列权限）表：给出了关于列权限的信息。该信息源自mysql.columns_priv授权表。是非标准表。

9、CHARACTER_SETS（字符集）表：提供了mysql实例可用字符集的信息。是SHOW CHARACTER SET结果集取之此表。

10、COLLATIONS表：提供了关于各字符集的对照信息。

11、COLLATION_CHARACTER_SET_APPLICABILITY表：指明了可用于校对的字符集。这些列等效于SHOW COLLATION的前两个显示字段。

12、TABLE_CONSTRAINTS表：描述了存在约束的表。以及表的约束类型。

13、KEY_COLUMN_USAGE表：描述了具有约束的键列。

14、ROUTINES表：提供了关于存储子程序（存储程序和函数）的信息。此时，ROUTINES表不包含自定义函数（UDF）。名为“mysql.proc name”的列指明了对应于INFORMATION_SCHEMA.ROUTINES表的mysql.proc表列。

15、VIEWS表：给出了关于数据库中的视图的信息。需要有show views权限，否则无法查看视图信息。

16、TRIGGERS表：提供了关于触发程序的信息。必须有super权限才能查看该表

17、FILES表，innodb所有表文件（ibd+frm）


######索引
SELECT * FROM 	information_schema.STATISTICS
