---
title: mysql-关键特性之（一）-Insert-Buffer-插入缓冲.md
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
title: mysql-关键特性之（一）-Insert-Buffer-插入缓冲.md
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
Insert Buffer可能是 InnoDB存储引擎关键特性中最令人激动与兴奋的一个功能。不过这个名字可能会让人认为插人缓冲是缓冲池中的一个组成部分。其实不然, InnoDB缓冲池中有 InsertBuffer 信息固然不错,但是Insertbuffer和数据页一样,也是物理页的一 个组成部分。

 在 InnoDB存储引擎中,主键是行唯一的标识符。通常应用程序中行记录的插入顺序是按照主键递增的顺序进行插入的。因此,插入聚集索引(Primary Key)一般是顺序的,不需要磁盘的随机读取。

比如按下列SQL定义表: 
CREATE TABLE t (
a INT AUTO_INCREMENT, 
b VARCHAR(30), 
PRIMARY KEY(a),
key(b)
);
其中a列是自增长的,若对a列插入NULL值,则由于其具有AUTO_INCREMENT 属性,其值会自动增长。同时页中的行记录按a的值进行顺序存放。在一般情况下,不需要随机读取另一个页中的记录。因此,对于这类情况下的插入操作,速度是非常快的。

>注意并不是所有的主键插入都是顺序的。若主键类是UUID这样的类,那么 插入和辅助索引一样,同样是随机的。即使主键是自增类型,但是插入的是指 定的值,而不是NULL值,那么同样可能导致插入并非连续的情况。 

但是不可能每张表上只有一个聚集索引,更多情况下,一张表上有多个非聚集的辅助索引(secondary index) 比如,用户需要按照b这个字段进行查找,并且b这个字段不是唯一的,即表是按如下的SQL语句定义的:
 CREATE TABLE t( a INT AUTO _INCREMENT, b VARCHAR(30), PRIMARY KEY (a), key (b) ; 
在这样的情况下产生了一个非聚集的且不是唯一的索引。在进行插入操作时,数据页的存放还是按主键a进行顺序存放的,但是对于非聚集索引叶子节点的插人不再是顺序的了,这时就需要离散地访问非聚集索引页,由于随机读取的存在而导致了插入操作性能下降。当然这并不是这个b字段上索引的错误,而是因为B+树的特性决定了非聚集索引插入的离散性。 需要注意的是,在某些情况下,辅助索引的插入依然是顺序的,或者说是比较顺序 的,比如用户购买表中的时间字段。在通常情况下,用户购买时间是一个辅助索引,用 来根据时间条件进行查询。但是在插入时却是根据时间的递增而插入的,因此插入也是 “较为”顺序的。

InnoDB存储引擎开创性地设计了 Insert Buffer,对于非聚集索引的插入或更新操作, 不是每一次直接插入到索引页中,而是先判断插入的非聚集索引页是否在缓冲池中,若在,则直接插人;

若不在,则先放入到一个 Insert Buffer对象中,好似欺骗。数据库这个非聚集的索引已经插到叶子节点,而实际并没有,只是存放在另一个位置。然后再以 一定的频率和情况进行 Insert Buffer和辅助索引页子节点的 merge(合并)操作,这时通 常能将多个插入合并到一个操作中(因为在一个索引页中),这就大大提高了对于非聚 集索引插入的性能。(提升io效率，减少io次数) 

>然而 Insert Buffer 的使用需要同时满足以下两个条件,这也是设计高性能数据库需要考虑的地方: 
1、索引是辅助索引(secondary index); 
2、索引不是唯一(unique)的。 


当满足以上两个条件时, InnoDB存储引擎会使用 Insert Buffer,这样就能提高插入操作的性能了。不过考虑这样一种情况: 应用程序进行大量的插入操作,这些都涉及了不唯一的非聚集索引,也就是使用了 Insert Buffer.若此时 MySQL数据库发生了宕机, 这时势必有大量的 Insert Buffer并没有合并到实际的非聚集索引中去。因此这时恢复可能需要很长的时间,在极端情况下甚至需要几个小时。

辅助索引不能是唯一的,因为在插入缓冲时,数据库并不去查找索引页来判断插入的记录的唯一性。如果去查找肯定又会有离散读取的情况发生,从而导致 Insert Buffer 失去了意义。 用户可以通过命令 SHOW ENGINE INNODB STATUS来查看插入缓冲的信息: 
mysql>SHOW ENGINE INNODB STATUS\G; ★1.row

Type: InnoDB Name: Status: == 100727 22: 21: 48 INNODB MONITOR OUTPUT Per second averages calculate from the last44 seconds INSERT BUFFER AND ADAPTIVE HASH INDEX Ibuf: size 7545, free list len 3790, seg size 11336, 8075308 inserts, 7540969 merged recs, 2246304 merges END OF INNODB MONITOR OUTPUT ==


seg size显示了当前 Insert Buffer的大小为11336×16KB,大约为177MB; free list len代表了空闲列表的长度;size代表了已经合并记录页的数量。而黑体部分的第2行 可能是用户真正关心的,因为它显示了插入性能的提高。 Inserts代表了插入的记录数; merged recs代表了合并的插入记录数量; merges代表合并的次数,也就是实际读取页的 次数。 merges: merged recs大约为1:3,代表了插入缓冲将对于非聚集索引页的离散逻辑请求大约降低了2/3 正如前面所说的,

目前 Insert Buffer存在一个问题是:在写密集的情况下,插入缓冲会占用过多的缓冲池内存(innodb_buffer pool),默认最大可以占用到1/2的缓冲池内存。
以下是InnoDB存储引擎源代码中对于 insert buffer的初始化操作:

~~~ 
/** Buffer pool size per the maximum insert buffer size*/
 #define IBUF_POOL_SIZE_PER _MAX _SIZE 2
 ibuf->max_size=buf_pool_get_size() / UNIV_PAGE_SIZE / IBUF_POOL_SIZE_PER_MAX_SIZE; 
~~~
这对于其他的操作可能会带来一定的影响。Percona上发布一些 patch来修正插入 缓冲占用太多缓冲池内存的情况,具体可以到 Percona官网进行查找。简单来说,修改 IBUF_POOL_SIZE_PER_MAX_SIZE  就可以对插入缓冲的大小进行控制。比如将IBUF_POOL_SIZE_PER_MAX_SIZE改为3，则最大只能使用1/3的缓冲池内存。


###2、Change Buffer 
InnoDB从1.0.x版本开始引入了 Change Buffer,可将其视为 Insert Buffer的升级 从这个版本开始, InnoDB存储引擎可以对DML操作 INSERT、 DELETE、 UPDATE 都进行缓冲,他们分别是: Insert Buffer、Delete Buffer、 Purge buffer 当然和之前 Insert Buffer一样, Change Buffer适用的对象依然是非唯一的辅助索引。

对一条记录进行 UPDATE 操作可能分为两个过程: 
1、将记录标记为已删除; 
2、真正将记录删除。

因此 Delete Buffer 对应 UPDATE操作的第一个过程,即将记录标记为删除。 Purge Buffer对应 UPDATE操作的第二个过程,即将记录真正的删除。

同时, InnoDB存储引擎提供了参数 innodb_change_buffering,用来开启各种 Buffer的选项。该参数可选的值 为: inserts、 deletes、 purges、 changes、all、 none inserts、 deletes。

purges 就是前面讨论过的三种情况。 changes表示启用 inserts和 deletes,all表示启用所有,none表示都不启用。该参数默认值为all。
~~~
SHOW VARIABLES LIKE '%innodb_change_buffering%' --all
~~~

从 InnoDB1.2.x版本开始,可以通过参数 innodb_change_buffer_max_size 来控制 Change Buffer 最大使用内存的数量: 
~~~
SHOW VARIABLES LIKE '%innodb_change_buffer_max_size%' --25
~~~

innodb_change_buffer_max_size  值默认为25,表示最多使用1/4的缓冲池内存空间。 而需要注意的是,该参数的最大有效值为50。

在 MySQL5.5版本中通过命令 SHOW ENGINE INNODB STATUS,可以观察到类似 如下的内容: 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f470180646e39d73.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
