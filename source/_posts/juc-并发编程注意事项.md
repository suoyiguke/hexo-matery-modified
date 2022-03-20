---
title: juc-并发编程注意事项.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: juc-并发编程注意事项.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
【强制】 高并发时，同步调用应该去考量锁的性能损耗。能用无锁数据结构，就不要用锁；
能锁区块，就不要锁整个方法体；能用对象锁，就不要用类锁。
说明：尽可能使加锁的代码块工作量尽可能的小，避免在锁代码块中调用 RPC 方法
