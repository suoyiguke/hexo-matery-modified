---
title: mysql-sql性能统计和执行时间剖析.md
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
title: mysql-sql性能统计和执行时间剖析.md
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
###查看最近执行的的sql耗时

使用 SHOW PROFILES可以得到最近执行的sql的执行时间。
比如，要比较两种sql的执行时间。可以这样做，注意中间需要使用`RESET QUERY CACHE;` 清除QUERY CACHE缓存避免影响实验结果
~~~
SET profiling = 1;
.............sql1........
RESET QUERY CACHE;
.............sql2........
SHOW PROFILES;
~~~

