---
title: mysql隔离级别道到底选择RR还是RC.md
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
title: mysql隔离级别道到底选择RR还是RC.md
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
但行好事  莫问前程:
现在生产环境，MySQL的隔离级别是调整成读已提交。

卡门:
为啥，这样做有什么好处吗。有些书上说rc和rr性能差别不大。

ClassIn.weibiao:
rc死锁更少。

阮胜昌:
oracle 的锁级别的RC



ClassIn.weibiao:
rc死锁更少。

阮胜昌:
oracle 的锁级别的RC

卡门:
因为Rc下禁用Gap lock的吗

无所谓:
丁奇45讲讲的很细

无所谓:
可以看看

Xanxus:
rc也有gap lock啊

ClassIn.weibiao:
@深圳-Sgl-莱昂纳德 没有，gap锁少些，

ClassIn.weibiao:
我们有些业务改rc了。

卡门:
嗯嗯，回头去看看

Xanxus:
我觉得应该是rr下，插入性能会有很大影响

Xanxus:
其他死锁什么应该都不是最主要的原因

rr要维护旧版本的undo快照的原因吗。所以说插入会说受影响?有没有测试过
