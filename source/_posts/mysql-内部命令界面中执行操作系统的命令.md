---
title: mysql-内部命令界面中执行操作系统的命令.md
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
title: mysql-内部命令界面中执行操作系统的命令.md
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

~~~
mysql> system ls;
appmetadatadb_20181210.sql  deleteDataInExtractdb.sh	       lib     my.cnf_20181023	       share				 sql_backup_20181123.tar
bin			    deleteDataInExtractdb.sh_20181226  log     poi_maintainer_log.sql  shop_device_day_20181211_all.sql  support-files
data			    extractdb.tar		       my.cnf  run		       sql_backup_20181123		 tmp
mysql> 
~~~

##### 2.2 查看当前路径

~~~
mysql> system pwd;
/data/mysql/my3307
~~~
