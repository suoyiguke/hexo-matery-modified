---
title: mybatis_plus-中的坑.md
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
title: mybatis_plus-中的坑.md
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
1、必须加.last("limit 1") 否则可能 selectOne()报错
 源码：JgOrderTemplate template = templateService.query().eq("template_no", templateNo).one();

    改：    JgOrderTemplate template = templateService.query().eq("template_no", templateNo).last("limit 1").one();

