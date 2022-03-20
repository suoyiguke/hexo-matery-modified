---
title: 再谈-Comparator比较器.md
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
###结合lambda使用
Arrays.sort(people, Comparator.comparing(Person::getName));

###设置次级排序

Collections.sort(list,Comparator.comparing(MachineInfo::getApp).thenComparing(MachineInfo::getIp).thenComparingInt(MachineInfo::getPort));


###comparinglnt 避免装箱的比较器
另外， comparing 和 thenComparing 方法都有变体形式，可以避免 int、 long 或 double 值
的装箱。要完成前一个操作， 还有一种更容易的做法：
Arrays.sort(people, Comparator.comparingInt(p -> p.getNameO -length()));

### 空安全的比较器
如果键函数可以返回 null, 可 能 就 要 用 到 nullsFirst 和 nullsLast 适配器。这些静态方
法会修改现有的比较器，从而在遇到 null 值时不会抛出异常， 而是将这个值标记为小于或
大于正常值。

Arrays.sort(peopleList, comparing(Person::getMiddleName , nulIsFirst(naturalOrder())));

和其他结合使用
~~~
DATAGROUPS = list.stream()
                .sorted(Comparator.nullsFirst(Comparator.comparing(MgbDictData::getDictType)
                .thenComparing(MgbDictData::getDictSort)
                .thenComparing(MgbDictData::getDictValue)))
                .collect(Collectors.groupingBy(MgbDictData::getDictType));
~~~

### reverseOrder 逆序
静态 reverseOrder 方法会提供自然顺序的逆序。要让比较器逆序比较， 可以使用 reversed
实例方法c 例如 naturalOrder().reversed() 等同于 reverseOrder()


