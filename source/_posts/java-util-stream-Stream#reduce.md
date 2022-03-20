---
title: java-util-stream-Stream#reduce.md
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
实现用一个12345的list生成一个以"element-" 为开头元素的List
~~~
    public static void main(String[] args) {
        List<Integer> numList = Arrays.asList(1, 2, 3, 4, 5, 6);
        ArrayList<String> result = numList.stream().reduce(new ArrayList<String>(), (a, b) -> {
            a.add("element-" + Integer.toString(b));
            return a;
        }, (a, b) -> null);
        System.out.println(result);

    }
~~~

[element-1, element-2, element-3, element-4, element-5, element-6]


a 代表生成的list，b代表原始list的元素
