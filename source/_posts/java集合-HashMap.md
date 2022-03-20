---
title: java集合-HashMap.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java源码分析
categories: java源码分析
---
---
title: java集合-HashMap.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java源码分析
categories: java源码分析
---
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4aaff5a391963b9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 初始容量16
![image.png](https://upload-images.jianshu.io/upload_images/13965490-55997e2888d18176.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 加载因子 0.75
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e6f95322e0410835.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 扩容为原来的2倍 

- HashMap是基于哈希表实现的，用Entry[]来存储数据，而Entry中封装了key、value、hash以及Entry类型的next
- HashMap存储数据是无序的
- hash冲突是通过拉链法解决的
- HashMap的容量永远为2的幂次方，有利于哈希表的散列
- HashMap不支持存储多个相同的key，且只保存一个key为null的值，多个会覆盖
- put过程，是先通过key算出hash，然后用hash算出应该存储在table中的index，然后遍历table[index]，看是否有相同的key存在，存在，则更新value；不存在则插入到table[index]单向链表的表头，时间复杂度为O(n)
- get过程，通过key算出hash，然后用hash算出应该存储在table中的index，然后遍历table[index]，然后比对key，找到相同的key，则取出其value，时间复杂度为O(n)
- HashMap是线程不安全的，如果有线程安全需求，推荐使用ConcurrentHashMap

hashMap源码分析：
https://blog.csdn.net/zjxxyz123/article/details/81111627
