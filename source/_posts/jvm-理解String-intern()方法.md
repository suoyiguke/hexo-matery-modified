---
title: jvm-理解String-intern()方法.md
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
title: jvm-理解String-intern()方法.md
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
> 十年磨一剑


如下，我们先来看个例子。没有实践的理论总是枯燥的~
>   String s1 = "yin";
     String intern = s1.intern();
     System.out.println(s1 == intern);

如上代码，调用s1的intern方法，先到常量池中找"yin"这个字面量。找到了直接返回常量池中的引用，没找到则将s2指向的对象加入到常量池中再返回引用。当然这里是从常量池中找到了"yin"这个字面量，随后将常量池中的引用返回，赋值给了intern 变量。因此s1和intern两个变量指向的引用是相同的，均是指向常量池中的对象。那么s1 == intern打印true。

再来看看这个例子
>   String s1 = new String("yin");
     String intern = s1.intern();
     System.out.println(s1 == intern);

如上代码，s1的引用指向堆中的对象。调用s1的intern方法，先到常量池中找"yin"这个字面量，这里还是能找到的，因为 new String("yin")会在这里创建两个对象，一个在常量池中一个在堆中。那么将常量池中的对象返回引用赋值给intern ，所以intern 引用指向常量池中的对象。因为s1和intern 变量指向不同的对象， 所以s1 == intern打印false。



`总而言之， intern()方法的返回值总是常量池中字符串的引用`

>- 但是要注意啊，若s1是以new的方式构造的字符串。那么调用了intern()方法，只是将堆中的对象copy一份到字符串常量池中。本身s1还是引用堆中的对象的，堆中的对象仍然存在。而且堆中的对象和常量池中的对象的引用是不同的；
>- 若s1是以引号的形式构造的字符串，那么这个对象本身就在字符串常量池中。调用了intern()方法，只是将常量池中对象的引用返回。








######案例一
> //s1指向常量池中的对象
String s1 = "yin";
> //s2指向堆中的对象（虽然说java7之后字符串常量池加入到了堆中，但s1和s2确实指向的是不同的对象）
String s2 = new String("yin");
//调用s2的intern方法，先到常量池中找"yin"这个字面量。找到了直接返回，没找到则将s2指向的对象加入到常量池中再返回引用
//这里肯定是找到了，于是将常量池中已经有的"yin"字面量的引用返回
> String intern = s2.intern();
//所以，intern引用和s1的引用是一样的。打印true
System.out.println(intern == s1);
//intern引用常量池中的对象，s2引用堆上的对象，打印false
System.out.println(intern == s2);
//s1引用常量池中的对象，s2引用堆上的对象，打印false
System.out.println(s1 == s2);


######案例二
>//s1指向常量池中的对象
String s1 = "yin";
//调用s1的intern方法，先到常量池中找"yin"这个字面量。找到了直接返回，没找到则将s1指向的对象加入到常量池中再返回引用
//这里是找到了，直接返回常量池中的引用
String intern = s1.intern();
//s2指向堆中的对象
String s2 = new String("yin");
//intern和s1均是常量池中的引用，所以打印true
System.out.println(intern == s1);
//s2是堆中的引用，打印flase
System.out.println(intern == s2);
//s1是常量池中的引用，s2是堆中的引用，打印false
System.out.println(s1 == s2);
######案例三

>String s1 = "yin";
String intern1 = s1.intern();
String s2 = new String("yin");
String intern2 = s1.intern();
//true
System.out.println(intern1 == s1);
//false
System.out.println(intern1 == s2);
//true
System.out.println(intern2 == s1);
//false
System.out.println(intern2 == s2);
//true
>System.out.println(intern1 == intern2);
//false
System.out.println(s1 == s2);
