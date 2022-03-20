---
title: 故障案例--mysql如何定位执行完但未提交的事务内容.md
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
title: 故障案例--mysql如何定位执行完但未提交的事务内容.md
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
1、查询mysql中当前尚未提交的事务，能查出事务最后一次执行的sql！

SELECT * from performance_schema.events_statements_current



我想到的第一种方法是利用performance_schema中的相关信息查询

mysql> showvariables like 'performance_schema';

+--------------------+-------+

|Variable_name      | Value |

+--------------------+-------+

|performance_schema | ON    |

+--------------------+-------+

1 row in set(0.00 sec)

通过查看events_statements_current表可看到每一个session正在执行的sql，哪怕它依旧执行完成了，只是没有提交。这里可看到事务1最后执行的正是updatetest_lock set id=123 where id=1;

mysql> select* from performance_schema.events_statements_current\G

***************************1\. row ***************************

              THREAD_ID: 31

               EVENT_ID: 32

           END_EVENT_ID: 32

             EVENT_NAME: statement/sql/update

                 SOURCE: mysqld.cc:956

            TIMER_START: 1540467163248000

              TIMER_END: 1540467380878000

             TIMER_WAIT: 217630000

              LOCK_TIME: 91000000

               SQL_TEXT: update test_lock setid=123 where id=1

                 DIGEST: 79642cef211ac8e9abd41afdb3d6e8e1

            DIGEST_TEXT: UPDATE `test_lock` SET`id` = ? WHERE `id` = ?

         CURRENT_SCHEMA: test

不过方案1有个缺陷，一个事务可能有一组sql组成，这个方法只能看到这个事务最后执行的是什么SQL，无法看到全部。

PS:关于information_schema.processlist和events_statements_current如何一一对应起来，可以查看performance_schema.threads表来关联，这里不多描述，给出一个可行的sql:

~~~
SELECT
	a.SQL_TEXT,
	c.id,
	d.trx_started
FROM
	events_statements_current a
JOIN threads b ON a.THREAD_ID = b.THREAD_ID
JOIN information_schema.PROCESSLIST c ON b.PROCESSLIST_ID = c.id
JOIN information_schema.innodb_trx d ON c.id = d.trx_mysql_thread_id
ORDER BY
	d.trx_started
~~~
