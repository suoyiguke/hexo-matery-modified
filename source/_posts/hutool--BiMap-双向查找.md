---
title: hutool--BiMap-双向查找.md
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
title: hutool--BiMap-双向查找.md
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
~~~
        BiMap<String, Integer> biMap = new BiMap<>(new HashMap<>());
        biMap.put("aaa", 111);
        biMap.put("bbb", 222);

        biMap.get("aaa");
        biMap.get("bbb");

        biMap.getKey(111);
        biMap.getKey(222);
~~~
