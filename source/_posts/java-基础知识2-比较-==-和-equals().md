---
title: java-基础知识2-比较-==-和-equals().md
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
### == 的用法
**`不推荐`== 使用在数值类型之间**
1、 == 使用在包装类型之间，比较的是引用地址

java中对于Integer var=?在-128至127之间的赋值，Integer对象是在IntegerCache.cache产生，会复用已有对象，这个区间内的Integer值可以直接使用==进行判断，但是这个区间之外的所有数据，都会在堆上产生，并不会复用已有对象，这是一个大坑，`推荐使用equals方法进行判断`。
~~~
Integer a1 = -129;
Integer b1 = -129;
System.out.println(a1==b1);//false

Integer a2 = 128;
Integer b2 = 128;
System.out.println(a2==b2);//flase
~~~

2、== 两边如果有一个是基本类型的话，比较的是内容
~~~
Integer a1 = -129;
int b1 = -129;
System.out.println(a1==b1);//true

Integer a2 = 128;
int b2 = 128;
System.out.println(a2==b2);//true
~~~
**==`不推荐`使用在String之间**
因为jvm中存在字符串常量池，String a = "yinkai" 的字符串实际上存在常量池里面。而new String("yinkai")在jvm堆内存里；因为==比较的是引用，所以返回false
~~~
String a = "yinkai";
String b = new String("yinkai");
System.out.println(a == b);//false
~~~


###equals()的用法
**1、`推荐`字符串之间的比较使用equals()**
~~~
String a = "yinkai";
String b = new String("yinkai");
System.out.println(a.equals(b));//true
~~~

**2、`推荐`数值类型之间的比较使用equals()**

~~~

		/**
		 * -128  127
		 */
Integer a1 = -129;
Integer b1 = -129;
System.out.println(a1==b1);//false
System.out.println(a1.equals(b1));//true

Integer a2 = -128;
Integer b2 = -128;
System.out.println(a2==b2);//true
System.out.println(a2.equals(b2));//true
~~~

**3、`推荐`Long 与 int 比较时使用equals()是个大坑！**
看代码：
~~~
   @Test
    public  void demo2(){
        Integer integer100 = 100;
        int int100 = 100;
        Long long200 = 200l;
        System.out.println(long200.equals(integer100 + int100));
    }
~~~

结果输出为false。 
分析过程： 
①integer100+int100就会得到一个类型为int且value为200的基础数据类型a 
②Long的equals方法将a进行装箱，装箱所得到的是类型为Integer的对象b 
③因为b与long200为不同的类型的对象，所以输出false；

总结：Long 与 相同值的 包装类 用equals比较时，如果传入的类型不是Long,那么全部返回false


###结论
- String使用equals()比较
- 数值使用equals()比较

###测试
~~~
  public static void main(String[] args){
        System.out.println("==========test1========");
        test1();
        System.out.println("==========test2========");
        test2();
        System.out.println("==========test3========");
        test3();
        System.out.println("==========test4========");
        test4();
        System.out.println("==========test5========");
        test5();
        System.out.println("==========test6========");
        test6();
        System.out.println("==========test7========");
        test7();


    }
    public static void test1(){
        Integer m=127;
        Integer n=127;
        System.out.println(m==n);//true
        System.out.println(m.equals(n));//true
    }
    public static void test2(){
        Integer m=127;
        int n=127;
        System.out.println(m==n);//true
    }
    public static void test3(){
        Integer m=127;
        Integer n=new Integer(127);
        System.out.println(m==n);//false
        System.out.println(m.equals(n));//true
    }
    public static void test4(){
        Integer m=127;
        Integer n=Integer.valueOf(127);
        System.out.println(m==n);//true
        System.out.println(m.equals(n));//true
    }

    public static void test5(){
        Integer m=128;
        Integer n=128;
        System.out.println(m==n);//false
        System.out.println(m.equals(n));//true
    }
    public static void test6(){
        Integer m=128;
        int n=128;
        System.out.println(m==n);//true
    }
    public static void test7(){
        Integer m=128;
        Integer n=new Integer(128);
        System.out.println(m==n);//false
        System.out.println(m.equals(n));//true
    }
~~~


1、int 跟Integer、Integer.valueOf()、new Integer()做==比较时，只比较两者的数值，数值相等即为true.根据这个原则，test2()和test6()都是输出为true;
   `“==” 等号只要作用在基本类型之上，那么就是比较内容`
   
2、When boxing (transforming int to Integer)the compiler uses a cache for small values (-128 - 127) and reuses the same objects for the same values.
在-128-127之间时，包括边界值，Integer m=127,Integer n=Integer.valueOf(127),都会将127装箱成Integer类型，并且m和n共用同一个127的Integer类型。
根据这个原则，test1()输出为true,true;

3、当值不在-128-127之内时，Integer m=128,Integer n= 128或者Integer n=Integer.valueOf(128)，也会将128装箱成Integer类型，但这时不再重用同一个Integer对象，而是各自一个了。此时的Integer
m=128或Integer m=Integer.valueOf(128)，都相当于new了一个Integer对象。


4、当一个int数值用new创建时，无论在不在-128-127之间，都会创建一个Integer对象，而且不会重用

5、Integer m=数值和Integer m=Integer.valueOf(数值）的效果一样的，两者可以互换。他们在-128-127之内时，会重用Integer,在之外，不会重用。

看看java.lang.Integer.valueOf(int)方法的源码，就一目了然了。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9347822769ecf43e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
