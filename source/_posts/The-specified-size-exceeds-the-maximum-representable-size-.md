---
title: The-specified-size-exceeds-the-maximum-representable-size-.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: The-specified-size-exceeds-the-maximum-representable-size-.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
The specified size exceeds the maximum representable size.



    使用32位的jvm支持的内存也最多为2的32次方，就是4G。

    出现此问题是jvm设置的最大内存大于32位jvm最大支持内存。换为64位的jdk即可。
