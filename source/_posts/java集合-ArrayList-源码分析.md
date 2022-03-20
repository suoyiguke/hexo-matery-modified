---
title: java集合-ArrayList-源码分析.md
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
title: java集合-ArrayList-源码分析.md
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
###基本方法
1、public boolean contains(Object o) 判断是否包含某元素，若list里存的是复合类型，请重写元素的equals和hashcode。因为contains实际调用是indexOff。里面使用equals实现的。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-75c4e37295e9855d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###源码解析
1、 无参构造
如果没有指定容量初始化一个ArrayList，那么是一个空数组 {}
![image.png](https://upload-images.jianshu.io/upload_images/13965490-553629886df55d6d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

要到第一次add元素时才会有
如果是空数组，初始容量为默认容量10和指定数值中较大的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d5a291a64c524b39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、初始容量10
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6e56187df0e55156.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、扩容大小 变成原来的1.5倍
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7777b270e7649293.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、加载因子 0.75  （扩容触发条件）只要超过原来的容量就会扩容

