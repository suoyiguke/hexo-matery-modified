---
title: 坑-List的remove(Object-o-)-只是删除第一个匹配的元素.md
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
不是我们想象的那样删除所有的指定元素。如果想删除所有指定元素。请使用removeAll
~~~
        List<String> list = new ArrayList<>();
        list.add("abc");
        list.add("abc");
        list.add("def");
        list.add("def");
        list.remove("def");
        //[abc, abc, def]
        System.out.println(list);
~~~

removeAll
~~~
        List<String> list = new ArrayList<>();
        list.add("abc");
        list.add("abc");
        list.add("def");
        list.add("def");
        list.removeAll(Collections.singleton("def"));
        //[abc, abc]
        System.out.println(list);
~~~


