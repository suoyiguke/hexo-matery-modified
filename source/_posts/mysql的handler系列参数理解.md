---
title: mysql的handler系列参数理解.md
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
title: mysql的handler系列参数理解.md
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
mysql> show status like '%Handler%';
+-------------------------+-------+
| Variable_name            | Value |
+-------------------------+-------+
| Handler_commit           | 1     |
| Handler_delete            | 0     |
| Handler_discover         | 0     |
| Handler_external_lock      | 2     |
| Handler_mrr_init           | 0     |
| Handler_prepare          | 0     |
| Handler_read_first         | 1     |
| Handler_read_key         | 1     |
| Handler_read_last         | 0     |
| Handler_read_next        | 0     |
| Handler_read_prev        | 0     |
| Handler_read_rnd         | 0     |
| Handler_read_rnd_next     | 267   |
| Handler_rollback          | 0     |
| Handler_savepoint         | 0     |
| Handler_savepoint_rollback | 0     |
| Handler_update           | 0     |
| Handler_write            | 0     |
+-------------------------+-------+
18 rows in set (0.08 sec)

~~~


解释一下各个参数：
Handler_read_first：此选项表明SQL是在做一个全索引扫描，注意是全部，而不是部分，所以说如果存在WHERE语句，这个选项是不会变的。
Handler_read_key：此选项数值如果很高，那么恭喜你，你的系统高效的使用了索引，一切运转良好。
Handler_read_next：此选项表明在进行索引扫描时，按照索引从数据文件里取数据的次数。
Handler_read_prev：此选项表明在进行索引扫描时，按照索引倒序从数据文件里取数据的次数，一般就是ORDER BY … DESC
Handler_read_rnd：就是查询直接操作了数据文件，很多时候表现为没有使用索引或者文件排序。
Handler_read_rnd_next：此选项表明在进行数据文件扫描时，从数据文件里取数据的次数。

可以看到这个sql的Handler_read_prev为2828694，该值已经非常的高。所以这个sql即便索引使用正确，也还是需要0.68s这么长的时间，同样我们可以看一下将desc换成asc时候的Handler_read_next：



