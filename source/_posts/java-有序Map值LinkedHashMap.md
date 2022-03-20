---
title: java-有序Map值LinkedHashMap.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
LinkedHashMap 拥有 HashMap 的所有特性，它比 HashMap 多维护了一个双向链表，因此可以按照插入的顺序从头部或者从尾部迭代，是有序的，不过因为比 HashMap 多维护了一个双向链表，它的内存相比而言要比 HashMap 大，并且性能会差一些，但是如果需要考虑到元素插入的顺序的话， LinkedHashMap 不失为一种好的选择
