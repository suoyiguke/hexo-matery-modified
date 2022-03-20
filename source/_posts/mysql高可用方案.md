---
title: mysql高可用方案.md
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
title: mysql高可用方案.md
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
### 简单主从




###大型集群方案
1、MHA 成熟稳定
2、MRG 未来MySQL高可用，发展的方向。MySQL8 mgr还可以，MySQL5.7 mgr基本无法使用
3、Innodb cluster ，MySQL Innodb cluster 被誉为MySQL RAC



###3个节点：
Orchestrator和replication-manager都是go语言开发的。
replication-manager 容易维护







##中间件代理方案
同求双节点高可用架构：
Arkproxy
原来用过 +proxysql 的
