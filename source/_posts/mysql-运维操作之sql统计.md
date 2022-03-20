---
title: mysql-运维操作之sql统计.md
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
title: mysql-运维操作之sql统计.md
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
###统计信息(SQL维度)
1、执行次数最多的SQL
~~~
SELECT
 DIGEST_TEXT,
 COUNT_STAR,
 FIRST_SEEN,
 LAST_SEEN 
FROM
 `performance_schema`.events_statements_summary_by_digest 
ORDER BY
 COUNT_STAR DESC;
~~~


2、平均响应时间最多的sql
~~~
SELECT
 DIGEST_TEXT,
 AVG_TIMER_WAIT,
 COUNT_STAR,
 FIRST_SEEN,
 LAST_SEEN 
FROM
 `performance_schema`.events_statements_summary_by_digest 
ORDER BY
 AVG_TIMER_WAIT DESC;
~~~


3、排序记录数最多
~~~
SELECT
 DIGEST_TEXT,
SUM_SORT_ROWS,
 COUNT_STAR,
 FIRST_SEEN,
 LAST_SEEN 
FROM
 `performance_schema`.events_statements_summary_by_digest 
ORDER BY
 SUM_SORT_ROWS DESC;
~~~

4、扫描记录数最多的
~~~
SELECT
 DIGEST_TEXT,
 SUM_ROWS_EXAMINED,
 COUNT_STAR,
 FIRST_SEEN,
 LAST_SEEN 
FROM
 `performance_schema`.events_statements_summary_by_digest 
ORDER BY
 SUM_ROWS_EXAMINED DESC;
~~~

5、使用临时表最多的sql
~~~
SELECT
 DIGEST_TEXT,
 SUM_CREATED_TMP_TABLES,
 SUM_CREATED_TMP_DISK_TABLES,
 COUNT_STAR,
 FIRST_SEEN,
 LAST_SEEN 
FROM
 `performance_schema`.events_statements_summary_by_digest 
ORDER BY
 SUM_CREATED_TMP_TABLES desc,SUM_CREATED_TMP_DISK_TABLES desc
~~~

6、返回结果集最多的SQL
~~~
SELECT
 DIGEST_TEXT,
 SUM_ROWS_SENT,
 COUNT_STAR,
 FIRST_SEEN,
 LAST_SEEN 
FROM
 `performance_schema`.events_statements_summary_by_digest
ORDER BY
 SUM_ROWS_SENT desc;
~~~

###统计信息(对象维度)
1、哪个表物理IO最多？
~~~
SELECT
 file_name,
 event_name,
 SUM_NUMBER_OF_BYTES_READ,
 SUM_NUMBER_OF_BYTES_WRITE 
FROM
 `performance_schema`.file_summary_by_instance 
ORDER BY
 SUM_NUMBER_OF_BYTES_READ + SUM_NUMBER_OF_BYTES_WRITE DESC;
~~~

2、哪个表逻辑IO最多?
~~~
SELECT
 object_schema,
 object_name,
 COUNT_READ,
 COUNT_WRITE,
 COUNT_FETCH,
 SUM_TIMER_WAIT 
FROM
 `performance_schema`.table_io_waits_summary_by_table 
ORDER BY
 sum_timer_wait DESC;
~~~
3、哪个索引访问最多？
~~~
SELECT
 OBJECT_SCHEMA,
 OBJECT_NAME,
 INDEX_NAME,
 COUNT_FETCH,
 COUNT_INSERT,
 COUNT_UPDATE,
 COUNT_DELETE 
FROM
 `performance_schema`.table_io_waits_summary_by_index_usage 
ORDER BY
 SUM_TIMER_WAIT DESC;
~~~






4、哪个索引从来没有使用过？
~~~
SELECT
 OBJECT_SCHEMA,
 OBJECT_NAME,
 INDEX_NAME 
FROM
 `performance_schema`.table_io_waits_summary_by_index_usage 
WHERE
 INDEX_NAME IS NOT NULL 
 AND COUNT_STAR = 0 
 AND OBJECT_SCHEMA <> 'mysql' 
ORDER BY
 OBJECT_SCHEMA,
 OBJECT_NAME;
~~~

###统计信息(等待事件维度)

1、哪个等待事件消耗的时间最多？
~~~
SELECT
 EVENT_NAME,
 COUNT_STAR,
 SUM_TIMER_WAIT,
 AVG_TIMER_WAIT 
FROM
 `performance_schema`.events_waits_summary_global_by_event_name 
WHERE
 event_name != 'idle' 
ORDER BY
 SUM_TIMER_WAIT DESC;
~~~
