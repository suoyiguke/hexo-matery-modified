---
title: java集合之数据结构特征.md
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
###集合类型（后缀）
1、List
可重复、有序（按插入顺序排序）、支持随机访问get(index)
2、Set
不可重复、不支持随机访问
3、Map
key-value形式；key不可重复，value可重复。

###集合特征（前缀）
1、Hash 
无序；
Hash的 containsKey、get、put 和 remove 的时间复杂度是O(1)，这些操作性能强于Tree O(log n)；


2、Linked
有序（按插入顺序排序）；
Linked进行remove、add操作效率高于Array;

3、Tree
排序（可自定义排序）、不可以指定集合初始容量; 代表：TreeMap、TreeSet；

4、Array
Array随机get(index)访问效率高于Linked




###性能比较
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b784c2010561f016.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
