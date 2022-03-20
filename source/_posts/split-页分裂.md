---
title: split-页分裂.md
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
title: split-页分裂.md
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

页之间是逻辑排序的。
页内数据也是逻辑有序的。

当16k的页存满了之后就会创建一个新的空闲页，来存新的数据。

split页分裂代价比较大。


5.7之前的页分裂时会使用大锁会锁主整个个树。
