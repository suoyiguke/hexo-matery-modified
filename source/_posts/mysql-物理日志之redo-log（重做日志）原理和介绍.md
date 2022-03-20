---
title: mysql-物理日志之redo-log（重做日志）原理和介绍.md
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
title: mysql-物理日志之redo-log（重做日志）原理和介绍.md
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
重做日志用来实现事务的持久性,即事务ACID中的D。 InnoDB是事务的存储引擎,其通过 Force Log at Commit机制实现事务的持久性,即当事务提交(COMMIT)时,必须先将该事务的所有日志写入到重做日志文件 进行持久化,待事务的COMMIT操作完成才算完成。

当我们想要修改DB上某一行数据的时候，InnoDB是把数据从磁盘读取到内存的缓冲池bp（buffer pool）上进行修改。这个时候数据在内存中被修改，与磁盘中相比就存在了差异，我们称这种有差异的数据为`脏页`（dirty page）。脏页指的是buffer pool中与磁盘不同的数据页。

而mysql对脏页的处理不是每次生成脏页就将脏页刷新回磁盘，这样会产生海量的IO操作，严重影响InnoDB的处理性能。既然脏页与磁盘中的数据存在差异，那么如果在这期间DB出现故障就会造成数据的丢失。为了解决这个问题，redo log就应运而生了。

###redo log、buffer pool、disk 三者之间的关系
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3fd72efaa25683be.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、redo log就是存储了数据被修改后的值。当我们提交一个事务时，InnoDB会先去把要修改的数据写入redo log 日志
2、然后再去修改buffer pool里面的真正数据页
3、通过 checkpoint机制写入到 disk。
关于checkpoint机制可以看看这篇文章 https://www.jianshu.com/p/f5cfc3f0158d








###redo log包括两部分：
####redo log buffer
是内存中的 重做日志缓冲 redo log buffer ，该部分日志是易失性的；
> SHOW VARIABLES LIKE 'innodb_log_buffer_size%'; 查看配置的redo log buffer大小，默认 16777216


####redo log file 
磁盘上的 重做日志文件 redo log file ，该部分日志是持久的

A、重做日志文件
①、innodb_log_group_home_dir参数指定的目录下有两个文件：ib_logfile0，ib_logfile1
②、该文件被称为：重做日志文件(redo log file)，记录Innodb存储引擎的事务日志。
③、例如：服务器意外宕机导致实例失败，Innodb存储引擎利用重做日志恢复到宕机前的状态，以此保证数据的完整性。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-45fafda106d1d390.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

B、日志文件组 group
每个Innodb存储引擎至少有1个重做日志文件组，每个组至少包含2个重做日志文件(ib_logfile0,ib_logfile1)。日志组中的文件大小是一致的，以循环的方式运行。文件1写满时，切换到文件2，文件2写满时，再次切换到文件1。就这样循环，闭环下去

日志文件参数：

>SHOW VARIABLES LIKE 'innodb_log_file_size' -- 重做日志文件的大小。
SHOW VARIABLES LIKE 'innodb_log_files_in_group' --  指定重做日志文件组中文件的数量，默认2
SHOW VARIABLES LIKE 'innodb_log_group_home_dir' -- innodb_log_group_home_dir 

对于发出的一条update语句写入到redo log时内部的详细过程如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-3aa8a3f8a9a8990e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


####redo log 从 log buffer到log file的刷新过程

为了确保每次日志都写入重做日志文件,在每次将重做日志缓冲写入重做日志文件后, InnoDB存储引擎都需要调用一次fsnc操作。由于重做日志文件打开并没有使用 O_DIRECT选项,因此重做日志缓冲先写入文件系统缓存。为了确保重做日志写入磁 盘,必须进行一次fsync操作。由于fsync的效率取决于磁盘的性能,因此磁盘的性能决定了事务提交的性能,也就是数据库的性能。

>logbuffer写入到logfile可以说需要经历两个步骤：1 写入操作系统缓存 2 进行fsync操作刷新到磁盘
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d0242330a397005b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


 InnoDB存储引擎允许用户手工设置非持久性的情况发生,以此提高数据库的性能。 即当事务提交时,日志不写入重做日志文件,而是等待一个时间周期后再执行 fsync操作(减少 fsync操作，减轻磁盘压力)。

由于并非强制在事务提交时进行一次 fsync操作,显然这可以显著提高数据库的性能。但是当数据库发生宕机时,由于部分日志未刷新到磁盘,因此会丢失最后一段时间的事务。 参数 innodb_fush_log_ attrxcommit用来控制重做日志刷新到磁盘的策略。

1、该参数 的默认值为1,表示事务提交时必须调用一次 fsync操作。还可以设置该参数的值为0和 2。
2、设置0 表示事务提交时不进行写入重做日志操作,这个操作仅在master thread中完成,而在 master thread中每1秒会进行一次重做日志文件的 fsync操作。(设置为1时 步骤1和步骤2都不会在事务提交时执行)
3、设置2 表示事务提交时将重做日志写入重做日志文件,但仅写入文件系统的缓存中,不进行 fsync操作。在这个设置下,当 MySQL数据库发生宕机而操作系统不发生宕机时,并不会导致事务的丢失。 而当操作系统宕机时,重启数据库后会丢失未从文件系统缓存/操作系统缓存中刷新到重做日志文件那部分事务。 （设置为2，事务提交时只会执行步骤1而不会执行步骤2）

关于这个innodb_flush_log_at_trx_commit参数可以看看这篇：
https://www.jianshu.com/p/77a28d67bac7






###总结redo log的作用
1、redolog 实现了ACID中的持久性。bufferpool中的dirtypage在断电时丢失（bp数据保存在内存），InnoDB在启动时，仍然会根据redolog中的记录完成数据恢复。

2、redolog的另一个作用是，通过延迟dirtypage的flush最小化磁盘的randomwrites（随机IO。（redolog会合并一段时间内TRX对某个page的修改）
