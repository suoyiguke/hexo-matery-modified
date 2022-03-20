---
title: java8-map和flatMap区别.md
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
**我们先来了解什么是流的扁平化**

对比下面两个例子，观察他们的输出结果
eg1
~~~
   public static void main(String[] args) {
        List<String> list = Arrays.asList("A,a", "B,b","C,c");
        List<String[]> collect = list.stream().map(s -> s.split(",")).collect(Collectors.toList());
        System.out.println(JSON.toJSONString(collect));

    }
~~~
>[["A","a"],["B","b"],["C","c"]]

eg2
~~~ 
   public static void main(String[] args) {
        List<String> list = Arrays.asList("A,a", "B,b","C,c");
        List<String> collect = list.stream().map(s -> s.split(",")).flatMap(Arrays::stream)
            .collect(Collectors.toList());
        System.out.println(collect);
    }
~~~
>[A, a, B, b, C, c]


eg2只是比eg1多个一步flatMap(Arrays::stream)。这样他们两个的结果就不相同了。
map返回了List<String[]>，而flatMap返回了 List<String>。flatMap返回值维度比map小了一个级别。

整个过程可以简单示意如下：


![image.png](https://upload-images.jianshu.io/upload_images/13965490-c74c6c9f87feab06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



