---
title: 数据校验之-org-springframework-util-Assert.md
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
title: 数据校验之-org-springframework-util-Assert.md
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
~~~
    public static void main(String[] args) {
        String name = "";
//        Assert.hasText(name, "名字不能为空");

        Integer age = null;
//        Assert.notNull(age, "年龄不能为空");

        Integer height = 180;
        Assert.isTrue(height > 185, "身高不能低于185");
    }
~~~
只要在全局异常处理IllegalArgumentException即可。但个人觉得还是自己封装自由度高一些，所以我们按照这个思路，写一个ValidatorUtils。
