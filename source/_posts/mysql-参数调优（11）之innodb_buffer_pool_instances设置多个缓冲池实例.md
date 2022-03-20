---
title: mysql-参数调优（11）之innodb_buffer_pool_instances设置多个缓冲池实例.md
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
title: mysql-参数调优（11）之innodb_buffer_pool_instances设置多个缓冲池实例.md
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
>INNODB_BUFFER_POOL_INSTANCES 参数也是在高并发高负载下设置后会对性能有提升

MySQL 5.5引入了缓冲实例作为减小内部锁争用来提高MySQL吞吐量的手段。在5.5版本这个对提升吞吐量帮助很小，然后在MySQL 5.6版本这个提升就非常大了，所以在MySQL5.5中你可能会保守地设置innodb_buffer_pool_instances=4，在MySQL 5.6和5.7中你可以设置为8-16个缓冲池实例。设置后观察会觉得性能提高不大，但在大多数高负载情况下，它应该会有不错的表现。对了，不要指望这个设置能减少你单个查询的响应时间。这个是在高并发负载的服务器上才看得出区别。比如多个线程同时做许多事情。

5.7、8.0 下INNODB_BUFFER_POOL_INSTANCES默认为1，若mysql存在高并发和高负载访问，设置为1则会造成大量线程对BUFFER_POOL的单实例互斥锁竞争，这样会消耗一定量的性能的。

pool_instances 可以设置为cpu核心数，它的作用是：
1）对于缓冲池在数千兆字节范围内的系统，通过减少争用不同线程对缓存页面进行读写的争用，将缓冲池划分为多个单独的实例可以提高并发性。可以类比为 java中的`ThreadLocal 线程本地变量` 就是为每个线程维护一个buffer pool实例，这样就不用去争用同一个实例了。相当于减少高并发下mysql对INNODB_BUFFER缓冲池的争用。

2）使用散列函数将存储在缓冲池中或从缓冲池读取的每个页面随机分配给其中一个缓冲池实例。每个缓冲池管理自己的空闲列表， 刷新列表， LRU和连接到缓冲池的所有其他数据结构，并受其自己的缓冲池互斥量保护。

>innodb_buffer_pool_size的设置需要为pool_instance的整数倍。可以被pool_instance整除，为每个buffer pool实例平均分配内存。

