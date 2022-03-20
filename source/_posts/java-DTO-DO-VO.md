---
title: java-DTO-DO-VO.md
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
《阿里巴巴开发手册》以及网上各种博客或多或少都有提到诸如DTO、DO、BO、PO、VO等等，也提倡对实体类进行分层。至于为什么要分层，它们的理由是“避免暴露内部设计细节，只展示必要的字段”，但我个人最大的感受其实是“解耦”。我曾遇到一件无奈的事，接口已经开发完毕，前后端也联合好了，结果产品临时要大改，Service层的逻辑基本要推倒重来，连查的表都不一样了。好在得益于DTO和VO的隔离，并没有影响到其它层，前端甚至完全不知道后端全部重写了，Swagger文档也和原来一模一样...

不过个人觉得没必要去扣这些概念，比如BO、PO是啥我也记不清。一般来说，POJO分为三类即可：
-  客户端/前端传入的DTO
- 与数据库字段映射的DO
- 返回给客户端/前端的VO

DO和VO一般没太多争议，至于DTO，有些公司又会细分各种O，至于有没有必要，则是仁者见仁智者见智了。


使用DTO DO VO的话，自然就避免不了`对象的深拷贝`了。

数据从DTO->DO 持久化到数据库中。
DO->VO 数据从库中出来放到视图模型VO中返回给前端。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-3b6ccdf84cd15863.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
