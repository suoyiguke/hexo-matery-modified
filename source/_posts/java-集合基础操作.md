---
title: java-集合基础操作.md
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
1、map 边遍历边删除

~~~
   Iterator<Entry<String, Cache>> it = cacheMap.entrySet().iterator();
        while (it.hasNext()) {
            Entry<String, Cache> next = it.next();
            GuavaCache value = (GuavaCache)  next.getValue();
            if (value.isEmpty(next.getKey())) {
                it.remove();
            }
        }

~~~
