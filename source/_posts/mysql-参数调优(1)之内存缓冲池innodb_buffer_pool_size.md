---
title: mysql-参数调优(1)之内存缓冲池innodb_buffer_pool_size.md
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
title: mysql-参数调优(1)之内存缓冲池innodb_buffer_pool_size.md
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
内存的大小是最能直接反映数据库的性能。InnoDB存储引擎既缓存数据，又缓存索引，并且将它们缓存于一个很大的`缓冲池`中，即InnoDB Buffer Pool。因此，内存的大小直接影响了数据库的性能性能测试。

Percona公司的CTO Vadin对此做了一次测试，以此反映内存的重要性，结果如下图所示：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-852723f935b386ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



在上述测试中，数据和索引总大小为18GB，然后将缓冲池的大小分别设为2GB、4GB、6GB、8GB、10GB、12GB、14GB、16GB、18GB、20GB、22GB，再进行sysbench的测试可以发现：随着缓冲池的增大，测试结果TPS(Transaction Per Second)会线性增长。

当缓冲池增大到20GB和2GB时，数据库的性能有了极大的提高，因为这时缓冲池的大小已经大于数据文件本身的大小，所有对数据文件的操作都可以在内存中进行。因此这时的性能应该是最优的，`再调大缓冲池并不能再提高数据库的性能`（再将参数调大就回去使用swap空间了）。所以，应该在开发应用前预估“活跃数据库的大小”是多少，并以此确定数据库服务器内存的大小。但是这样的预估通常是不容易达到准确的。

> 经过以上实验，可以看出`innodb_buffer_pool_size`是mysql参数调优中首当其冲的最重要的一个。增大它能够让mysql的性能得到很大提升！！！

**专用的mysql服务器**
网上很多说innodb_buffer_pool_size为系统的70%，这是错的！因为你真的设了70%你的swap空间（虚拟内存）会被挤压性能反而会变低，你不要忘了你还有os，上面还可能有监控agent端。一旦swap空间被挤压后你的mysql反面严重拖慢读写。

此处强烈建议设成内存的20%-65%间（独立的mysql服务器），为什么有一个20%呢？对于<4gb的mysql用服务器来说按照20%系统内存来设置。由于我们是128gb的内存，此处我建议使用72G(56%),如果内存超过128gb，一般我们会把pool instance设成16个，每个开启10g左右 buffer_pool_size，对于256gb内存的服务器来说我们可以这样设。


**共享服务器**
如果你的MySQL服务器与其它应用共享资源，那么上面的经验就不那么适用了。在这样的环境下，设置一个对的数字有点难度。对此我们可以使用`缓存池命中率` 和  `总innodb表文件大小`来进行判断。

**判断当前数据库内存是否达到瓶颈，从而调整缓存池大小**
如何判断当前数据库的内存是否已经达到瓶颈了呢？可以通过查看当前服务器的状态，比较物理磁盘的读取和内存读取的比例来判断缓冲池的命中率，即通过 `缓存池命中率`来判断，我们可以这样得到相关参数：

~~~
SHOW GLOBAL STATUS LIKE 'innodb%read%'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-717cdfeab9f2c9c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上述参数的具体含义如下所示：
1、Innodb_buffer_pool_reads 表示InnoDB缓冲池无法满足的请求，从而到物理磁盘读取页的次数
2、Innodb_buffer_pool_read_ahead 预读次数
3、Innodb_buffer_pool_read_ahead_evicted 预读的页
4、Innodb_buffer_pool_read_requests 从缓冲池中读取页的次数
5、Innodb_data_read   表示Innodb启动后，从物理磁盘上读取的字节数总和。
6、Innodb_data_reads 表示Innodb启动后，物理磁盘上发起的IO请求次数，每次读取肯能需要读多个页。


**缓存池命中率计算方法**
x =  缓冲池读次数/( 缓冲池读次数+ 预读数 + 物理磁盘读次数)
= Innodb_buffer_pool_read_requests /(Innodb_buffer_pool_read_requests +Innodb_buffer_pool_read_ahead + Innodb_buffer_pool_reads )
= 0.9665 = 96%

可以直接使用这条sql计算缓冲池命中率
~~~
SELECT
	( SELECT variable_value FROM PERFORMANCE_SCHEMA.global_status WHERE variable_name = 'Innodb_buffer_pool_read_requests' ) / ( SELECT SUM( variable_value ) FROM PERFORMANCE_SCHEMA.global_status WHERE variable_name IN ( 'Innodb_buffer_pool_read_requests', 'Innodb_buffer_pool_read_ahead', 'Innodb_buffer_pool_reads' ) )
~~~

`通常 InnoDB存储引擎的缓冲池的命中率不应该小于99%`，所以现在可以调大innodb_buffer_pool_size参数。（我本机内存是8G，我调整到5G，6G的样子只能到98%。无法达到99%，mysql占用内存899M）。在线设置的sql：
~~~
SET GLOBAL innodb_buffer_pool_size = 6442450944 -- 6G
~~~

如果命中率太低，则应考虑扩充内存，增加innodb_buffer_pool_size的值。即使缓冲池的大小已经大于数据库文件的大小，这也并不意味着没有磁盘操作。数据库的缓冲池只是一个用来存放热点的区域，后台的线程还负责将脏页异步地写入到磁盘。此外，每次事务提交时还需要将日志写入重做日志文件。


物理磁盘上平均每次读取字节数=  Innodb_data_read / Innodb_data_reads
~~~
SELECT variable_value FROM PERFORMANCE_SCHEMA.global_status WHERE variable_name = 'Innodb_data_read' 
~~~


**innodb表占用总空间**
可以通过下列语句查询得到所有innodb表的数据和索引的总占用空间。可以看到我本机的innodb大小是 1.31G，那么我们至多可以将innodb_buffer_pool_size设置为1.31G了，不过大多数情况你不需要那样做，你只需要缓存你经常使用的数据集。
~~~
SELECT engine,
  count(*) as TABLES,
  concat(round(sum(table_rows)/1000000,2),'M') rows,
  concat(round(sum(data_length)/(1024*1024*1024),2),'G') DATA,
  concat(round(sum(index_length)/(1024*1024*1024),2),'G') idx,
  concat(round(sum(data_length+index_length)/(1024*1024*1024),2),'G') total_size,
  round(sum(index_length)/sum(data_length),2) idxfrac
FROM information_schema.TABLES
WHERE table_schema not in ('mysql', 'performance_schema', 'information_schema')
GROUP BY engine
ORDER BY sum(data_length+index_length) DESC LIMIT 10;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-076f0f3e73a72b59.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**调整方式**

在线修改，5.7以后可以。但是要注意修改innodb_buffer_pool_size 可能造成`业务波动`。但也最好选择业务低峰期和没有大事务操作时候进行，同时要修改MySQL配置文件，防止重启后恢复到原来的值。
~~~
SET GLOBAL innodb_buffer_pool_size = 2147483648  #2G
~~~

配置文件方式，修改后重启
~~~
[mysqld]
innodb_buffer_pool_size = 2147483648  #设置2G
innodb_buffer_pool_size = 2G  #设置2G
innodb_buffer_pool_size = 500M  #设置500M
~~~


**innodb_buffer_pool_instances**
还有一个和buffer pool 相关的参数看这里 https://www.jianshu.com/p/f84fe0979cdf
