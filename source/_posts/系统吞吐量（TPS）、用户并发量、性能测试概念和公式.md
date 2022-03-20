---
title: 系统吞吐量（TPS）、用户并发量、性能测试概念和公式.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: 系统吞吐量（TPS）、用户并发量、性能测试概念和公式.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
系统吞吐量几个重要参数：QPS（TPS）、并发数、响应时间



###系统吞度量的三个要素


QPS（TPS）：每秒钟request数/事务 数量
并发数： 系统同时处理的request数/事务数
响应时间：  一般取平均响应时间

###三要素之间的关系
理解了上面三个要素的意义之后，就能推算出它们之间的关系：
QPS（TPS）= 并发数/平均响应时间

