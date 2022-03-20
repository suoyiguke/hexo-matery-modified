---
title: sys-statement_analysis-sql查询时间统计.md
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
title: sys-statement_analysis-sql查询时间统计.md
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
SELECT
	* 
FROM
	sys.statement_analysis WHERE db='mgb_treasure_system'


该表记录了执行的sql，比慢查询日志更方便。非常有用


1、statement_analysis是一个视图
2、默认按SUM_TIMER_WAIT倒序。查询最慢的查询会从上到下
3、statement_analysis可以代替慢查询的部分功能。只想得到慢查询日志可以直接使用statement_analysis。若想得到具体某个时间点的满查询还是得用忙查询。
~~~

CREATE ALGORITHM = MERGE DEFINER = `mysql.sys` @`localhost` SQL SECURITY INVOKER VIEW `statement_analysis` AS SELECT
`sys`.`format_statement` ( `performance_schema`.`events_statements_summary_by_digest`.`DIGEST_TEXT` ) AS `query`,
`performance_schema`.`events_statements_summary_by_digest`.`SCHEMA_NAME` AS `db`,
IF
	( ( ( `performance_schema`.`events_statements_summary_by_digest`.`SUM_NO_GOOD_INDEX_USED` > 0 ) OR ( `performance_schema`.`events_statements_summary_by_digest`.`SUM_NO_INDEX_USED` > 0 ) ), '*', '' ) AS `full_scan`,
	`performance_schema`.`events_statements_summary_by_digest`.`COUNT_STAR` AS `exec_count`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_ERRORS` AS `err_count`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_WARNINGS` AS `warn_count`,
	`sys`.`format_time` ( `performance_schema`.`events_statements_summary_by_digest`.`SUM_TIMER_WAIT` ) AS `total_latency`,
	`sys`.`format_time` ( `performance_schema`.`events_statements_summary_by_digest`.`MAX_TIMER_WAIT` ) AS `max_latency`,
	`sys`.`format_time` ( `performance_schema`.`events_statements_summary_by_digest`.`AVG_TIMER_WAIT` ) AS `avg_latency`,
	`sys`.`format_time` ( `performance_schema`.`events_statements_summary_by_digest`.`SUM_LOCK_TIME` ) AS `lock_latency`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_ROWS_SENT` AS `rows_sent`,
	round( ifnull( ( `performance_schema`.`events_statements_summary_by_digest`.`SUM_ROWS_SENT` / nullif( `performance_schema`.`events_statements_summary_by_digest`.`COUNT_STAR`, 0 ) ), 0 ), 0 ) AS `rows_sent_avg`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_ROWS_EXAMINED` AS `rows_examined`,
	round( ifnull( ( `performance_schema`.`events_statements_summary_by_digest`.`SUM_ROWS_EXAMINED` / nullif( `performance_schema`.`events_statements_summary_by_digest`.`COUNT_STAR`, 0 ) ), 0 ), 0 ) AS `rows_examined_avg`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_ROWS_AFFECTED` AS `rows_affected`,
	round( ifnull( ( `performance_schema`.`events_statements_summary_by_digest`.`SUM_ROWS_AFFECTED` / nullif( `performance_schema`.`events_statements_summary_by_digest`.`COUNT_STAR`, 0 ) ), 0 ), 0 ) AS `rows_affected_avg`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_CREATED_TMP_TABLES` AS `tmp_tables`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_CREATED_TMP_DISK_TABLES` AS `tmp_disk_tables`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_SORT_ROWS` AS `rows_sorted`,
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_SORT_MERGE_PASSES` AS `sort_merge_passes`,
	`performance_schema`.`events_statements_summary_by_digest`.`DIGEST` AS `digest`,
	`performance_schema`.`events_statements_summary_by_digest`.`FIRST_SEEN` AS `first_seen`,
	`performance_schema`.`events_statements_summary_by_digest`.`LAST_SEEN` AS `last_seen` 
FROM
	`performance_schema`.`events_statements_summary_by_digest` 
ORDER BY
	`performance_schema`.`events_statements_summary_by_digest`.`SUM_TIMER_WAIT` DESC
~~~
