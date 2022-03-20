---
title: Lazy.md
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
title: @Lazy.md
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
背景：一个接口有两个实现类，根据配置切换不同的实现类。现在是spring启动会自动初始化两个，当其实我们只需使用一个，另一个的加载就是浪费资源！此时我们就可以使用@Lazy注解来达到只加载我们需要的！

1、在实现类上加上 @Lazy
2、在 @Autowired注入的地方也加上 @Lazy
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1c38d77eae82d4b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
