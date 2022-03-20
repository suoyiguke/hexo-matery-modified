---
title: synchronized-锁不住-Integer-类型解决.md
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
title: synchronized-锁不住-Integer-类型解决.md
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
但是运行起来好像是锁不住，debug了一下看了一下，因为userId是Intefer类型的所以每次获取到的userId的地址值都是不一样的，所以根本没法锁。
然后我就想到了把Integer类型转换成String类型来使用，后来一弄还是不行，然后研究了研究发现好像新建的String类型是在堆中的，并不是在字符串常量池，这个时候我就想到了使用intern()方法，使其返回字符串常量池中的地址,然后就成功的锁住了
