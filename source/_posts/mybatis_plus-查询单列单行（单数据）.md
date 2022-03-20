---
title: mybatis_plus-查询单列单行（单数据）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis_plus-查询单列单行（单数据）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---

一般用作单行查询
~~~
        Object obj = jgRulaEmbargoService.getObj(Wrappers.<JgRulaEmbargo>query().select("1").eq("commodity_sku","K.124.1381.202102030222,K.35.10704.202201130012") .last(Constant.LIMIT_1), o -> o);
        System.out.println(obj);


        Long o = (Long) jgRulaEmbargoService.getObj(Wrappers.<JgRulaEmbargo>lambdaQuery().select(JgRulaEmbargo::getId).eq(JgRulaEmbargo::getCommoditySku, "K.124.1381.202102030222,K.35.10704.202201130012").last(Constant.LIMIT_1), (Function<Object, Object>) o1 -> (Long) o1);
        System.out.println(o);
~~~
