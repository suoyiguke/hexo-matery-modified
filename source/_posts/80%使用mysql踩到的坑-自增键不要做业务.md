---
title: 80%使用mysql踩到的坑-自增键不要做业务.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: 80%使用mysql踩到的坑-自增键不要做业务.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
1、用户数量信息泄露
2、如果mysql主键因为人为因素导致又从1开始，那么对整个应用都是毁灭性打击的！
3、双主同步写的时候会导致更新丢失

