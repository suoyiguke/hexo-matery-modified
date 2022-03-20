---
title: 证明-newString1-会创建两个对象.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: 证明-newString1-会创建两个对象.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
######证明 new String("1") 会创建两个对象
~~~
        String s3 = new String("1");
        String intern = s3.intern();
        System.out.println(s3 == intern);
~~~

打印false，说明字符串常量池中对象的引用和堆中对象的引用不同。说明s3.intern()又在字符串常量池中创建了一个对象。在加上new String("1")在堆上创建的对象，那么就是2个了


######证明 new String("1") 会创建一个对象

~~~
String s1 = new String("1");
String intern1 = s1.intern();

 String s2 = new String("1");
 String intern2 = s2.intern();

 System.out.println(intern1 == intern2);
~~~

1、两个intern的返回值比较打印true，说明 s2.intern();只是复用了之前在字符串常量池中生成的对象，并没有再次创建对象
2、毋庸置疑，new String("1");肯定在堆上创建了对象，因此 此时 new String("1") 只会创建一个对象
