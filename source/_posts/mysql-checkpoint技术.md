---
title: mysql-checkpoint技术.md
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
title: mysql-checkpoint技术.md
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
>将buffer poll 脏页写入到磁盘中的技术就是 checkpoint技术

前面已经讲到了,缓冲池的设计目的为了协调CPU速度与磁盘速度的鸿沟。因此页的操作首先都是在缓冲池中完成的。如果一条DML语句,如 Update或 Delete改变了页 中的记录,那么此时页是脏的,即缓冲池中的页的版本要比磁盘的新。数据库需要将新版本的页从缓冲池刷新到磁盘。 

1、倘若每次一个页发生变化,就将新页的版本刷新到磁盘,那么这个开销是非常大的。若热点数据集中在某几个页中,那么数据库的性能将变得非常差。

2、同时,如果在从缓冲池将页的新版本刷新到磁盘时发生了宕机,那么数据就不能恢复了。为了避免发生数据丢失的问题,当前事务数据库系统普遍都采用了 Write Ahead Log 策略, **即当事务提交时,先写重做日志,再修改页。** 当由于发生宕机而导致数据丢失时,通过重做日志 redo log  来完成数据的恢复。这也是事务ACID中(Durability持久性)的要求。

思考下面的场景:
如果重做日志可以无限地增大,同时缓冲池也足够大,能够缓冲所有数据库的数据,那么是不需要将缓冲池中页的新版本刷新回磁盘。因为当发生宕机时,完全可以通过重做日志来恢复整个数据库系统中的数据到宕机发生的时刻。

但是这需要两个前提条件: 
1、缓冲池可以缓存数据库中所有的数据;
2、 重做日志可以无限增大。 
对于第一个前提条件,有经验的用户都知道,当数据库刚开始创建时,表中没有任何数据。缓冲池的确可以缓存所有的数据库文件。然而随着市场的推广,用户的增加, 产品越来越受到关注,使用量也越来越大。这时负责后台存储的数据库的容量必定会不断增大。当前3TB的 MySQL数据库已并不少见,但是3TB的内存却非常少见。目前 Oracle Exadata 旗舰数据库一体机也就只有2TB的内存。因此第一个假设对于生产环境 应用中的数据库是很难得到保证的。 
再来看第二个前提条件:重做日志可以无限增大。也许是可以的,但是这对成本的要求太高,同时不便于运维。DBA或SA不能知道什么时候重做日志是否已经接近于磁盘可使用空间的阈值,并且要让存储设备支持可动态扩展也是需要一定的技巧和设备支持的。  好的,即使上述两个条件都满足,那么还有一个情况需要考虑:宕机后数据库的恢复时间。当数据库运行了几个月甚至几年时,这时发生宕机,重新应用重做日志的时间会非常久,此时恢复的代价也会非常大。 


###因此 Checkpoint(检查点)技术的目的是解决以下几个问题: 

1、缩短数据库的恢复时间;

当数据库发生宕机时,数据库不需要重做所有的日志,因为 Checkpoint之前的页都已经刷新回磁盘。故数据库只需对 Checkpoint后的重做日志进行恢复。这样就大大缩短了恢复的时间。（只需要对最近的一个checkpoint之后的redo log进行恢复，而不是对所有的redo log）


2、缓冲池不够用时,将脏页刷新到磁盘; 

此外,当缓冲池不够用时,根据LRU算法会溢出最近最少使用的页,若此页为脏页,那么需要强制执行Checkpoint,将脏页也就是页的新版本刷回磁盘。

3、重做日志不可用时,刷新脏页。 

重做日志出现不可用的情况是因为当前事务数据库系统对重做日志的设计都是循环使用的,并不是让其无限增大的,这从成本及管理上都是比较困难的。重做日志可以被重用的部分是指这些重做日志已经不再需要（这部分的redo log中的数据已经checkpoint到磁盘中去了，所以就不再需要了）,即当数据库发生宕机时,数据库恢复操作不需要这部分的重做日志,因此这部分就可以被覆盖重用。若此时重做日志还需要使用,那么必须强制产生 Checkpoint,将缓冲池中的页至少刷新到当前重做日志的位置。 （redo log 空间满了，促进释放 redo log 空间）



###查看Checkpoint的标记位置
对于 InnoDB存储引擎而言,其是通过LN(Log Sequence Number)来标记版本 的。而LSN是8字节的数字,其单位是字节。每个页有LSN,重做日志中也有LSN, Checkpoint也有LSN.可以通过命令 SHOW ENGINE INNODB STATUS来观察:

![image.png](https://upload-images.jianshu.io/upload_images/13965490-4059ef64eacdd734.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###Checkpoint发生的时间、条件及脏页的选择
在 InnoDB存储引擎中, Checkpoint发生的时间、条件及脏页的选择等都非常复杂。

而 Checkpoint所做的事情无外乎是将缓冲池中的脏页刷回到磁盘。不同之处在于每次刷新多少页到磁盘,每次从哪里取脏页,以及什么时间触发 Checkpoint。


###两种Checkpoint
在 InnoDB存储 引擎内部,有两种 Checkpoint,分别为: 1、Sharp Checkpoint 2、 Fuzzy Checkpoint 

####Sharp Checkpoint
Sharp Checkpoint 发生在数据库关闭时将所有的脏页都刷新回磁盘,这是默认的工作方式,即参数innodb_fast_shutdown=1 （所有的脏页）
####Fuzzy Checkpoint
但是若数据库在运行时也使用 Sharp Checkpoint,那么数据库的可用性就会受到很大的影响。故在 InnoDB存储引擎内部使用 Fuzzy Checkpoint进行页的刷新,即只刷新一 部分脏页,而不是刷新所有的脏页回磁盘。（一部分脏页）

这里笔者进行了概括,在 InnoDB存储引擎中可能发生如下几种情况的 Fuzzy Checkpoint: 


①、Master Thread Checkpoint 
对于 Master Thread 中发生的 Checkpoint,差不多以每秒或每十秒的速度从缓冲池的脏页列表中刷新一定比例的页回 磁盘。这个过程是异步的,即此时 InnoDB存储引擎可以进行其他的操作,用户查询线程不会阻塞。 

②、FLUSH LRU LIST Checkpoint 

FLUSH LRU_LIST Checkpoint 是因为InnoDB存储引擎需要保证LRU列表中需要有差不多100个空闲页可供使用。在 InnoDB11.1.x版本之前,需要检查LRU列表中是否有足够的可用空间操作发生在用户查询线程中,显然这会阻塞用户的查询操作。倘若没有100个可用空闲页,那么 InnoDB存储引擎会将LRU列表尾端的页移除。如果这些页中有脏页,那么需要进行Checkpoint,而这些页是来自LRU列表的,因此称为 FLUSH LRU LIST Checkpoint. 
而从 MySQL5.6版本,也就是 InnoDB1.2.x版本开始,这个检查被放在了一个单独的Page Cleaner线程中进行,并且用户可以通过参数 innodb_lru_scan_depth 控制 `LRU列表`中可用页的数量,该值默认为1024,如:

>SHOW VARIABLES LIKE '%innodb_lru_scan_depth%' -- 1024


(bf的LRU列表没有足够空间引发的checkpoint： 之前版本的mysql将LRU LIST Checkpoint 放在用户查询线程中会导致一定的阻塞，后续版本将之拎出来放在 Page Cleaner线程，LRU列表中可用空闲页少于innodb_lru_scan_depth 1024个页时 Page Cleaner线程会将LRU列表尾端的页移除，如果这些页中有脏页,那么需要进行FLUSH LRU LIST Checkpoint  )

③、Async/Sync Flush Checkpoint 

Async/Sync Flush Checkpoint指的是重做日志文件不可用的情况,这时需要强制将一些页刷新回磁盘,而此时脏页是从脏页列表中选取的。若将已经写入到重做日志的LSN 记为 redo_lsn ,将已经刷新回磁盘最新页的LSN记为 checkpoint_lsn ,则可定义: 
checkpoint_age=  redo_lsn -  checkpoint_lsn （checkpoint_age代表 redo log + bp中的脏页 = 需要写入磁盘的页总量）
再定义以下的变量: 
async_water_mark=75%* total_redo_ log_file_size 
sync_water_mark = 90% * total_redo_log_file_size 

若每个重做日志文件的大小为1GB,并且定义了两个重做日志文件,则重做日志文件的总大小为2GB。那么 async_water_mark=1.5gb,sync_water_mark=1.8gb.则:

1、当 checkpoint_age<async_water_mark时,不需要刷新任何脏页到磁盘; 
2、当 async_water_mark<checkpoint_age<sync_water_mark时触发 Async Flush,从 Flush 列表中刷新足够的脏页回磁盘,使得刷新后满足 checkpoint_age<sync_water_mark; 
3、 checkpoint_age>sync_water_mark 这种情况一般很少发生,除非设置的重做日志文件太小,并且在进行类似 LOAD DATA的 BULK INSERT操作此时触 发 Sync Flush操作,从 Flush列表中刷新足够的脏页回磁盘,使得刷新后满足 checkpoint_age<async_water_mark. 可见, Async/Sync Flush Checkpoint是为了保证重做日志的循环使用的可用性。在 InnoDB1.2.x版本之前, Async Flush Checkpoint会阻塞发现问题的用户查询线程,而 Sync Flush Checkpoint会阻塞所有的用户查询线程,并且等待脏页刷新完成。从 InnoDB 1.2.x版本开始也就是5.6版本,这部分的刷新操作同样放入到了单独的Page Cleaner Thread中,故不会阻塞用户查询线程。 MySQL官方版本并不能查看刷新页是从 Flush列表中还是从LRU列表中进行 Checkpoint的,也不知道因为重做日志而产生的 Async/Sync Flush的次数。但是InnoSQL 版本提供了方法,可以通过命令 SHOW ENGINE INNODB STATUS来观察,如:


(redo log file 满了引发的checkpoin）

④、Dirty Page too much Checkpoint 

最后一种 Checkpoint的情况是 Dirty Page too much,即脏页的数量太多,导致 InnoDB存储引擎强制进行 Checkpoint。其目的总的来说还是为了保证缓冲池中有足够可用的页。其可由参数 innodb_maxdirty pages pct控制:
>SHOW VARIABLES LIKE '%innodb_max_dirty_pages_pct%' --75

innodb_max_dirty_pages_pct 值为75表示,当缓冲池中脏页的数量占据75%时,强制进行 Checkpoint,刷新一部分的脏页到磁盘。在 InnoDB1.0.版本之前,该参数默认 值为90,之后的版本都为75。

(bp中脏页占比超过innodb_max_dirty_pages_pct 会触发一个Dirty Page too much Checkpoint )


####总结下，发生checkpoint的时机
1、主线程每秒或每10秒触发
2、mysql停止时触发全量的脏页回收checkpoint
3、buffer pool 中LRU列表剩余空间低于 innodb_lru_scan_depth，移除列表尾端页时，若是脏页则触发checkpoint
4、redo log file 不可用，剩余容量少于一定值后触发 checkpoint。
5、buffer pool中脏页超过百分值 innodb_max_dirty_pages_pct 触发checkpoint，保证bp中有足够多可用页
