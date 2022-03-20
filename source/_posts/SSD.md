---
title: SSD.md
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
title: SSD.md
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
机械硬盘 100IOPS 
顺序读 100M每秒。磁盘带宽
随机读性能非常慢。用吞吐量IOPS，每秒钟处理IO的能力来衡量；
对于数据库最看重的就是随机访问IOPS能力

![image.png](https://upload-images.jianshu.io/upload_images/13965490-716ebb53688e6e13.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

固态硬盘 100万IOPS
MYSQL一定要使用固态硬盘


###配置
1、centos
调整磁盘调度算法是：deadline 或 noop；
即使是HDD盘也需要调为deadline ，只是没有SSD那么明显
~~~
[root@localhost block]# echo deadline > /sys/block/sda/queue/scheduler 
[root@localhost block]# cat /sys/block/sda/queue/scheduler 
noop [deadline] cfq 
[root@localhost block]# cat /sys/block/sr0/queue/scheduler 
noop [deadline] cfq 
[root@localhost block]# echo deadline > /sys/block/sr0/queue/scheduler 
[root@localhost block]# cat /sys/block/sr0/queue/scheduler 
noop [deadline] cfq 

~~~


2、磁盘参数
这个参数与磁盘性能非常大关系。极大影响IOPS
~~~
 //SSD，平缓刷新。解决抖动
innodb_flush_neighbors =0
 //设置了raid还能线上还可以调成8G
innodb_log_file_size = 4G
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2fc87f210d768a77.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



3、SSD推荐
100万IOPS



![image.png](https://upload-images.jianshu.io/upload_images/13965490-046d5f38ddd707dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



4、文件系统推荐
- cfs/ext4
- noatime
- nobarrier

5、操作系统
- 推荐linux
- 关闭swap
- 磁盘调度算法设置为deadline 
- mount 加上 noatime,noarrie
![image.png](https://upload-images.jianshu.io/upload_images/13965490-63ff8076b70f98b2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



20块固态做raid 5




>普通的IOPS到6W差不多了
