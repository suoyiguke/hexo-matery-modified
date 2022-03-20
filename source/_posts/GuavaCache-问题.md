---
title: GuavaCache-问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-GuavaCache
categories: java-GuavaCache
---
---
title: GuavaCache-问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-GuavaCache
categories: java-GuavaCache
---
1、    private final ConcurrentMap<String, Cache> cacheMap = Maps.newConcurrentMap();
的 CacheName 不会被回收，怎么实现CacheName 的回收？

