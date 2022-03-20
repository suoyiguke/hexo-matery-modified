---
title: java-集合之大总结.md
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
Collection

|　　├AbstractCollection  对Collection接口的最小化抽象实现

|　　│ 

|　　├List  有序集合

|　　│-├AbstractList  有序集合的最小化抽象实现 

|　　│-├ArrayList  基于数组实现的有序集合

|　　│-├LinkedList  基于链表实现的有序集合

|　　│-└Vector  矢量队列

|　　│　└Stack  栈，先进后出

|　　│

|　　├Set  不重复集合

|　　│├AbstractSet  不重复集合的最小化抽象实现

|　　│├HashSet  基于hash实现的不重复集合，无序

|　　│├LinkedHashSet  基于hash实现的不重复集合，有序

|　　│└SortedSet  可排序不重复集合

|　　│   └NavigableSet  可导航搜索的不重复集合

|　　│     └TreeSet  基于红黑树实现的可排序不重复集合

|　　│

|　　├Queue  队列

|　　│├AbstractQueue  队列的核心实现

|　　│├BlockingQueue  阻塞队列

|　　│└Deque  可两端操作线性集合

| 

Map  键值映射集合

|　　├AbstractMap  键值映射集合最小化抽象实现

|　　├Hashtable  基于哈希表实现的键值映射集合，key、value均不可为null

|　　├HashMap  类似Hashtable，但方法不同步，key、value可为null

|　　   └LinkedHashMap  根据插入顺序实现的键值映射集合

|　　├IdentityHashMap  基于哈希表实现的键值映射集合，两个key引用相等==，认为是同一个key

|　　├SortedMap   可排序键值映射集合

|　　   └NavigableMap  可导航搜索的键值映射集合

|　   └WeakHashMap  弱引用建，不阻塞被垃圾回收器回收，key回收后自动移除键值对

![image](https://upload-images.jianshu.io/upload_images/13965490-218823be9d9a1e5e.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以比较的点：

*   有序、无序
*   可重复、不可重复
*   键、值是否可为null
*   底层实现的数据结构（数组、链表、哈希...）
*   线程安全性
