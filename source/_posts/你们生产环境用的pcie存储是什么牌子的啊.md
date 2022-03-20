---
title: 你们生产环境用的pcie存储是什么牌子的啊.md
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
title: 你们生产环境用的pcie存储是什么牌子的啊.md
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
刘皇叔:
你们生产环境用的pcie存储是什么牌子的啊

刘皇叔:
稳定性怎么样

走失的小老虎儿:
我们超云的，inter芯片！

走失的小老虎儿:
不过是sas协议

走失的小老虎儿:
不是pci

刘皇叔:
nvme的呢

走失的小老虎儿:
nvme 也是

走失的小老虎儿:
m.2的口，pcie协议！

走失的小老虎儿:
性能还可以，不能做raid，用lvm条带

走失的小老虎儿:
两块盘每秒可以7g左右

走失的小老虎儿:
pcie是cpu直通的，不能过raid阵列，所以支持不了raid

刘皇叔:


走失的小老虎儿:
超云机器国产的，建议入坑试试！


走失的小老虎儿:
[哈哈]

不会游泳的鱼:
8.0.24推了？

走失的小老虎儿:
提供的磁盘，做完raid 10，每秒160m写入！
