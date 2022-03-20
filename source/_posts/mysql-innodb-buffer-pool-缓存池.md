---
title: mysql-innodb-buffer-pool-缓存池.md
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
title: mysql-innodb-buffer-pool-缓存池.md
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
 InnoDB存储引擎是基于磁盘存储的,并将其中的记录按照页的方式进行管理。因此可将其视为基于磁盘的数据库系统。（Disk-base Database）。在数据库系统中，由于CPU速度与磁盘速度之间的鸿沟，基于磁盘的数据库系统通常使用缓冲池技术来提高数据库整体性能。
 
>缓冲池的大小直接影响着数据库的整体性能。应该是mysql数据库参数调优中最优先考虑的！

 缓冲池简单来说就是一块内存区域，通过内存的速度来弥补磁盘速度较慢对数据库性能的影响。bp分别参与对读和写的内部机制

1、在数据库中进行读取页的操作，首先将从磁盘中读到的页（redo log）放在缓冲池中，这个过程称为`FIX`在缓冲池中。在下一次在读取相同页时，首先判断该页是否在缓冲池中，如果在，称该页在缓冲池中被命中，直接读取该页，否则，读取磁盘上的页。

 2、对数据库中页的修改操作，则首先修改在缓冲池中的页，然后再以一定的频率刷新到磁盘上。这里要注意，页从缓冲池刷新回磁盘的操作并不是在每次页发生更新时触发，而是通过一种称为 `CheckPoint机制 ` 刷新回磁盘。同样这也是为了提高数据库的整体性能。






###buffer poll的结构

![image.png](https://upload-images.jianshu.io/upload_images/13965490-bfaf362df9e439b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


1、data page
2、index page
3、insert buffer  
4、lock info
5、自适应hash索引
6、数据字典信息

当然除了buffer poll时内存对象，还有redo log_buffer、额外内存池innodb_addional_mem_pool_size


###多个缓冲池实例
 从InnoDB 1.0.x版本开始，允许有多个缓冲池实例。每个页根据哈希值平均分配到不同的缓冲池实例中。



###LRU List、Free List 和 Flush List 缓存池内存管理算法

>维护热点数据，淘汰冷点数据

####LRU（Latest Recent Used，最近最少使用）算法：

最频繁使用的页在LRU列表的前端，而最少使用的页在LRU列表的尾端。当缓冲池剩余空间不能容纳最新读取到的页时，将首先去释放LRU列表的尾端最少使用的页。
但事实上，innodb对LRU算法有它的优化，加入了 midpoint位置。新读取到的页，虽然是最新访问的页，但并不直接放到LRU列表的首部，而是放到midpoint位置这个算法成为 midpoint insertion strategy。默认情况在LRU列表的5/8处。midpoint位置可以由innodb_old_blocks_pct参数控制。
~~~
SHOW VARIABLES LIKE '%innodb_old_blocks_pct%'
~~~
默认值 37， 即在LRU列表的37%

midpoint之前的列表为`new列表`，之后为`old列表`。new列表中的页都是最为活跃的热点数据。
那为什么不直接采用朴素的LRU算法，直接将新读取的页放到列表首部？原因是存在某些对索引或数据的扫描sql，这种sql会访问表中的许多页，甚至是全部的页，而这些页通常来说只在在这次查询中使用，并不是活跃的热点数据，直接将这么多的页插入到首部会导致直接的热点数据全部下移。甚至是直接被挤出LRU列表。导致之后的热点数据查询全都从磁盘降低速度。如果预估自己活跃的数据不止63%，那么在执行sql的前，还可以通过下调整这个参数来减少热点页被刷出的概率：
~~~
SET GLOBAL innodb_old_block_pct=20;
~~~
>默认的缓冲中的页在第一次被读取时（也就是命中缓存）会被移动到新页子表头部，意味着其会长期待在缓冲池中不会被淘汰。这样就会存在一个问题，一次表扫描（比如使用mysqldump或者没有条件的select查询）可能会将大量数据放入缓存中，并淘汰相应数量的旧数据，但是可能这些数据只使用一次，后面不再使用；同样地，因为MySQL自动触发的read-ahead也会在下一次访问该页时被放入新页子表头部。这些情形会将本应会被频繁使用的页移动到旧页子表中。
所以MySQL采用如下方式避免上面的问题，新读取的页会放入缓冲池中点，也即默认情况下所有的新读取的页都会被插入到尾部开始的3/8位置处。`在后面的第一次命中（被访问时）的页会被移动到列表的头部`。因此，那些读入缓存但是后面从来不会被访问的页也从不会被放入列表的头部，也就会在后面被从缓冲池淘汰。



      


![2020-06-16_113926.png](https://upload-images.jianshu.io/upload_images/13965490-57597c3d72895ea5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





MySQL改进的LRU算法将那些被频繁查询的页放在表头部的新页子表中，表尾的旧页子表则放那些较少使用的页，这些页也是淘汰的候选页。

默认配置下，算法操作如下：

1、 3/8的列表划分为尾部的旧页子表，存放那些可以淘汰的旧页。

2、列表中点(midpoint，注意这里虽然说是中点，但是不一定是严格的中间位置，比如默认配置下，该位置从表头计算为列表5/8的位置)是新页子表和旧页子表的边界。

3、当 InnoDB从磁盘读一页数据并放入缓冲池中时，它会将此页插入到列表的`中间位置 midpoint`（也就是旧页子表的头部）。发生读页一般是因为用户查询数据，或者InnoDB自动触发的read-ahead操作。

4、   读取旧页子表中的数据会让该页变新（年轻，young），并将其移动到缓冲池的头部（也就是新页子表的头部）。`如果是因为用户查询读造成该页被读取，则该页会立即被标识为年轻，并直接插入到列表头部`。如果该页因为read-ahead被读取，则首次读取该页并放入缓冲池时不会将该页放入新页列表头部，而是放入列表中点，需要再次读取才能使该页被标识为年轻状态。（该页可能一直没有被标识为年轻状态直到被淘汰）。

5、MySQL通过参数`innodb_old_blocks_pct`来控制旧页子表占整个缓冲池列表的比例，默认为37，也就是上面说的3/8。


6、read-ahead（预读）、或者表、索引扫描都会造成类似的`缓冲池扰动`。在这些情景下，页通常会被读取（命中）若干次，然后从此不再访问。为此MySQL提供了配置参数`innodb_old_blocks_time`用来指定该页在放入缓冲池后第一次读之后一定时间内（时间窗口，单位毫秒,milliseconds）读取不会被标识为年轻，也就是不会被移动到列表头部。参数`innodb_old_blocks_time`的默认值是1000，增大这个参数将会造成更多的页会更快的从缓冲池中被淘汰。



###正常情况下，dirtypage什么时候flush到disk上？

1、redo log是一个环(ring)结构，当redo 空间占满时，将会将部分dirtypage flush到disk上，然后释放部分redolog。这种情况可以通过Innodb_log_wait(SHOWGLOBALSTATUS)观察，情况发生该计数器会自增一次。

2、当需要在bp分配一个page，但是已经满了，并且所有的page都是dirty的（否则可以释放不dirty的page），通常是不会发生的。这时候必须flush dirty pages to disk。这种情况将会记录到Innodb_buffer_pool_wait_free中。一般地，可以可以通过启动参数innodb_max_dirty_pages_pct控制这种情况，当bufferpool中的dirtypage到达这个比例的时候，将会强制设定一个checkpoint，并把dirtypageflush到disk中。

3、检测到系统空闲的时候，会flush，每次64pages。

涉及的InnoDB配置参数：innodb_flush_log_at_trx_commit、innodb_max_dirty_pages_pct；状态参数：Innodb_log_wait、Innodb_buffer_pool_wait_free。

