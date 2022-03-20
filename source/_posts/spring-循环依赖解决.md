---
title: spring-循环依赖解决.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: spring-循环依赖解决.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
> Bean with name 'sysDepartServiceImpl' has been injected into other beans [sysBaseApiImpl] in its raw version as part of a circular reference, but has eventually been wrapped. This means that said other beans do not use the final version of the bean. This is often the result of over-eager type matching - consider using 'getBeanNamesOfType' with the 'allowEagerInit' flag turned off, for example.. 

在注入是加上    @Lazy注解
比如
>    @Autowired
    @Lazy
    private ISysBaseAPI sysBaseAPI;
