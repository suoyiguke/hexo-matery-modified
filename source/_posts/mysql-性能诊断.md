---
title: mysql-性能诊断.md
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
title: mysql-性能诊断.md
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
###诊断步骤
1．检查系统全局资源负载
2．检查MySQL错误日志
3.  检查MySQL在做什么
4. 检查lnnoDB事务情况
5. 检查MySQL复制状态


###MySQL诊断工具
1、 error log & slow log & general log
2、MySQL SHOW [SESSION|GLOBAL]STATUS
3、SHOW PROCESSLIST
4、lnnoDB存储引擎状态 SHOW ENGINE INNODB STATUS
5、Explain查看执行计划
6、performance schema


###快速诊断

- top 判断主机负载情况
- dmesg | tail  是否存在oom-killer 或tcp drop等错误信息
- vmstat 1  检查r、free、si、so、us,sy, id, wa,st列
-  mpstat -P ALL 1 检查CPU使用率是否均衡
- pidstat 1  检查进程的CPU使用率，多核利用情况
- iostat -xz 1  检查r/s, w/s,rkB/s, wkB/s, await, avgqu-sz,%util
- free -m 检查内存使用情况
- sar -n DEV 1  检查网络吞吐量
- sar -n TCP,ETCP 1  检查tcp连接情况active/s, passive/s, retrans/s



###InnoDb表必须有主键或唯一索引


查询没有主键的表
没有设置主键的表的DML性能将非常低！用下面sql可以查出所有没有创建主键的表。
我们可以给它加上主键
~~~
SELECT
	t.table_schema,
	t.table_name 
FROM
	information_schema.TABLES t
	LEFT JOIN information_schema.table_constraints c ON ( t.table_schema = c.table_schema AND t.table_name = c.table_name AND c.constraint_type IN ( 'PRIMARY KEY', 'UNIQUE' ) ) 
WHERE
	t.table_schema NOT IN (
		'mysql',
		'information_schema',
	'PERFORMANCE_SCHEMA') AND t.engine = 'InnoDB'
	AND c.table_name IS NULL;
~~~


###避免大事务，运行时间长或变更记录多
~~~

	
SELECT
	a.requesting_trx_id '被阻塞事务ID',
	b.trx_mysql_thread_id '被阻塞线程ID',
	TIMESTAMPDIFF( SECOND, b.trx_wait_started, NOW( ) ) '被阻塞秒数',
	b.trx_query '被阻塞的语句',
	a.blocking_trx_id '阻塞事务ID',
	c.trx_mysql_thread_id '阻塞线程ID',
	d.INFO '阻塞事务信息' 
FROM
	information_schema.INNODB_LOCK_WAITS a
	INNER JOIN information_schema.INNODB_TRX b ON a.requesting_trx_id = b.trx_id
	INNER JOIN information_schema.INNODB_TRX c ON a.blocking_trx_id = c.trx_id
	INNER JOIN information_schema.PROCESSLIST d ON c.trx_mysql_thread_id = d.ID;
~~~


###性能诊断重要参数

• max_connection
• innodb_buffer_pool_size
• Innodb_flush_neighbors
• Innodb_io_capacity
• Innodb_log_file_size
• innodb_thread_concurrency
