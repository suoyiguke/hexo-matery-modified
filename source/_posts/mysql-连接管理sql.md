---
title: mysql-连接管理sql.md
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
title: mysql-连接管理sql.md
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

###1、显示当前正在执行的MySQL连接。
~~~
show processlist;
~~~

###2、查看每个ip的当前连接数

合并ip
~~~
SELECT
	SUBSTRING_INDEX( HOST, ':', 1 ) AS ip,
	count( * ) 
FROM
	information_schema.PROCESSLIST 
GROUP BY
	ip;
~~~

根据ip分开查询 连接具体状态
~~~
SELECT
	substring_index( HOST, ':', 1 ) AS host_name,
	state,
	count( * ) 
FROM
	information_schema.PROCESSLIST 
GROUP BY
	state,
	host_name
~~~
数量之和 = SHOW STATUS LIKE 'Threads_connected';





###3、当前活跃连接数
~~~
SHOW STATUS LIKE 'Thread_%';
~~~

1、Thread_cached: 被缓存的线程的个数
2、Threads_connected：当前连接的线程的个数
3、Threads_created：总创建的连接数
2、Threads_running：处于激活状态的线程的个数

