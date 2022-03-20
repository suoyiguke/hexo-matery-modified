---
title: 使用RamUsageEstimator计算对象占用堆内存大小.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: 使用RamUsageEstimator计算对象占用堆内存大小.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
 pom依赖

~~~
<dependency>
    <groupId>org.apache.lucene</groupId>
    <artifactId>lucene-core</artifactId>
    <version>8.3.0</version>
</dependency>
~~~

2. 计算内存大小,返回MB
~~~
private int getMb(Object obj) {
 
    if (obj == null) {
        return 0;
    }
    //计算指定对象本身在堆空间的大小，单位字节
    long byteCount = RamUsageEstimator.shallowSizeOf(obj);
    if (byteCount == 0) {
        return 0;
    }
    double oneMb = 1 * 1024 * 1024;
 
    if (byteCount < oneMb) {
        return 1;
    }
 
    Double v = Double.valueOf(byteCount) / oneMb;
    return v.intValue();
}
 ~~~
