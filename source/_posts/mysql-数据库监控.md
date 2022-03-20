---
title: mysql-数据库监控.md
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
title: mysql-数据库监控.md
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
目前常用开源监控工具有nagios，zabbix，grafana，但这些是面向专业DBA使用的，而对于业务研发人员来说，没有专业的MySQL理论知识，并且上述监控工具均为纯英文界面，交互不直观，那么多的监控指标，你知道有哪些是研发最关心的吗？

所以每次都是DBA通知研发，系统哪块出了问题，这样的效率其实是低下的，我是希望把监控这块东西定制化，做成开发一眼就能看懂的指标项，纯中文页面，清爽直观，简约而不简单，出了问题报警信息直接第一时间推送给研发，效率会大大提升，同时也减少了DBA作为中间人传话的作用（传达室大爷角色）。

参考了天兔Lepus的UI风格，目前采集了数据库连接数（具体连接了哪些应用程序IP，账号统计）、QPS/TPS、索引使用率统计，同步复制状态/延迟监控。
