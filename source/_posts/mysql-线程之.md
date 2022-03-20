---
title: mysql-线程之.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-线程之.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---

###1、Purge Thread



>purge thread：清空undo页、清理“deleted”page


 Purge Thread 事务被提交后,其所使用的 undolog可能不再需要,因此需要 Purge Thread来回收 已经使用并分配的undo页。

在 InnoDB1.1版本之前, purge操作仅在 InnoDB存储引擎 的 Master Thread中完成。

而从 InnoDB1.1版本开始, purge操作可以独立到单独的线 程中进行,以此来减轻Master Thread的工作从而提高CPU的使用率以及提升存储引 擎的性能。
用户可以在 MySQL数据库的配置文件中添加如下命令来启用独立的 Purge Thread: 
~~~
[mysqld] innodb_purge_threads=1
~~~
在 InnoDB1.1版本中,即使将 innodbpurge_threads设为大于1, InnoDB存储引擎 启动时也会将其设为1,并在错误文件中出现如下类似的提示: 120529 22: 54: 16 [Warning] option 'innodb-purge-threads': unsigned value 4 adjusted to 1 "




###page cleaner thread：刷新脏页
