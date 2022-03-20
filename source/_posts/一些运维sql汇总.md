---
title: 一些运维sql汇总.md
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
title: 一些运维sql汇总.md
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
###5.7 统计线程消耗内存
select thread_id, event_name, SUM_NUMBER_OF_BYTES_ALLOC from performance_schema.memory_summary_by_thread_by_event_name order by SUM_NUMBER_OF_BYTES_ALLOC desc limit 10;
###查看LRU的具体信息的表
SELECT * FROM information_schema.innodb_buffer_page_lru;

###查看mysql 哪个库或者那个表占用内存最大
select * from sys.innodb_buffer_stats_by_table;

###查看buffer pool 空间占用情况

SELECT pool_id,pool_size,free_buffers,database_pages FROM information_schema.innodb_buffer_pool_stats;
