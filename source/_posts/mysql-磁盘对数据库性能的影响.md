---
title: mysql-磁盘对数据库性能的影响.md
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
title: mysql-磁盘对数据库性能的影响.md
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
###传统机械硬盘
当前大多数数据库使用的都是传统的机械硬盘。机械硬盘的技术目前已非常成熟，在服务器领域一般使用SAS或SATA接口的硬盘。服务器机械硬盘开始向小型化转型，目前大部分使用25寸的SAS机械硬盘。
机械硬盘有两个重要的指标：一个是寻道时间，另一个是转速。当前服务器机械硬盘的寻道时间已经能够达到3ms，转速为15000RM(rotate per minute)。传统机械硬盘最大的问题在于读写磁头，读写磁头的设计使硬盘可以不再像磁带一样，只能进行顺序访问，而是可以随机访问。但是，机械硬盘的访问需要耗费长时间的磁头旋转和定位来查找，因此顺序访问的速度要远高于随机访问。传统关系数据库的很多设计也都是在尽量充分地利用顺序访问的特性

>通常来说，可以将多块机械硬盘组成`RAID`来提高数据库的性能，也可以将数据文件分布在不同硬盘上来达到访问负载的均衡。


### 固态硬盘


1、对于固态硬盘在 InnoDB存储引擎中的优化，可以增加innodb_io_capacity变量的值达到充分利用固态硬盘带来的高IOPS特性。不过这需要用户根据自己的应用进行有针对性的调整。

2、在 InnoSQL及 InnoDB1.2版本中，可以选择关闭邻接页的刷新，同样可以为数据库的性能带来一定效果的提升此外

3、还可以使用 InnoSQL开发的L2 Cache解决方案，该解决方案可以充分利用固态硬盘的超高速随机读取性能，在内存缓冲池和传统存储层之间建立一层基于闪存固态硬盘的二级缓冲池，以此来扩充缓冲池的容量，提高数据库的性能。

4、与基于磁盘的固态硬盘 Cache类似的解决方案还有 Facebook Flash Cache和 bcache，只不过它们是基于通用文件系统的，对 InnoDB存储引擎本身的优化较少
 
###磁盘IO关键参数：
innodb_io_capacity
