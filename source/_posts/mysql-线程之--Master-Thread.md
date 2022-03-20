---
title: mysql-线程之--Master-Thread.md
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
title: mysql-线程之--Master-Thread.md
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
 InnoDB存储引擎的主要工作都是在一个单独的后台线 程 Master Thread中完成的,这一节将具体解释该线程的具体实现及该线程可能存在 的问题。

###InnoDB1.0.x版本之前的 Master Thread 

Master Thread具有最高的线程优先级别。

其内部由多个循环(loop)组成:
1、主循环 (loop)
2、后台循环( backgroup loop)
3、刷新循环(lush loop)
4、暂停循环(suspend loop) 

>Master Thread会根据数据库运行的状态在 loop、 background loop、flush loop和 suspend loop中进行切换。  

####Loop主循环功能介绍
Loop被称为主循环,因为大多数的操作是在这个循环中,其中有两大部分的操 作：  每秒钟的操作和每10秒的操作。

loop循环通过 thread sleep来实现,这意味着所谓的每秒一次或每10秒 一次的操作是不精确的。在负载很大的情况下可能会有延迟(delay),只能说大概在这个频率下。

当然, InnoDB源代码中还通过了其他的方法来尽量保证这个频率。

###每秒一次的操作 
①、每秒刷新redo log buffer到redo log file机制 ,即使这个事务还没有提交(总是) `重要`

>即使某个事务还没有提交, InnoDB存储引擎仍然每秒会将重做日志缓冲中的内容刷新到重做日志文件。这一点是必须要知道的,因为这可以很好地解释为什么再大的事务提交(commit)的时间也是很短的。

当然，还有其它条件被满足后也会将redo log buffer刷新到redo log file，
innodb_flush_log_at_trx_commit 被设置为0或2时，会在事务commit的时候也会触发。具体看看这篇https://www.jianshu.com/p/77a28d67bac7 

②、合并插入缓冲（insert buffer）(可能); 
合并插入缓冲(Insert Buffer)并不是每秒都会发生的。 InnoDB存储引擎会判断当前一秒内发生的IO次数是否小于5次,如果小于5次, InnoDB认为当前的IO压力很小,可以执行合并插入缓冲的操作。

③、至多刷新100个 InnoDB的缓冲池中的脏页到磁盘(可能); 
刷新100个脏页也不是每秒都会发生的。 InnoDB存储引擎通过判断当前缓冲池中脏页的比例(buf_get_modified_ratio_pct)是否超过了配置文件中innodb_max_dirty_pages_pct这个参数(默认为90,代表90%，后来的版本中调整成75%),如果超过了这个阈值, InnoDB存储引擎认为需要做磁盘同步的操作,将100个脏页写入磁盘中。脏页的刷新机制checkpoint 可以看看这篇 https://www.jianshu.com/p/f5cfc3f0158d


④、如果当前没有用户活动(no user activity),则切换到 background loop(可能) 


###每10秒一次的操作
①、刷新100个脏页到磁盘(可能的情况下) 
在以上的过程中, InnoDB存储引擎会先判断过去10秒之内磁盘的IO操作是否小于200次,如果是, InnoDB存储引擎认为当前有足够的磁盘IO操作能力,因此将100 个脏页刷新到磁盘。因为有空闲的IO磁盘利用率可以去做这个刷新脏页操作。没有空间就交给第5步去刷新脏页

②、合并至多5个插入缓冲(总是); 
接着, InnoDB存储引擎会合并插入缓冲。不同于每秒一次操作时可能发生的合并插入缓冲操作,这次的合并插入缓冲操作总会在这个阶段进行。

③、将日志缓冲刷新到磁盘(总是); 
之后, InnoDB存储引擎会再进行一次将日志缓冲刷新到磁盘的操作。这和每秒一次时发生的操作是一样的。

④、删除无用的Undo页(总是); 
接着 InnoDB存储引擎会进行一步执行 full purge操作,即删除无用的Undo 页。对表进行update、 delete这类操作时,原先的行被标记为删除,但是因为一致性读(consistent read)的关系,需要保留这些行版本的信息。但是在 full purge过程中, InnoDB存储引擎会判断当前事务系统中已被标记删除的行是否可以删除,比如有时候可能还有查询操作需要读取之前版本的undo信息,如果可以删除, InnoDB会立即将其删除。

从源代码中可以发现, InnoDB存储引擎在执行 full purge操作时,每次最多尝试回收20 个undo页。

⑤、刷新100个或者10个脏页到磁盘(总是) 
 然后, InnoDB存储引擎会判断缓冲池中脏页的比例(buf_get_modified_ratio_pct), 如果有超过70%的脏页,则刷新100个脏页到磁盘,如果脏页的比例小于70%,则只需 刷新10%的脏页到磁盘。

####background loop 后台循环功能介绍
接着来看 background loop,若当前没有用户活动(数据库空闲时,is idle )或者数据库关闭 ( shutdown),就会切换到这个循环。
 background loop会执行以下操作: 

1、删除无用的Undo页(总是) 
2、合并20个插入缓冲(总是) 
3、跳回到主循环(总是); 
4、不断刷新100个页直到符合 buf_get_modified_ratio_pct < innodb_max_dirty_pages_pct 条件(可能,跳转到flush loop中完成) 

若 flush loop中也没有什么事情可以做了, InnoDB存储引擎会切换到 suspend_loop,将 Master Thread挂起,等待事件的发生。若用户启用(enable)了InnoDB存储 引擎,却没有使用任何 InnoDB存储引擎的表,那么Master Thread总是处于挂起的 状态。 最后, Master Thread完整的伪代码如下:

![image.png](https://upload-images.jianshu.io/upload_images/13965490-20cd0b4cef8e8093.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###InnoDB1.0.x版本的 Master Thread

######新增innodb_io_capacity参数
在Innodb 1.0.x版本之前，InnoDB存储引擎最大只会每秒只会刷新100个脏页到磁盘、合并20个插入缓冲。硬编码实现方式限制了 磁盘IO吞吐量和写入性能。所以之后提供了一个可以直接配置这个阈值的方式，那么就是  `innodb_io_capacity` 参数。 用心记下 innodb io  capacity （城市）


InnoDB Plugin(从 InnoDB1.0.x版本开始)提供了参数  innodb_io_capacity，将配置innodb的每秒刷新脏页数、合并插入缓冲数交给用户灵活配置

>该参数影响两个方面，规则如下: 
1、合并插入缓冲时,每秒合并插入缓冲的数量为 innodb_io_capacity值的5%，默认就是 200*5%=10 
2、在从缓冲区刷新脏页时（checkpoint）,每秒刷新脏页的数量就等于innodb_io_capacity的值，默认200

适当调高innodb_io_capacity可以提高IO性能


###### innodb_max_dirty_pages_pct 默认值的问题
在1.0.x 版本之前,该值的默认为90,意味着脏页占缓冲池的90%但是该值“太大”了,因为 InnoDB存储引擎在每秒刷新缓冲池和 flush loop时会判断这个值,如果该值大于innodb_max_dirty_pages_pct,才刷新100个脏页,如果有很大的内存,或者数据库服务器的压力很大,这时刷新脏页的速度反而会降低。

同样,在数据库的恢复阶段可能需要更多的时间。 在很多论坛上都有对这个问题的讨论,有人甚至将这个值调到了20或10,然后测试发现性能会有所提高,但是将 innodb_max_dirty_pages_pct调到20或10会增加磁盘 的压力,系统的负担还是会有所增加的。 Google在这个问题上进行了测试,证明20并 不是一个最优值。而从 InnoDB1.0.x版本开始, innodbmax_dirtypagespct默认值变为了75,和 Google测试的80比较接近。这样既可以加快刷新脏页的频率,又能保证了 磁盘IO的负载。

~~~
SHOW VARIABLES LIKE '%innodb_max_dirty_pages_pct%'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-28ba2f2dc97361b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>innodb_max_dirty_pages_pct 表示脏页占buffer poll的比值，决定是否触发每秒刷新脏页,设置大了会导致脏页积累过多、刷新脏页的速度降低。设置小了又会导致频繁进行脏页的刷新、磁盘IO负担大。

######新增innodb_adaptive_flushing参数

InnoDB1.0.x版本带来的另一个参数是 innodb_adaptive_flushing(自应地刷新), 该值影响每秒刷新脏页的数量。原来的刷新规则是:脏页在缓冲池所占的比例小于 innodb_dirty_pages_pct 时,不刷新脏页;大于 innodb_dirty_pages_pct时,刷新100个脏页。随着innodb_adaptive_flushing 参数的引入, InnoDB存储引擎会通过一个名为 buf_flush_get_desired_flush_rate 的函数来判断需要刷新脏页最合适的数量。粗略地翻阅源代码后发现 buf_flush_get_desired_flush_rate 通过判断产生重做日志(redo log)的速度来决定最合适的刷新脏页数量。

>因此,当脏页的比例小于 innodb_adaptive_flushing 时,也会刷新一定量的脏页。通过产生重做日志(redo log)的速度来`自适应的刷新` 

~~~
SHOW VARIABLES LIKE '%innodb_adaptive_flushing%' -- 默认ON 开启
~~~

######新增innodb_purge_batch_size参数
之前每次进行 full purge操作时,最多回收20个undo 页,从 InnoDB1.0.x版本开始引入了参数 innodb_purge_batch_size,该参数可以控制每次full purge回收的Undo页的数量。该参数的默认值为20,并可以动态地对其进行修改,具体如下:
~~~
SHOW VARIABLES LIKE '%innodb_purge_batch_size%'
SET GLOBAL innodb_purge_batch_size = 400
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f74da1ab2892523f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###InnoDB1.2.x版本的 Master Thread

InnoDB1.2.x版本的 Master Thread 在 InnoDB1.2.x版本中再次对 Master Thread进行了优化,由此也可以看出 Master Thread对性能所起到的关键作用。在 InnoDB1.2.x版本中, Master Thread的伪代码如下: 

>if InnoDB is idle 
srv_master_do_idle_tasks();
else 
srv_master_do_active_tasks();
 
其中 srv_master_do_idle_tasks 就是之前版本中每10秒的操作,srv_master_do_active_tasks()处理的是之前每秒中的操作。

1、对于刷新脏页的操作,从 Master Thread 线程分离到一个单独的 Page Cleaner Thread,从而减轻了 Master Thread的工作,同时进一步提高了系统的并发性。 

~~~
PageCleanerThread()
{
    
    //刷新缓冲池中的脏页到磁盘（可能）：
        if(buf_get_modified_ratio_pct>buf_max_dirty_pages_pct)
            刷新脏页个数：100%*innodb_io_capacity
        if(buf_get_modified_ratio_pct<buf_max_dirty_pages_pct)
            刷新脏页个数：10%*innodb_io_capacity
}
~~~
