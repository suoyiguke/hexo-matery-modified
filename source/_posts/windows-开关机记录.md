---
title: windows-开关机记录.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
---
title: windows-开关机记录.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
###ctrl + R
输入 eventvwr

1、计算机--> 右键 --> 管理

2、

　　![image](https://upload-images.jianshu.io/upload_images/13965490-8dec4c73f522510d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

　　查了下资料：

| **6005** | 信息 | EventLog | 事件日志服务已启动。(开机) |
| **6006** | 信息 | EventLog | 事件日志服务已停止。(关机) |

　　　　其中6005,6006的解说，基本正确，但是 有一个 6009（6009信息EventLog按ctrl、alt、delete键(非正常)关机）基本不正确... 我这里机子上 开机也会有 6009，难道是 按ctrl、alt、delete键 就会有 6009？未查到 ms的官方说明...


###具体编码
开关机日志
正常
1074, 6006, 13, 12, 6005,41,6008
1074 记录某用户在某计划下重启
6006 日志服务关闭
13 OS关闭时间按
12 OS启动时间
6005 日志服务开启


异常
41,6008
41	断点或故障要重启
6008 系统在某时间关机
后续没有记录OS和日志服务的关闭时间。
只有日志和OS启动时间。
