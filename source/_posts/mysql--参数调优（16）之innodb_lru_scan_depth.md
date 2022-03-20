---
title: mysql--参数调优（16）之innodb_lru_scan_depth.md
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
title: mysql--参数调优（16）之innodb_lru_scan_depth.md
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
27)innodb_lru_scan_depth

推荐设置：2000

作用：

innodb_io_capactiy 在sas 15000转的下配置800就可以了，在ssd下面配置2000以上。

可使用默认配置。即不设。如果不配的后果：

默认为200，db吞吐量上不去。

配置实例：

innodb_lru_scan_depth = 2000
