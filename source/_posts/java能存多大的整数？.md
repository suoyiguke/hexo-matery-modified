---
title: java能存多大的整数？.md
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
无限，内存有多大，他就能存多大的数。
使用BigInteger 
~~~
    BigInteger bigInteger = new BigInteger("9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999");
        System.out.println(bigInteger);
~~~
