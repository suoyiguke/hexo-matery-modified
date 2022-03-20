---
title: java-集合之如何决定使用HashMap还是TreeMap？.md
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
HashMap基于散列桶（数组和链表）实现；TreeMap基于红黑树实现。
HashMap不支持排序；TreeMap默认是按照Key值升序排序的，可指定排序的比较器，主要用于存入元素时对元素进行自动排序。
HashMap大多数情况下有更好的性能，尤其是读数据。在没有排序要求的情况下，使用HashMap。
都是非线程安全。


###使用建议
（1）HashMap:适用于在Map中插入、删除和定位元素。 
（2）Treemap:适用于按自然顺序或自定义顺序遍历键（key）。 
（3）HashMap通常比TreeMap快一点（树和哈希表的数据结构使然），建议多使用HashMap,在需要排序的Map时候才用TreeMap. 
（4）HashMap 非线程安全 TreeMap 非线程安全 
（5）HashMap的结果是没有排序的，而TreeMap输出的结果是排好序的。

在HashMap中通过get（）来获取value,通过put（）来插入value,ContainsKey（）则用来检验对象是否已经存在。可以看出，和ArrayList的操作相比，HashMap除了通过key索引其内容之外，别的方面差异并不大。
