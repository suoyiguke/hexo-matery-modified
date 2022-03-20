---
title: 范围查询和等值查询的EXPLAIN-猜测.md
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
title: 范围查询和等值查询的EXPLAIN-猜测.md
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
###范围查询
失效： type等于ALL，key空 、fitered小于100、 rows非常大、 ref为空、`Using where`


生效: type等于range，key有值 、fitered等于100、 rows小、  Using where; Using index、ref为空




###等值查询
等值查询不生效：ALL 、key为空、ref为空、rows非常大、fitered等于1、`Using where`

等值查询生效：type等于ref、key不为空、ref等于const（多个的话就有多个const）、rows小，fitered等于100、Extra为空

