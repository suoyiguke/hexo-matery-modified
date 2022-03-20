---
title: java-源码研究之HashSet.md
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
title: java-源码研究之HashSet.md
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
1、HashSet的底层实现是HashMap
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aed1e9332897f5b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、为什么HashSet中add进去的元素是一个，而HashMap确需要key、value两个数据
- HashSet中add进去的数据充当HashMap的key
- HashMap的value是一个Object类型的常量

![image.png](https://upload-images.jianshu.io/upload_images/13965490-fea8db48d4371581.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c7a3360074e68038.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
