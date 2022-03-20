---
title: mysql-全部log-配置.md
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
title: mysql-全部log-配置.md
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
全部的
~~~
[mysqld]
#——--------—-MysQL Log setting------------——#
log_error=mysql-error.log
log_bin=mysql-bin.log
slow_query_log_file=mysql-slow.log
relay_log=mysql-relay.log
log_slave_updates=1
sync_binlog=1
relay_log_recovery=1
binlog_format=row
expire_logs_days=30
slow_query_log=1 
long_query_time=2
log_queries_not_using_indexes=1
log_throttle_queries_not_using_indexes=10
log_slow_admin_statements=1
log_slow_slave_statements=1
min_examined_row_limit=1000
log_output=FILE

[mysqld-5.7]
log_timestamps=system 
~~~

~~~
