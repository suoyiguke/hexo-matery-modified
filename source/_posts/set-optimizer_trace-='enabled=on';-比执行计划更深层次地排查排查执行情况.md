---
title: set-optimizer_trace-='enabled=on';-比执行计划更深层次地排查排查执行情况.md
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
title: set-optimizer_trace-='enabled=on';-比执行计划更深层次地排查排查执行情况.md
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
从MySQL5.6版本开始，optimizer_trace 可支持把MySQL查询执行计划树打印出来，对DBA深入分析SQL执行计划，COST成本都非常有用，打印的内部信息比较全面。默认是关闭的，功能支持动态开关，因为对性能有20%左右影响，只建议分析问题时，临时开启。

1. 默认是关闭的
~~~
mysql> show variables like 'optimizer_trace';
+-----------------+--------------------------+
| Variable_name | Value |
+-----------------+--------------------------+
| optimizer_trace | enabled=off,one_line=off |
+-----------------+--------------------------+
1 row in set (0.05 sec)
~~~
2.演示 optimizer_trace 简单的使用流程：
2.1 会话级别临时开启
~~~
mysql> set session optimizer_trace="enabled=on",end_markers_in_json=on;
~~~
2.2 执行你的SQL
~~~
select host,user,plugin from user ;
~~~
2.3 查询information_schema.optimizer_trace表
~~~
mysql> SELECT trace FROM information_schema.OPTIMIZER_TRACE\G;
~~~
2.4 导入到一个命名为xx.trace的文件，然后用JSON阅读器来查看 
~~~
SELECT TRACE INTO DUMPFILE “xx.trace” FROM INFORMATION_SCHEMA.OPTIMIZER_TRACE;
~~~

补充：永久开启 optimizer_trace    （重启失效）
~~~
mysql> set optimizer_trace="enabled=on";
~~~
 

###实践
~~~
set optimizer_trace ='enabled=on'; -- 打开跟踪，只能查看自己session执行语句情况
SELECT *  from information_schema.OPTIMIZER_TRACE
~~~

~~~
SELECT @@optimizer_trace
enabled=on,one_line=off
~~~
>这东西只能在命令行下才能看到内容！
