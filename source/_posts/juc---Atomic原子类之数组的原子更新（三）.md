---
title: juc---Atomic原子类之数组的原子更新（三）.md
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
title: juc---Atomic原子类之数组的原子更新（三）.md
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
通过原子的方式更新数组里的某个元素，Atomic包提供了以下3个类。
- AtomicIntegerArray：原子更新整型数组里的元素。
- AtomicLongArray：原子更新长整型数组里的元素。
- AtomicReferenceArray：原子更新引用类型数组里的元素。




>AtomicIntegerArray类主要是提供原子的方式更新数组里的整型，其常用方法如下。
>- int addAndGet（int i，int delta）：以原子方式将输入值与数组中索引i的元素相加。
>- boolean compareAndSet（int i，int expect，int update）：如果当前值等于预期值，则以原子方式将数组位置i的元素设置成update值
