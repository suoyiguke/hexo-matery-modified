---
title: mysql--参数调优（16）之-innodb_buffer_pool_load_at_startup、innodb_buffer_pool.md
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
title: mysql--参数调优（16）之-innodb_buffer_pool_load_at_startup、innodb_buffer_pool.md
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
25)innodb_buffer_pool_load_at_startup

推荐设置：

0

作用：

这两个参数几乎没人用一般dba也不曾听说过，它是什么意思呢？Mysql在第一次（重启）时，它的buffer_pool_size中是空的，随着mysql运行时间1-2小时后，它的buffer_pool_size里开始被塞入东西，它分为old block与new block，而此时mysql性能开始一点点读写效率上去了，那是因为在buffer_pool_size没有放入东西时，mysql很多读写发生在硬盘上，从硬盘到内存的加载过程是一个比较漫长和耗时的过程，因此我们往往会设一个startup=1以加快这个“预热”过程，它与参数shutdown配合使用，即相当于把上次使用的innot_db_buffer_pool里的东西在启动时先做一次加载，以加快mysql的性能。它会在innodb的数据目录中生成一个文件：ib_buffer_pool。高度注意：加入了startup和shutdown=1时，mysql的启动过程会比较慢，如果你上次的dump出的buffer_pool里的东西有50多g那么mysql启动时的加载过程会变得比较慢。这个值很多人使用默认的0（不开启），它的影响就是你在mysql重启后，一开始你的系统读写性能不如在你系统运行了2-4小时（视db读写而定）反而它的读写性能变好了。不设使用默认值（0）。

如果不配的后果：

不配的话系统默认为0

配置实例：

innodb_buffer_pool_load_at_startup = 0
