---
title: mysql-主从复制之在线设置或忽略需要同步的库和表.md
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
title: mysql-主从复制之在线设置或忽略需要同步的库和表.md
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
在 EMySQL5.5/5.6版本里,设置同步复制过滤,例如,设置忽略掉test库的t2表,你需要在my.cnf配置文件里增加 replicate-ignore-table=test. t2 必须重启mysq服务进程才能生效 

在 MySQL5.7里,通过一个新的命令,可以支持在线动态修改,而无须重mysq进程就生效 

~~~
CHANGE REPLICATION FILTER REPLICATE_DO_DB = ( db1, db2 );
CHANGE REPLICATION FILTER REPLICATE_IGNORE_DB = ( db1, db2 );
CHANGE REPLICATION FILTER REPLICATE_DO_TABLE = ( db1.t1 );
CHANGE REPLICATION FILTER REPLICATE_IGNORE_TABLE = ( db2.t2 ); 
CHANGE REPLICATION FILTER REPLICATE_WILD_DO_TABLE = ('db.t%');
CHANGE REPLICATION FILTER REPLICATE_WILD_IGNORE_TABLE = ('db.t%');
~~~

增强了易用性,方便了不少。 MariaDB110.1并不提供此功能。
