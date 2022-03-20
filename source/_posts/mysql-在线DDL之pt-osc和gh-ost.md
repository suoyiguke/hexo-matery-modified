---
title: mysql-在线DDL之pt-osc和gh-ost.md
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
title: mysql-在线DDL之pt-osc和gh-ost.md
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
gh-ost 是 GitHub 开源的在线更改 MySQL 表结构的工具
github  https://github.com/github/gh-ost/
从国内仓库下载速度会快点 https://gitee.com/mirrors/gh-ost
在centeros上推荐使用rpm方式安装
~~~
wget https://github.com/github/gh-ost/releases/download/v1.1.0/gh-ost-1.1.0-1.x86_64.rpm
rpm -i gh-ost-1.1.0-1.x86_64.rpm 
~~~

**原理**
gh-ost有三种工作模式

模式一、连接从库，在主库转换
这是 gh-ost 默认的工作模式，它会查看从库情况，找到集群的主库并且连接上去，对主库侵入最少
连接从库，变更主库 - 默认方式，slave需要开启log-slave-update；
大体步骤是：
1、在主库上创建 _xxx_gho（和原表表结构一致）、_xxx_ghc（记录变更日志），并修改 _xxx_gho 表结构；
2、从 slave 上读取二进制日志事件，将变更应用到主库上的 _xxx_gho 表；
3、在主库上读源表的数据写入 _xxx_gho 表中；
4、在主库上完成表切换。

模式二、连接主库，在主库转换
需要使用 --allow-on-master 选项：
1.在变更的服务器上 创建 ghost table( _tbname_gho like tbname)
2.更改 _tbname_gho 结构为新表结构
3.作为mysql的slave连接mysql server，并记录新增binlog event
4.交替执行: 应用新增events到 ghost table 和 复制老表的记录到 ghost table
5.使用原子性的rename来进行table重命名(ghost table 替代 老表)


>模拟mysql从机从主机的Binlog Dump线程中接收数据

模式三、在从库上测试和转换
这种模式会在从库上做修改。gh-ost 仍然会连上主库，但所有操作都是在从库上做的，不会对主库产生任何影响。在操作过程中，gh-ost 也会不时地暂停，以便从库的数据可以保持最新。
--migrate-on-replica 选项让 gh-ost 直接在从库上修改表。最终的切换过程也是在从库正常复制的状态下完成的。
--test-on-replica 表明操作只是为了测试目的。在进行最终的切换操作之前，复制会被停止。原始表和临时表会相互切换，再切换回来，最终相当于原始表没被动过。主从复制暂停的状态下，你可以检查和对比这两张表中的数据。



**注意**
操作的mysql需开启row类型的binlog
1、原表必须要有主键或者唯一索引（不含NULL）
2、不支持外键
3、不支持触发器
4、不支持虚拟列
5、不支持 5.7 point类型的列
6、 mysql 5.7 JSON列不能是主键
7、不能存在另外一个table名字一样，只是大小写有区别
8、不支持多源复制
9、不支持M-M 双写
10、不支持FEDERATED engine


**测试**

gh-ost --user="root" --password="Sgl20@14" --host=192.168.1.116 --database="test" --table="user" --alter="ALTER TABLE user MODIFY COLUMN name char(6) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER id;" --allow-on-master --execute



**对比**

gh-ost基于binlog处理，所以性能赶不上pt-osc；但是不需要需要创建触发器，不对原表有改动；读binlog可以放在从库执行，减少主库的压力；
当系统负载极高时，gh-ost有可能无法跟上binlog日志的处理（未测试过该场景）


pt-osc：percona online schema change
gh-ost：GitHub's online schema migration for MySQL







**快速使用**
1、简单使用它来添加cc2 、cc3 两个字段到test.test1；使用--allow-on-master 直接连接主库
>gh-ost --user="root" --password="Sgl20@14" --host=192.168.1.116 --database="test" --table="test1" --alter="ADD COLUMN cc2 varchar(10),add column cc3 int not null default 0 comment 'test' " --allow-on-master --execute
~~~
[root@localhogh-ost --user="root" --password="Sgl20@14" --host=192.168.1.116 --database="test" --table="test1" --alter="ADD COLUMN cc2 varchar(10),add column cc3 int not null default 0 comment 'test' " --allow-on-master --execute
[2021/03/02 14:41:21] [info] binlogsyncer.go:133 create BinlogSyncer with config {99999 mysql 192.168.1.116 3306 root    false false <nil> false UTC true 0 0s 0s 0 false}
[2021/03/02 14:41:21] [info] binlogsyncer.go:354 begin to sync binlog from position (mysql-bin.000011, 154)
[2021/03/02 14:41:21] [info] binlogsyncer.go:203 register slave for master server 192.168.1.116:3306
[2021/03/02 14:41:21] [info] binlogsyncer.go:723 rotate to (mysql-bin.000011, 154)
# Migrating `test`.`test1`; Ghost table is `test`.`_test1_gho`
# Migrating jiazhi09:3306; inspecting jiazhi09:3306; executing on localhost.localdomain
# Migration started at Tue Mar 02 14:41:14 +0800 2021
# chunk-size: 1000; max-lag-millis: 1500ms; dml-batch-size: 10; max-load: ; critical-load: ; nice-ratio: 0.000000
# throttle-additional-flag-file: /tmp/gh-ost.throttle 
# Serving on unix socket: /tmp/gh-ost.test.test1.sock
Copy: 0/68175 0.0%; Applied: 0; Backlog: 0/1000; Time: 6s(total), 0s(copy); streamer: mysql-bin.000011:2975; Lag: 0.01s, State: migrating; ETA: N/A
Copy: 0/68175 0.0%; Applied: 0; Backlog: 0/1000; Time: 7s(total), 1s(copy); streamer: mysql-bin.000011:10192; Lag: 0.01s, State: migrating; ETA: N/A
Copy: 69632/69632 100.0%; Applied: 0; Backlog: 0/1000; Time: 8s(total), 1s(copy); streamer: mysql-bin.000011:682322; Lag: 0.01s, State: migrating; ETA: due
Copy: 69632/69632 100.0%; Applied: 0; Backlog: 1/1000; Time: 8s(total), 1s(copy); streamer: mysql-bin.000011:687276; Lag: 0.01s, State: migrating; ETA: due
# Migrating `test`.`test1`; Ghost table is `test`.`_test1_gho`
# Migrating jiazhi09:3306; inspecting jiazhi09:3306; executing on localhost.localdomain
# Migration started at Tue Mar 02 14:41:14 +0800 2021
# chunk-size: 1000; max-lag-millis: 1500ms; dml-batch-size: 10; max-load: ; critical-load: ; nice-ratio: 0.000000
# throttle-additional-flag-file: /tmp/gh-ost.throttle 
# Serving on unix socket: /tmp/gh-ost.test.test1.sock
Copy: 69632/69632 100.0%; Applied: 0; Backlog: 0/1000; Time: 9s(total), 1s(copy); streamer: mysql-bin.000011:691965; Lag: 0.01s, State: migrating; ETA: due
[2021/03/02 14:41:24] [info] binlogsyncer.go:164 syncer is closing...
[2021/03/02 14:41:24] [error] binlogstreamer.go:77 close sync with err: sync is been closing...
[2021/03/02 14:41:24] [info] binlogsyncer.go:179 syncer is closed
# Done

~~~

2、在主从复制结构中连接从机


>gh-ost --host=192.168.1.116 --port=3307 --user="root" --password="Sgl20@14" --database="test"  --table="test1" --alter="ADD COLUMN cc4 varchar(10),add column cc5 int not null default 0 comment 'test' "  --execute


**参数解释**
--max-load=Threads_running=25 表面如果在执行gh-ost的过程中出现Threads_running=25则暂停gh-ost的执行
--critical-load=Threads_running=60 表明执行过程中出现Threads_running达到60则终止gh-ost的执行
--chunk-size=1000 设置每次从原表copy到 ghost table的行数
--ok-to-drop-table 执行完之后删除原表
--allow-on-master 直连主库执行


