---
title: ConcurrentSkipListMap.md
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
title: ConcurrentSkipListMap.md
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
>ConcurrentSkipListMap 可以看做是是线程安全的treeMap

ConcurrentHashMap
JDK为我们提供了很多Map接口的实现，使得我们可以方便地处理Key-Value的数据结构。


当我们希望快速存取<Key, Value>键值对时我们可以使用HashMap。
当我们希望在多线程并发存取<Key, Value>键值对时，我们会选择ConcurrentHashMap。
TreeMap则会帮助我们保证数据是按照Key的自然顺序或者compareTo方法指定的排序规则进行排序。
OK，那么当我们需要多线程并发存取<Key, Value>数据并且希望保证数据有序时，我们需要怎么做呢？
也许，我们可以选择ConcurrentTreeMap。不好意思，JDK没有提供这么好的数据结构给我们。
当然，我们可以自己添加lock来实现ConcurrentTreeMap，但是随着并发量的提升，lock带来的性能开销也随之增大。
Don't cry......，JDK6里面引入的ConcurrentSkipListMap也许可以满足我们的需求。
什么是ConcurrentSkipListMap
ConcurrentSkipListMap提供了一种线程安全的并发访问的排序映射表。内部是SkipList（跳表）结构实现，在理论上能够O(log(n))时间内完成查找、插入、删除操作。
存储结构
ConcurrentSkipListMap存储结构跳跃表（SkipList）：
1、最底层的数据节点按照关键字升序排列。
2、包含多级索引，每个级别的索引节点按照其关联数据节点的关键字升序排列。
3、高级别索引是其低级别索引的子集。
4、如果关键字key在级别level=i的索引中出现，则级别level<=i的所有索引中都包含key。
注：类比一下数据库的索引、B+树。


###为什么没有ConcurrentTreeMap？

例如,一个非并发HashMap拥有并发对等的ConcurrentHashMap.为什么TreeMap不会发生？

解决方法
Why there is the non-concurrent TreeMap on one side and the ConcurrentSkipListMap on one other?

我怀疑这是因为使一个树结构并发太难或遭遇锁定性能问题.在有序集合方面,SkipLists是非常简单的数据结构,并为树提供类似的行为和性能.

不用说,SkipList可以提供类似的特征,这些特征就是为了查找,插入,删除等提供O(logN)性能的项目的有序集合.至少它给出了性能的概率近似.

这是一个good page about skiplists.他们是非常酷的数据结构.我只能希望在现代编程数据结构类中被教授.
