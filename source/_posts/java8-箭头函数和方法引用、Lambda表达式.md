---
title: java8-箭头函数和方法引用、Lambda表达式.md
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


~~~
filter(p -> p.getAge()>18)
~~~
p方法参数 -> p.getAge()>18 方法内容

这里是将整个箭头函数作为参数传递给map方法。map方法源码如下：
~~~
   public<U> Optional<U> map(Function<? super T, ? extends U> mapper) {
        Objects.requireNonNull(mapper);
        if (!isPresent())
            return empty();
        else {
            return Optional.ofNullable(mapper.apply(value));
        }
    }
~~~
可以看到map方法的参数是：
>Function<? super T, ? extends U> mapper

第一眼看成两个参数举个手~，其实只有一个类型为`Function<? super T, ? extends U>`的mapper参数;
故这就是箭头函数的类型`Function`


