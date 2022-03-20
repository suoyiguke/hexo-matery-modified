---
title: Elasticsearch-运维1.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
---
title: Elasticsearch-运维1.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
###es 获取所有节点状态
Elasticsearch 笔记 Elasticsearch 笔记

elasticsearch（es）如何获取集群中所有节点的信息，主要是状态、角色、ip、cpu、内存等占用情况？

1推荐方式
推荐方式
es 的监控 api _cat 提供了查看集群（cluster）中各节点（node）的接口 nodes，具体如下：

GET /_cat/nodes?v
示例输出如下：

ip            heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
172.16.18.122           65          99   7    1.71    1.44     1.40 mdi       -      elastic2
172.16.18.123           56          99   6    1.26    1.86     1.97 mdi       *      elastic3
172.16.18.125           47          99   6    1.16    1.51     1.42 mdi       -      elastic5
172.16.18.124           30          98   6    1.33    1.76     1.76 mdi       -      elastic4
172.16.18.126           47          98   6    1.34    1.33     1.47 mdi       -      elastic6
172.16.18.121           61          98   7    2.45    2.47     2.18 mdi       -      elastic1
该 nodes 命令显示集群的拓扑信息，分别包含了每个 node 的信息，每列的意义如下：

ip：集群中节点的 ip 地址；
heap.percent：堆内存的占用百分比；
ram.percent：总内存的占用百分比，其实这个不是很准确，因为 buff/cache 和 available 也被当作使用内存；
cpu：cpu 占用百分比；
load_1m：1 分钟内 cpu 负载；
load_5m：5 分钟内 cpu 负载；
load_15m：15 分钟内 cpu 负载；
node.role：mdi 分别表示 master、data、ingest；
master：* 代表是 master 节点，- 代表普通节点；
name：节点的名称。
