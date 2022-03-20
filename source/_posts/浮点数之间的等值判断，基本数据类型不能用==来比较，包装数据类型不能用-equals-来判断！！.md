---
title: 浮点数之间的等值判断，基本数据类型不能用==来比较，包装数据类型不能用-equals-来判断！！.md
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
## BigDecimal

### BigDecimal 的用处

《阿里巴巴Java开发手册》中提到：**浮点数之间的等值判断，基本数据类型不能用==来比较，包装数据类型不能用 equals 来判断。** 具体原理和浮点数的编码方式有关，这里就不多提了，我们下面直接上实例：
~~~
        float a = 1.0f - 0.9f;
        float b = 0.9f - 0.8f;
        System.out.println(a);
        System.out.println(b);
        // false
        System.out.println(a == b);
        System.out.println(a == b);

        Float c = 1.0f - 0.9f;
        Float d = 0.9f - 0.8f;
        System.out.println(c);
        System.out.println(d);
        //false
        System.out.println(Objects.equals(c,d));
~~~
具有基本数学知识的我们很清楚的知道输出并不是我们想要的结果（**精度丢失**），我们如何解决这个问题呢？一种很常用的方法是：**使用 BigDecimal 来定义浮点数的值，再进行浮点数的运算操作。**
~~~
BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("0.9");
BigDecimal c = new BigDecimal("0.8");

BigDecimal x = a.subtract(b); 
BigDecimal y = b.subtract(c); 

System.out.println(x); /* 0.1 */
System.out.println(y); /* 0.1 */
System.out.println(Objects.equals(x, y)); /* true */
~~~
### BigDecimal 的大小比较

`a.compareTo(b)` : 返回 -1 表示 `a` 小于 `b`，0 表示 `a` 等于 `b` ， 1表示 `a` 大于 `b`。
~~~
BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("0.9");
System.out.println(a.compareTo(b));// 1
~~~
### BigDecimal 保留几位小数

通过 `setScale`方法设置保留几位小数以及保留规则。保留规则有挺多种，不需要记，IDEA会提示。
~~~
BigDecimal m = new BigDecimal("1.255433");
BigDecimal n = m.setScale(3,BigDecimal.ROUND_HALF_DOWN);
System.out.println(n);// 1.255</pre>
~~~
### BigDecimal 的使用注意事项

注意：我们在使用BigDecimal时，为了防止精度丢失，推荐使用它的 **BigDecimal(String)** 构造方法来创建对象。《阿里巴巴Java开发手册》对这部分内容也有提到如下图所示。

![《阿里巴巴Java开发手册》对这部分BigDecimal的描述](https://upload-images.jianshu.io/upload_images/13965490-56ca015bd1d3ebf0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
        //0.1000000000000000055511151231257827021181583404541015625
        System.out.println(new BigDecimal(0.1));

        //0.1
        System.out.println(new BigDecimal("0.1"));


        //0.1
        System.out.println(BigDecimal.valueOf(0.1));
~~~
### 总结

BigDecimal 主要用来操作（大）浮点数，BigInteger 主要用来操作大整数（超过 long 类型）。

BigDecimal 的实现利用到了 BigInteger, 所不同的是 BigDecimal 加入了小数位的概念
