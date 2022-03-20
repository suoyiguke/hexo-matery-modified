---
title: mybatis_plus-最好写的query.md
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
title: mybatis_plus-最好写的query.md
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
     1、 List<MbUndertakesOrderDto> exitList = imgbUndertakesOrderDtoService.list(Wrappers.<MbUndertakesOrderDto>lambdaQuery().select(MbUndertakesOrderDto::getOriginalPlatformOrderNo)
                .in(MbUndertakesOrderDto::getOriginalPlatformOrderNo, list));

