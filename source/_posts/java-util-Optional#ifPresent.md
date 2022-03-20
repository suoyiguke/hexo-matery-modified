---
title: java-util-Optional#ifPresent.md
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
ifPresent 用于对过滤出的数据如果存在。如果经过过滤条件后，有数据的话就可以进行修改。
~~~

 Optional<A> firstA= AList.stream() 
                          .filter(a -> "小明".equals(a.getUserName())) 
                          .findFirst()
                          .ifPresent(a -> {
                              a.setUserName("明明");
                          })

~~~
