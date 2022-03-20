---
title: mysql-router+mysql-shell+mgr就是innodb-cluster.md
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
title: mysql-router+mysql-shell+mgr就是innodb-cluster.md
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
田帅萌:
这个不是我公众号的吗。。

但行好事  莫问前程:
美团和京东用mgr还是很多的

但行好事  莫问前程:
是的

但行好事  莫问前程:
优秀的文档，分享一下

戒糖低盐轻碳水:
记得是翻译的官方文档

一失足成千古风流人物🐾:
赞

但行好事  莫问前程:
我们环境也用的mysql innodb cluster,把mgr做成一个高可用组件。

阑珊处:


Traveler过客:
@郑州-税友-常伟俊  业务直接连接的是mysql router嘛

但行好事  莫问前程:
也在探索中，刚开始使用

但行好事  莫问前程:
是的

但行好事  莫问前程:
MySQL router

但行好事  莫问前程:
非核心业务

戒糖低盐轻碳水:
mysql router+mysql shell+mgr就是innodb cluster

Traveler过客:
有些金融企业还是有点不敢用，还是用传统的主从架构

但行好事  莫问前程:
@深圳-神州信息-馒头 是的

但行好事  莫问前程:
我们架构是非关键信息主从复制，关键信息innodb cluster，中间通过kafka分发到这两个节点。

但行好事  莫问前程:
不是核心业务

但行好事  莫问前程:
慢慢探索中

但行好事  莫问前程:
总共用了20多个机器


杨惠:
大家现在mysql在业务中用的最多架构是那些

但行好事  莫问前程:
主从复制1主3从，innodb cluster 5节点，kafka 3节点。中间还有备份服务器，监控服务器，中间用的的是weblogic 2 节点，负载均衡用的F5

但行好事  莫问前程:
主从复制吧！

无所谓:
主从复制

不会游泳的鱼:
我就一个主从
