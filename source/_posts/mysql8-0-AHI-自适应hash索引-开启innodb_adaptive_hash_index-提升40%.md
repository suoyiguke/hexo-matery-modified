---
title: mysql8-0-AHI-自适应hash索引-开启innodb_adaptive_hash_index-提升40%.md
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
title: mysql8-0-AHI-自适应hash索引-开启innodb_adaptive_hash_index-提升40%.md
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

###AHI
Adaptive Hash Index  
AHI
自适应hash索引 

~~~
SHOW VARIABLES like '%innodb_adaptive_hash_index%'
~~~




MySQL InnoDB存储引擎的自适应哈希（Adaptive Hash Index，下简称AHI）功能，想必很多同学都有所了解。**若用户的访问模式基本都是类似KV操作的点查询（point select），则InnoDB存储引擎会自动创建哈希索引。** 在有了哈希索引后，查询无需走B+树搜索，而直接通过hash就能直接定位查询的数据。因此，通过AHI功能，MySQL的查询性能就能得到大幅提升。查询能提升多少呢？对于写入操作又是否有影响呢？AHI有什么副作用么？今天姜老师就将带你走进最熟悉的InnoDB功能：AHI。


###AHI读写性能影响

想必很多同学没有意识到，AHI能有40%的性能提升。而这就是哈希索引的威力。从下图可以看到，在AHI的加持下，主键查询可以达到140万的QPS： 

![图片](https://upload-images.jianshu.io/upload_images/13965490-c99420f3b419f08e?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但若当我们通过参数 innodb_adaptive_hash_index 关闭AHI功能后，主键查询的性能下跌为了100万QPS：

![图片](https://upload-images.jianshu.io/upload_images/13965490-bc652bd2c13811ae?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对于写入操作，开启和关闭AHI功能对性能的影响都没有太大的区别。
这是因为当DML测试时， MySQL 的瓶颈主要是在磁盘写入。具体可以通过 sysbench 的 oltp_update_index.lua 基准测试进行观察。 整个测试请看下面的测试： 

<iframe class="video_iframe rich_pages" data-vidtype="2" data-mpvid="wxv_1907498846515953669" data-cover="http%3A%2F%2Fmmbiz.qpic.cn%2Fmmbiz_jpg%2FMEpoEwcicyJkNzLREwWo6SzUwkpiaqvdqgG6ouJ3BrbaRa6wHwqTrsmKFicCX1GTUhaz3sfb64DIOr6Lpftkh6xIA%2F0%3Fwx_fmt%3Djpeg" allowfullscreen="" frameborder="0" data-ratio="1.8444444444444446" data-w="1992" data-src="https://mp.weixin.qq.com/mp/readtemplate?t=pages/video_player_tmpl&amp;auto=0&amp;vid=wxv_1907498846515953669" width="677" height="393" data-vh="380.8125" data-vw="677" scrolling="no" marginwidth="0" marginheight="0" src="https://mp.weixin.qq.com/mp/videoplayer?video_h=380.8125&amp;video_w=677&amp;scene=126&amp;random_num=9751&amp;article_title=MySQL%E6%80%A7%E8%83%BD%E6%8F%90%E5%8D%8740%25%E7%9A%84AHI%E5%8A%9F%E8%83%BD%EF%BC%8C%E4%BD%A0%E7%9F%A5%E9%81%93%E4%B9%88%EF%BC%9F&amp;source=4&amp;vid=wxv_1907498846515953669&amp;mid=2649741497&amp;idx=1&amp;__biz=MjM5MjIxNDA4NA==&amp;nodetailbar=0&amp;uin=MTUwNDEwNjk3Ng==&amp;key=8a4cd6e752389d60037c4ec10174266abb047b9189fbb920fd14b50ed25735ea26643eb6ad55dfe7f6af05270950a1865b8b932ed9fce0375836969c927e16cba1cc910cdde4ff1ab652592e991f895ea53be1bc6f1bb78190bd4878634c0488fa6d46b8fbabb2a4f9c3879c28505c4e9833aae194d145bd734699ebf226d300&amp;pass_ticket=2B2xs/U0KTA2x1x2MwtZFHjT6Yk6hVdlOr4pt7fGolareMChE9uqth+EzaMclEi/&amp;version=&amp;devicetype=Windows&amp;nbsp;10&amp;nbsp;x64&amp;wxtoken=777&amp;sessionid=1626316562&amp;preview=0&amp;is_in_pay_subscribe=0&amp;nickname=InsideMySQL&amp;roundHeadImg=http://mmbiz.qpic.cn/mmbiz_png/MEpoEwcicyJnImTO91oibgWWd4bFX0aORJyoF8gibF6b298No0tKjKfxLH5AASdC72b5VPp0Y4KAibtf89JI3nWfVQ/0?wx_fmt=png&amp;enterid=1626317147&amp;subscene=" style="margin: 0px; padding: 0px; max-width: 100%; box-sizing: border-box !important; overflow-wrap: break-word !important; display: block; width: 677px !important; height: 393px !important; overflow: hidden; top: 0px;"></iframe>


###AHI的副作用

作为一个几乎透明的功能，其实一般用户无需关心，基本可以认为AHI是即开即用的功能。默认AHI参数的设置也是比较合理的，例如参数 innodb_adaptive_hash_index_parts 设置为 8 。
然而，AHI存在一个副作用：当删除大表，且缓冲池（Buffer Pool，下简称BP）比较大，如超过32G，则MySQL数据库可能会有短暂被hang住的情况发生。这时会对业务线程造成一定影响，从而导致业务系统的抖动。产生这个问题的原因是在删除表的时候，InnoDB存储引擎会将该表在BP中的内存都淘汰掉，释放可用空间。这其中包括数据页、索引页、自适应哈希页等。当BP比较大是，扫描BP中flush_list链表需要比较长的时间，因此会产生系统的抖动。因此在海量的互联网并发业务中，删除表操作需要做精细的逻辑控制，如： 

*1\. 业务低峰期删除大表；*

*2\. 删除表前禁用AHI功能；*

*3\. 控制脏页链表长度，只有长度小于一定阈值，才发起删除操作；*

*4\. 删除表后启用AHI功能；*  

不过呢，所有这么麻烦的处理在 MySQL 8.0.23 版本之后，就都不再需要了。 因为官方已经彻底修复了这个问题：

![图片](https://upload-images.jianshu.io/upload_images/13965490-a6af69dd1413de1c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意，截至目前最新的 MySQL 5.7.34 版本并没有进行修复，所以 5.7 还需要用户自己做控制。
若有同学想知道 MySQL 8.0 中的具体修复逻辑，可见github上提交：*https://github.com/mysql/mysql-server/commit/a0aa59ad8a42dcbbb69b911990b89ecd6c14b851*



###总结

AHI真的是一个InnoDB的好功能，这才是真正的AI数据库该有的样子。但InnoDB存储引擎在2001年发布时，就支持了这个功能，创始人Heikki Tuuri真可谓具有卓越的远见。但在使用时，要特别注意删除大表可能产生的hang住问题。这会对业务产生一定的影响，对于较高要求的业务来说，或许是不能接受的。不过，若升级到 MySQL 8.0.23 版本后，这些问题将不复存在。那么，升级 MySQL 8.0 ，你准备好了么？





###推荐

仅限于8.0.23+，现在推荐开启AHI


