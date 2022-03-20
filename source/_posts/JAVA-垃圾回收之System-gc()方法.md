---
title: JAVA-垃圾回收之System-gc()方法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
---
title: JAVA-垃圾回收之System-gc()方法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
在默认情况下， System.gc()会显式直接触发 Full GC，同时对老年代和新生代进行回收 。 而一般情况下，垃圾回收应该是自动进行的，无须手工触发 ， 否则就太过于麻烦了 。 如果过于频繁地触发垃圾回收，对于系统的整体性能是没有好处的。因此虚拟机提供了 一 个选项Di sabl eExpli c itG C 来控制是否手工触发 GC 。
