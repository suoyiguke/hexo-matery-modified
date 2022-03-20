---
title: 7种遍历hashMap的方式那种最好？.md
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
HashMap 遍历从大的方向来说，可分为以下 4 类：

迭代器（Iterator）方式遍历；
For Each 方式遍历；
Lambda 表达式遍历（JDK 1.8+）;
Streams API 遍历（JDK 1.8+）。
但每种类型下又有不同的实现方式，因此具体的遍历方式又可以分为以下 7 种：

使用迭代器（Iterator）EntrySet 的方式进行遍历；
使用迭代器（Iterator）KeySet 的方式进行遍历；
使用 For Each EntrySet 的方式进行遍历；
使用 For Each KeySet 的方式进行遍历；
使用 Lambda 表达式的方式进行遍历；
使用 Streams API 单线程的方式进行遍历；
使用 Streams API 多线程的方式进行遍历。





本文我们讲了 HashMap 4 种遍历方式：迭代器、for、lambda、stream，以及具体的 7 种遍历方法，综合性能和安全性来看，我们应该尽量使用迭代器（Iterator）来遍历 EntrySet 的遍历方式来操作 Map 集合，这样就会既安全又高效了。

~~~
        // 创建并赋值 HashMap
        Map<Integer, String> map = new HashMap();
        map.put(1, "Java");
        map.put(2, "JDK");
        map.put(3, "Spring Framework");
        map.put(4, "MyBatis framework");
        map.put(5, "Java中文社群");
        // 遍历
        Iterator<Entry<Integer, String>> iterator = map.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<Integer, String> entry = iterator.next();
            System.out.println(entry.getKey());
            System.out.println(entry.getValue());
        }
~~~








###3.Lambda 方式


小结
我们不能在遍历中使用集合 map.remove() 来删除数据，这是非安全的操作方式，但我们可以使用迭代器的 iterator.remove() 的方法来删除数据，这是安全的删除集合的方式。同样的我们也可以使用 Lambda 中的 removeIf 来提前删除数据，或者是使用 Stream 中的 filter 过滤掉要删除的数据进行循环，这样都是安全的，当然我们也可以在 for 循环前删除数据在遍历也是线程安全的。

总结
本文我们讲了 HashMap 4 大类(迭代器、for、lambda、stream)遍历方式，以及具体的 7 种遍历方法，**除了 Stream 的并行循环**，其他几种遍历方法的性能差别不大，但从简洁性和优雅性上来看，Lambda 和 Stream 无疑是最适合的遍历方式。除此之外我们还从「安全性」方面测试了 4 大类遍历结果，从安全性来讲，我们应该使用迭代器提供的 iterator.remove() 方法来进行删除，这种方式是安全的在遍历中删除集合的方式，或者使用 Stream 中的 filter 过滤掉要删除的数据再进行循环，也是安全的操作方式。

总体来说，本文提供了 7 种方式肯定也不是最全的，我是想给读者在使用 HashMap 时多一种选择，然而选择那一种形式的写法，要综合：性能、安全性、使用环境的 JDK 版本以及优雅性和可读性等方面来综合考虑。
