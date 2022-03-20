---
title: spring-StringUtils-split的坑.md
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
title: spring-StringUtils-split的坑.md
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
   
        String[] split1 = org.apache.commons.lang.StringUtils.split("aaaa,bbbb,cccc", Constant.COMMA);
        System.out.println(split1.length);
        System.out.println(Arrays.asList(split1));

        String[] split2 = org.springframework.util.StringUtils.split("aaaa,bbbb,cccc", Constant.COMMA);
        System.out.println(split2.length);
        System.out.println(Arrays.asList(split2));
~~~
3
[aaaa, bbbb, cccc]
2
[aaaa, bbbb,cccc]

spring家的StringUtils.split有问题，只会拆一次，请认准apache的包使用。不然掉坑里了
