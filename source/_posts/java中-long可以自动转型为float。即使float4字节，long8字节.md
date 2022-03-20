---
title: java中-long可以自动转型为float。即使float4字节，long8字节.md
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
~~~
        long zz = 1111111111111111111L;
        double d = zz;
        float f = zz;
        //false
        System.out.println(Double.valueOf(d).equals(f));
~~~

首先范围上讲float范围要大，另外，float精度要低，用的是幂指数方式表示数值，小数精度为7位。long表示更精确一些，没有估计数值。
