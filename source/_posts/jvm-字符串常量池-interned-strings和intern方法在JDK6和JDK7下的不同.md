---
title: jvm-字符串常量池-interned-strings和intern方法在JDK6和JDK7下的不同.md
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
title: jvm-字符串常量池-interned-strings和intern方法在JDK6和JDK7下的不同.md
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
>尝试着去理解他人

我们来看一个程序，下面有4个字符串引用。s、s2、s3、s4
分别为s、s2 和 s3、s4进行两两比较
~~~

 class StringinternDemo {
     public static void main(String[] args) {
         String s = new String("1");
         s.intern();
         String s2 = "1";
         System.out.println(s == s2);
         String s3 = new String("1") + new String("1");
         s3.intern();
         String s4 = "11";
         System.out.println(s3 == s4);
     }
 }
~~~
以上代码在java6和java7、java8中输出结果不同：



######我们先看JDK1.6

![image.png](https://upload-images.jianshu.io/upload_images/13965490-29daf78ae7b8f9ce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在 JDK6 中上述的所有打印都是 false 的，尤其是s3 == s4打印false。因为 JDK6 中的常量池是放在PermGen永久区中的， PermGen 区和正常的 Java Heap 区域是完全分开的。上面说过，如果是使用引号声明的字符串都会直接在字符串常量池中生成，而 new 出来的 String 对象是放在 Java Heap 区域。所以s3在堆中，s4在PermGen 区中。 所以拿一个 Java Heap 区域的对象地址和PermGen 区中的对象地址进行比较，肯定是不相同的，即使调用 String.intem() 方法也是没有任何关系的。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-dd377d450b96aa4b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





######我们再来看JDK1.7
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ad972aad2b03d614.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

s1和s2在不同JDK版本下的比较是相同的，那么重点来看 s3 和 s4 字符串。 String s3 = new String("1") + new String("1");，这句代码中现在生成了2 个对象（其实还有2个匿名的new String("1") 对象），是字符串常量池中的“ 1 ”和 Java Heap 中的 s3 引用指向的对象 。 接下来 s3 .intern();这一句代码，是将 s3 中的“ 11 ”字符串放入 String 常量池中，因为此时常量池中不存在” 11 ”字符串，因此常规做法是像图 1-4 中表示的那样，在常量池中生成一个” 11 ”的对象，关键点是如图 1-5 所示 JDK7 中常量池不在 Perm 区域了，这块做了调整 。 常量池中不需要再存储一份对象了，可以直接存储堆中的引用 。 这份引用指向 s3 引用的对象，也就是说引用地址是相同的。最后 String s4 ＝” 11 ”；这句代码中” 11 ”是显示声明的，因此会直接去常量池中创建，创建的时候发现已经有这个对象了，此时也就是指向 s3 引用对象的一个引用 。 所以 s4 引用就指向和s3 一样了 。 因此最后的比较 s3 二 s4 是 true 。


![image.png](https://upload-images.jianshu.io/upload_images/13965490-c48e7c14144900f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###记录下自己的感悟
上面的内容来自《深入理解JVM ＆ G1 GC 》这本书。

######来看new String("1") + new String("1");的例子
~~~
String s3 = new String("1") + new String("1");
s3.intern();
String s4 = "11";
System.out.println(s3 == s4);
~~~
System.out.println(s3 == s4); 在JDK7下打印true而在JDK6下打印false的原因是：
在JDK7中 s3.intern(); 把s3指向的堆中对象 new String("11")的引用加入到了字符串常量池中；

> 有的人可能会疑惑了： 这个new String("11")是怎么来的？
   new String("1") + new String("1")其实会创建多个对象，其中就包含了这个new String("11")，具体可以看看这篇文章 https://www.jianshu.com/p/9451bfaec698

因为JDK7中已经将字符串常量池移到堆中，`所以JDK7字符串常量池可以只存堆中字符串对象的引用`，以便节省空间。这里呢就是将堆中的new String("11")的引用加入到了字符串常量池中。
那么因为s3.intern();的关系，此时s3的引用 就是 字符串常量池中"11"字面量的引用，而s4 直接指定了它的引用是"11"字面量。
由等号的传递性可得： s3的引用 就是 s4的引用。System.out.println(s3 == s4); 打印true

######有时候事情没有看似的简单，再来看这个 new String("1") 例子
~~~
 String s3 = new String("1");
 s3.intern();
 String s4 = "1";
System.out.println(s3 == s4);
~~~
它打印的是false，这就很奇怪了。上面的new String("1") + new String("1")都能打印true，这里只是用new String("1")反而打印false了？

> 首先new String("1")在这里会创建两个对象，一个在堆中的new String("1")，一个在字符串常量池中的"1"。所以 s3.intern()这条语句就不会再到字符串常量池中创建对象了，相当于是一个无效方法执行。自然s4和s3的引用不同了（s3引用堆、s4引用常量池）；
然后上面的new String("1") + new String("1")却不会在字符串常量池中创建'11'字面量，故随后的s3.intern();起作用，字符串常量池直接存储s3的引用。那么s4去常量池中找字面量，当然又复用s3的引用了


######再进行一些实验
我们把new String("1") + new String("1");例子再修改下，将中间的s3.intern();去掉。看看执行结果会怎样
~~~
String s1 = new String("1") + new String("1");
String s2 = "11";
System.out.println(s1 == s2);
~~~
这次终于打印false了，看来s3.intern();是真的在这个例子中起到作用了


再把new String("1")的例子中的s3.intern()去掉
~~~
String s1 = new String("1") ;
String s2 = "1";
System.out.println(s1 == s2);
~~~
当然还是false了

###总结

从上述的例子代码可以看出 jdk7 版本对 intern 操作和常量池都做了一定的修改。主要包括2点：

>1、将字符串常量池从Perm永久代（方法区）移动到了Java Heap堆中
2、调用 intern 方法时，若池中不存在对象但堆中存在对象，字符串常量池会直接保存堆中对象的引用，而不会重新创建对象。不过，池中已经存在对象再调用intern 方法就是无效操作了。
