---
title: GC问题排查思路.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: GC问题排查思路.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
###可视化实时内存监控，现在各个区域是怎么样了
涉及到类似的错误，最开始三板斧肯定是查看 JVM 的情况。很多中小型公司没有建立可视化的监控平台，比如Zabbix、Ganglia、Open-Falcon、Prometheus等等，没办法直接可视化看到JVM各个区域的内存变化，GC次数和GC耗时。

###或者使用jstat 查看内存
不过不用怕，咱们用 jstat 这种工具也可以。

###dump内存快照和jhat分析
分析到这里，后面的过程就很简单了，我们可以通过 jmap 工具，dump 出内存快照，然后再用 jhat 或者 Visual VM 之类的可视化工具来分析就可以了。

通过内存快照的分析，直接定位出来那个几百MB的大对象，发现竟然是个Map之类的数据结构，这是什么鬼？

返回头去开始撸代码，发现是从数据库里查出来的数据存放在了这个Map里，没有好办法，再继续地毯式排查。

最后发现竟然是有条坑爹的 SQL 语句没加 where条件！！不知道是手滑还是忘了，测试的时候这个分支也没走到（*画外音：这段代码的开发和测试都不是我*

![重大事故！线上系统频繁卡死，凶手竟然是 Full GC？](https://upload-images.jianshu.io/upload_images/13965490-ef312a11bcfb1a3a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

）

没有 where 条件，每次查询肯定会有超出预期的大量数据，导致了每隔一段时间就会搞出几个上百 MB 的大对象，这些对象全部直接进入老年代，然后触发 Full GC ！
