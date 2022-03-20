---
title: mysql-两阶段提交.md
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
title: mysql-两阶段提交.md
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
#重要的日志模块：redo log

**1、WAL技术**
而粉板和账本配合的整个过程，其实就是MySQL里经常说到的WAL技术，WAL的全称是Write-Ahead Logging 预写式日志，它的关键点就是先写日志，再写磁盘，也就是先写粉板，等不忙的时候再写账本。
具体来说，当有一条记录需要更新的时候，InnoDB引擎就会先把记录写到redo log（粉板）里面，并更新内存，这个时候更新就算完成了。同时，InnoDB引擎会在适当的时候，将这个操作记录更新到磁盘里面，而这个更新往往是在系统比较空闲的时候做，这就像打烊以后掌柜做的事。

如果今天赊账的不多，掌柜可以等打烊后再整理。但如果某天赊账的特别多，粉板写满了，又怎么办呢？这个时候掌柜只好放下手中的活儿，把粉板中的一部分赊账记录更新到账本中，然后把这些记录从粉板上擦掉，为记新账腾出空间。

与此类似，InnoDB的redo log是固定大小的，比如可以配置为一组4个文件，每个文件的大小是1GB，那么这块“粉板”总共就可以记录4GB的操作。从头开始写，写到末尾就又回到开头循环写，如下面这个图所示。

![image](https://upload-images.jianshu.io/upload_images/13965490-9e8009bf7667f5e3.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

write pos是当前记录的位置，一边写一边后移，写到第3号文件末尾后就回到0号文件开头。checkpoint是当前要擦除的位置，也是往后推移并且循环的，擦除记录前要把记录更新到数据文件。

write pos和checkpoint之间的是“粉板”上还空着的部分，可以用来记录新的操作。如果write pos追上checkpoint，表示“粉板”满了，这时候不能再执行新的更新，得停下来先擦掉一些记录，把checkpoint推进一下。


**2、crash-safe能力**
有了redo log，InnoDB就可以保证即使数据库发生异常重启，之前提交的记录都不会丢失，这个能力称为crash-safe。
要理解crash-safe这个概念，可以想想我们前面赊账记录的例子。只要赊账记录记在了粉板上或写在了账本上，之后即使掌柜忘记了，比如突然停业几天，恢复生意后依然可以通过账本和粉板上的数据明确赊账账目。

**3、两阶段提交**
将redo log的写入拆成了两个步骤：prepare和commit，这就是"两阶段提交"。

# 重要的日志模块：binlog


1、redo log是InnoDB引擎特有的日志，而Server层也有自己的日志，称为binlog（归档日志）。



####redolog和binlog 这两种日志有以下三点不同。

1.  redo log是InnoDB引擎特有的；binlog是MySQL的Server层实现的，所有引擎都可以使用。
2.  redo log是物理日志，记录的是“在某个数据页上做了什么修改：修改前修改后和修改关系”；binlog是逻辑日志，记录的是这个语句的原始逻辑，比如“给ID=2这一行的c字段加1 ”。
3.  redo log是循环写的，空间固定会用完；binlog是可以追加写入的。“追加写”是指binlog文件写到一定大小后会切换到下一个，并不会覆盖以前的日志。




#什么是两阶段提交？
1 redolog prepare阶段 2 写binlog 3 redolog commit阶段

当在2之前崩溃时
重启恢复：后发现没有commit，回滚。备份恢复：没有binlog 。一致

当在3之前崩溃
重启恢复：虽没有commit，但满足prepare和binlog完整，所以重启后会自动commit。备份：有binlog. 一致

>两阶段提交是跨系统维持`数据逻辑一致性`时常用的一个方案，即使你不做数据库内核开发，日常开发中也有可能会用到。


#为什么需要两阶段提交, 两阶段提交怎么保证数据库中两份日志间的逻辑一致性(什么叫逻辑一致性)? 
使用binlog恢复数据之后的状态



#如果不是两阶段提交, 先写redo log和先写bin log两种情况各会遇到什么问题?
如果不用两阶段提交，要么就是先写完redo log再写binlog，或者采用反过来的顺序。我们看看这两种方式会有什么问题。仍然用前面的update语句来做例子。假设当前ID=2的行，字段c的值是0，再假设执行update语句过程中在写完第一个日志后，第二个日志还没有写完期间发生了crash，会出现什么情况呢？

1、先写redo log后写binlog。假设在redo log写完，binlog还没有写完的时候，MySQL进程异常重启。由于我们前面说过的，redo log写完之后，系统即使崩溃，仍然能够把数据恢复回来，所以恢复后这一行c的值是1。
但是由于binlog没写完就crash了，这时候binlog里面就没有记录这个语句。因此，之后备份日志的时候，存起来的binlog里面就没有这条语句。
然后你会发现，如果需要用这个binlog来恢复临时库的话，由于这个语句的binlog丢失，这个临时库就会少了这一次更新，恢复出来的这一行c的值就是0，与原库的值不同。

2、先写binlog后写redo log。如果在binlog写完之后crash，由于redo log还没写，崩溃恢复以后这个事务无效，所以这一行c的值是0。但是binlog里面已经记录了“把c从0改成1”这个日志。所以，在之后用binlog来恢复的时候就多了一个事务出来，恢复出来的这一行c的值就是1，与原库的值不同。

#redolog和binlog的功能侧重点
redolog在于 crash-safe
binlog在于 归档

#redolog和binlog分别记录什么？
1、Redo log 记录这个页 “做了什么改动”
2、binlog记录看是选择那种模式。 Binlog有两种模式，statement 格式的话是记sql语句， row格式会记录行的内容，记两条，更新前和更新后都有;
来看一段mysqlbinlog导出的row类型的binlog日志，明显记录了id从2改为了3
>mysqlbinlog  --no-defaults --database=test --base64-output=decode-rows -v  C:\mysql5715\data\mysql-bin.000003 >zz.sql
~~~
BEGIN
/*!*/;
# at 291
#210225 11:57:18 server id 1  end_log_pos 336 CRC32 0x590f19dd 	Table_map: `test`.`ff` mapped to number 114
# at 336
#210225 11:57:18 server id 1  end_log_pos 382 CRC32 0x60df92de 	Update_rows: table id 114 flags: STMT_END_F
### UPDATE `test`.`ff`
### WHERE
###   @1=2
### SET
###   @1=3
# at 382
#210225 11:57:18 server id 1  end_log_pos 413 CRC32 0x42a39683 	Xid = 17771313
COMMIT/*!*/;
~~~
#redolog和binlog是分别什么类型的日志？
redo是物理的，binlog是逻辑的；

#redolog和binlog是分别属于mysql架构的那个部分实现的？
redolog属于存储引擎（innodb独有）
binlog属于server层面

#主从复制现在是基于binlog逻辑日志的，那么像redolog这种物理日志呢？
物理复制业界有团队在做了，物理的速度也将远超逻辑的，毕竟只记录了改动向量








#mysql备份策略

我理解备份就是救命药加后悔药，灾难发生的时候备份能救命，出现错误的时候备份能后悔。事情都有两面性，没有谁比谁好，只有谁比谁合适，完全看业务情况和需求而定。一天一备恢复时间更短，binlog更少，救命时候更快，但是后悔时间更短，而一周一备正好相反。我自己的备份策略是设置一个16小时延迟复制的从库，充当后悔药，恢复时间也较快。再两天一个全备库和binlog，作为救命药,最后时刻用。这样就比较兼顾了。

#恢复策略
昨天上午 恢复别人误操作配置表数据，幸好有xtarbackup凌晨的全量备份，只提取了改表的ibd文件，然后在本地 做了 一个一样的空表，释放该表空间，加载 提取后的ibd文件，提取昨天零晨到九点的binlog文件 筛选改表这个时段的操作记录 增量更新到本地导出csv 导入线上 。binlog太tm重要了


#一个update语句执行流程

有了对这两个日志的概念性理解，我们再来看执行器和InnoDB引擎在执行这个简单的update语句时的内部流程。

1.  执行器先找引擎取ID=2这一行。ID是主键，引擎直接用树搜索找到这一行。如果ID=2这一行所在的数据页本来就在内存中，就直接返回给执行器；否则，需要先从磁盘读入内存，然后再返回。

2.  执行器拿到引擎给的行数据，把这个值加上1，比如原来是N，现在就是N+1，得到新的一行数据，再调用引擎接口写入这行新数据。

3.  引擎将这行新数据更新到内存中，同时将这个更新操作记录到redo log里面，此时redo log处于prepare状态。然后告知执行器执行完成了，随时可以提交事务。

4.  执行器生成这个操作的binlog，并把binlog写入磁盘。

5.  执行器调用引擎的提交事务接口，引擎把刚刚写入的redo log改成提交（commit）状态，更新完成。

这里我给出这个update语句的执行流程图，图中浅色框表示是在InnoDB内部执行的，深色框表示是在执行器中执行的。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-4a21e37131039d90.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

你可能注意到了，最后三步看上去有点“绕”，将redo log的写入拆成了两个步骤：prepare和commit，这就是"两阶段提交"。
