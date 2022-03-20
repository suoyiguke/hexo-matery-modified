---
title: mysql如何从5-6升级到5-7？.md
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
title: mysql如何从5-6升级到5-7？.md
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
https://dev.mysql.com/doc/refman/5.7/en/upgrade-binary-package.html#upgrade-procedure-inplace
###In-place Upgrade 
>原地跟新，非常快。但是需要停机

5.7版本的mysql可以直接使用5.6版本的data，因此无需导入导出。


1、下载一个5.7版本
2、stop mysql 5.6
>建议stop后备份整个data目录，防止意外发生

3、unlink mysql 删除原来指向5.6的软链
4、ln -s mysql5.7 mysql 创建新的指向5.7的软链  
5、/etc/init.d/mysql.server start  启动5.7

那么元数据呢？
6、查看error.log
Created with MySQL 50628,now running 50716.
Please use mysql_upgrade to fix this error.

7、那么执行下 mysql_upgrade -s 
只更新元数据表（system table）不跟新业务表

8、/etc/init.d/mysql.server restart 重启

9、再看error.log，已经看不到有erro信息


为什么说5.0升级到5.7没有任何问题呢？
官方文章有提到
https://mysqlserverteam.com/upgrading-directly-from-mysql-5-0-to-5-7-using-an-in-place-upgrade/

跨大版本降级是不行的，小版本可以。这是一个值得注意的地方。
高版本总是兼容低版本，低版本不会加兼容高版本。


问题：
1、升级后性能会有变化吗？
完全不会，因为my.cnf配置并没有修改。除非是因为新版本中已经提供了新参数，我们需要配置下。
2、不停机备份可以直接使用cp命令备份吗？
不可以，copy data目录必须在停机下使用。
如果想要做到不停机备份，就得使用别的热备工具。
3、为什么不使用导入导出？
线上数据过于庞大，导入导出效率太低！
网易mysql 最低300G,生产库平均 500G，较大900G。

4、如何做到不停机升级?
ip飘移。
先升级从机再升级主机
swtich over过来

5、升级主库的话，主库停机从库扛着。那么业务在从库产生的数据如何同步到主库？

因为我们在做搞可用的时候会飘一个，还会绑一个虚ip。
虚ip飘到从机，从机会升级为主机。那么升级的原来的主机会作为从机。这样数据还是会同步过去。

6、错误时间可以调整系统时间吗？
5.7  log_timestamps='SYSTEM' 变成系统时间了

7、主从版本不同可以同吗？
5.7同步5.6没问题，5.6同步5.7不行


