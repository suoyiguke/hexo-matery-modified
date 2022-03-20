---
title: juc---Atomic原子类之引用类型的原子更新（四）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: juc---Atomic原子类之引用类型的原子更新（四）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
原子更新基本类型的AtomicInteger，只能更新一个变量，如果要原子更新多个变量，就需
要使用这个原子更新引用类型提供的类。Atomic包提供了以下3个类。
·AtomicReference：原子更新引用类型。
·AtomicReferenceFieldUpdater：原子更新引用类型里的字段。
·AtomicMarkableReference：原子更新带有标记位的引用类型。可以原子更新一个布尔类
型的标记位和引用类型。构造方法是AtomicMarkableReference（V initialRef，boolean
initialMark）。
以上几个类提供的方法几乎一样，所以本节仅以AtomicReference为例进行讲解，
