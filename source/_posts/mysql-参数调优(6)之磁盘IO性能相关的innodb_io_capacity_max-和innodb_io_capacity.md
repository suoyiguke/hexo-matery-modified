---
title: mysql-参数调优(6)之磁盘IO性能相关的innodb_io_capacity_max-和innodb_io_capacity.md
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
title: mysql-参数调优(6)之磁盘IO性能相关的innodb_io_capacity_max-和innodb_io_capacity.md
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
作用于磁盘IO，可以提高db吞吐量,提高写入性能

###innodb_io_capacity

 在Innodb 1.0.x版本之前，这个参数不存在，InnoDB存储引擎最大只会每秒只会刷新100个脏页到磁盘、合并20个插入缓冲。这种硬编码实现方式限制了 磁盘IO吞吐量和写入性能。所以之后提供了一个可以直接配置这个阈值的方式，那么就是  `innodb_io_capacity`  


InnoDB Plugin(从 InnoDB1.0.x版本开始)提供了参数  innodb_io_capacity

>该参数影响两个方面，规则如下: 
1、合并插入缓冲时,每秒合并插入缓冲的数量为 innodb_io_capacity值的5%，默认就是 200*5%=10 
2、在从缓冲区刷新脏页时（checkpoint）,每秒刷新脏页的数量就等于innodb_io_capacity的值，默认200


配置建议，它是innodb_io_capacity_max的一半，默认innodb_io_capacity=100。同样，它对读无效对写有决定意义。


这是一个更加高级的调优，只有当你在频繁写操作的时候才有意义（它不适用于读操作）。若你真的需要对它进行调整，最好的方法是要了解系统可以支持多大的 IOPS。譬如，假设服务器有一块 SSD 硬盘，我们可以设置 `innodb_io_capacity_max=6000` 和 `innodb_io_capacity=3000`（最大值的一半）。运行 sysbench 或者任何其他基准工具来对磁盘吞吐量来进行基准测试是一个好方法。


###innodb_io_capacity_max


若用户使用了SSD类的磁盘,或者将几块磁盘做了RAID,当存储设备拥有更高的 IO速度时,完全可以将 innodbio_capacity值调得再高点,直到符合磁盘IO的吞吐量 为止。 



默认 innodb_io_capacity_max=200


推荐配置如下：

innodb_io_capacity 它会直接决定mysql的tps（吞吐性能），这边给出参考：
sata/sas硬盘这个值在200
sas raid10: 2000
ssd硬盘：8000
 fusion-io（闪存卡）：25,000-50,000

当然最佳的值还是需要自己测试在决定！


>* innodb_io_capacity：用来当刷新脏数据时，控制MySQL每秒执行的写IO量。  * innodb_io_capacity_max: 在压力下，控制当刷新脏数据时MySQL每秒执行的写IO量  首先，这与读取无关 – SELECT查询执行的操作。对于读操作，MySQL会尽最大可能处理并返回结果。至于写操作，MySQL在后台会循环刷新，在每一个循环会检查有多少数据需要刷新，并且不会用超过innodb_io_capacity指定的数来做刷新操作。这也包括更改缓冲区合并（在它们刷新到磁盘之前，更改缓冲区是辅助脏页存储的关键）。  第二，我需要解释一下什么叫“在压力下”，MySQL中称为”紧急情况”，是当MySQL在后台刷新时，它需要刷新一些数据为了让新的写操作进来。然后，MySQL会用到innodb_io_capacity_max。  那么，应该设置innodb_io_capacity和innodb_io_capacity_max为什么呢？  最好的方法是测量你的存储设置的随机写吞吐量，然后给innodb_io_capacity_max设置为你的设备能达到的最大IOPS。innodb_io_capacity就设置为它的50-75%，特别是你的系统主要是写操作时。  通常你可以预测你的系统的IOPS是多少。例如由8 15k硬盘组成的RAID10能做大约每秒1000随机写操作，所以你可以设置innodb_io_capacity=600和innodb_io_capacity_max=1000。许多廉价企业SSD可以做4,000-10,000 IOPS等。  这个值设置得不完美问题不大。但是，要注意默认的200和400会限制你的写吞吐量，因此你可能偶尔会捕捉到刷新进程。如果出现这种情况，可能是已经达到你硬盘的写IO吞吐量，或者这个值设置得太小限制了吞吐量。
