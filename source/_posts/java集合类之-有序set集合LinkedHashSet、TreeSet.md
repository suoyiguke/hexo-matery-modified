---
title: java集合类之-有序set集合LinkedHashSet、TreeSet.md
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
> set 特征是去重；list特征是有序。有没有既有序又去重的集合呢？还真有！

###LinkedHashSet

>LinkedHashSet（有序）通过链表的形式保证有序；它的有序指的是`插入顺序`。

顾名思义，LinkedHashSet包含了三个数据结构要素：Linked、Hash、Set。
set集合不可重复，没有get方法。Linked 保证插入顺序。

这样的话，LinkedHashSet 就是有序、不重复、初始化不可指定大小（初始大小只能是0）、不能使用get(index)进行随机访问。


###TreeMap、TreeSet
TreeSet（有序），可以使用比较器：Comparable（内部）与Comparator（外部），通过Collections.sort()进行排序；
内部比较器-对应类上面实现comparable的接口，重写compare的方法；
 例如：Collections.sort(set);
外部比较器--对应类上面，编写内部静态类-比较器，实现对应的comparator接口；
 例如：Collections.sort(set, new AscAgeComparator());

 注意：set集合中保存对象的时候，去重，要重写对象的hashcode()和equals()方法


>TreeMap的基本操作 containsKey、get、put 和 remove 的时间复杂度是 O(log n)，HashMap的时间复杂度是O(1)，可见没有排序需求的情况下HashMap的性能更好。
