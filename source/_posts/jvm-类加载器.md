---
title: jvm-类加载器.md
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
title: jvm-类加载器.md
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
###什么是类加载器
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8df71041b3e80fa2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

负责加载class文件，`class文件在文件开头由特定的文件标识`，将class文件字节码内容加载到内存中，并将这些内容转换成方法区中的运行时数据结构并且`ClassLoader只负责class文件的加载`，至于它是否可以运行，则由Execution Engine（执行引擎）决定。

class文件开头特点的标志：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a28c87a9ebd46aff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


.java文件==编译===>.class文件==通过ClassLoader加载===>类模板

###java中有四种类加载器
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e1722a02222b7348.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####启动类加载器(Bootstrap) 使用C++编写

- object是对象，getClass()是类模板,getClassLoader()是该类模板的加载器，`Object类的加载器打印出来是null`
- 其实就是类启动类加载器(Bootstrap) ，如果是jdk自带的类走的就是Bootstrap加载器
- Object类之所以可以直接使用，是因为Bootstrap加载器加载了Object类(rt.jar包被加载)
- jr 是runtime的缩写，表示java运行时必要；rt.jar包括 java.lang和java.util的核心包
~~~
Object object = new Object();
System.out.println(object.getClass().getClassLoader());//null
~~~

####扩展类加载器(Extension) 使用Java编写
- jdk安装路径下的\jre\lib\ext文件夹的jar包都是会被Extension加载器加载的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-81b763857ece2bb4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
查看其中的zipfs.jar，com.sun.nio.zipfs.ZipInfo类
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4a8a943725a61d29.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
打印下该类的加载器，果然是ExtClassLoader
~~~
 //sun.misc.Launcher$ExtClassLoader@42110406
ZipInfo zipInfo = new ZipInfo();
System.out.println(zipInfo.getClass().getClassLoader());
~~~
- AppClassLoader的父加载器也是ExtClassLoader
~~~
ClassLoader classLoader = MybatisAutoConfiguration.class.getClassLoader();   System.out.println(classLoader.getParent());//sun.misc.Launcher$ExtClassLoader@446cdf90
~~~
####应用程序类加载器(AppClassLoader)
也叫系统类加载器，加载当前应用的classpath下的所有类
- java程序员自己定义的类就是使用AppClassLoader加载的
- 当然包括咱们熟知的spring、mybatis框架等，都是使用AppClassLoader加载的
~~~
ClassLoader classLoader = Test.class.getClassLoader();
System.out.println(classLoader); //sun.misc.Launcher$AppClassLoader@58644d46
~~~

####用户自定义加载器
Java.lang.ClassLoader的子类，用户可以定制类的加载方式


###ClassLoader的双亲委派机制保证了沙箱安全
- 现在我要找a.class这样的类，先去Bootstrap根加载器中找；找不到再到Extension拓展类加载器中找；没找到再到AppClassLoader应用类加载器中找
- 如果都没找到就会抛出classNotFindExption异常表示没有找到该class
- 先找到class就先使用，后面的相同的class(相同包名、相同类名)被忽略
- 双亲委派机制就是为了保护jdk源代码不被覆盖不被用户定义的类污染而存在的


####举个例子
1、自己定义一个java.lang.String 类
~~~
package java.lang;

public class String {
    public static void main(String[] args) {
        System.out.println("123123");
    }
}
~~~
运行，报错；表示该类中不存在main方法；因为先到Bootstrap根加载器中找java.lang.String(rt.jar)找到了，而那个String类不存在main方法。所以报错了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-36a072b55c1ddcdb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、同样再新建一个com.sun.nio.zipfs.ZipInfo类，这个类属于扩展类加载器(Extension) 加载的
~~~
package com.sun.nio.zipfs;
public class ZipInfo {
    public static void main(String[] args) {
        System.out.println("hahahaha");
    }
}

~~~
输出一段字符串；在第二级别的Extension加载器中找到了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-62cde9464c24011a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看看com.sun.nio.zipfs.ZipInfo类源码，果然有输出；自己定义的字符串没有得到输出，因为自己定义的类没有得到加载
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f370a08b8af11bfa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

