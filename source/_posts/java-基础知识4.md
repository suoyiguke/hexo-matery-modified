---
title: java-基础知识4.md
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
**1、++i 和 i++的区别**

- i++先赋值后增加

- ++i 先增加后赋值

~~~
public static void main(String[] args) {
    int i = 0;
    System.out.println(i++);//0  此时i的值已经为1，i++的返回值只是执行i++之前i的副本
    System.out.println(i);//1
}
public static void main(String[] args) {
    int i = 0;
    System.out.println(++i);//1  此时i的值为1，++i的值返回值就是i的值
    System.out.println(i);//1
}
~~~
- 一个特殊的例子 i=i++;

执行i++之前i的值的副本为0，副本赋值给i了。那么输出0
~~~
public static void main(String[] args) {
    int i = 0;
    i=i++;
    System.out.println(i);//0  执行i++之前i的值的副本为0，副本赋值给i了。那么输出0
}
~~~

**2、一个".java"源文件中是否可以包括多个类（不是内部类）？有什么限制？**

- 可以有多个类，但只能有一个public的类，并且public的类名必须与文件名相一致。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-18c3d0bd55fc2f5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
有多个punlic类，报错~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9cd324d70be0e779.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 可以没有public类，类名可以不和文件名保持一致
 ![image.png](https://upload-images.jianshu.io/upload_images/13965490-0aef3498bf11c61b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



- 一个java文件里包含多个类的话，编译一个java文件会生成多个class文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9fd9561d1e34aefe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**3、数值类型的错误**

1、float i = 0.1 报错
java中出现的浮点小数默认是双精度，因此需要使用double类型来接收~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-205dfe896832492a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、Long j = 121321; 报错
java中的整数默认是int类型,如果需要直接赋值给Long类型的话。后面需要加一个L;直接赋值给long类型却是正确的！因为存在int到long的隐式类型转换
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7904ccb7806c1db0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**4、&和&&的区别**
 - &&具有`短路`的功能，即如果第一个表达式为false，则不再计算第二个表达式；例如，对于if(str != null && !str.equals(“”))表达式，当str为null时，后面的表达式不会执行，所以不会出现NullPointerException如果将&&改为&，则会抛出NullPointerException异常。

- &还可以用作`位运算符`，当&操作符两边的表达式不是boolean类型时，&表示按位与操作，我们通常使用0x0f来与一个整数进行&运算，来获取该整数的最低4个bit位，例如，0x31 & 0x0f的结果为0x01。 

**5、switch语句变量类型**
- 在jdk 1.7 之前，switch 只能支持 byte、short、char、int 这几个基本数据类型和其对应的封装类型。switch后面的括号里面只能放int类型的值，但由于byte，short，char类型，它们会 自动 转换为int类型（精精度小的向大的转化），所以它们也支持。

- Jdk1.7之后整型、枚举类型，boolean，字符串都可以。

**6、char型变量中能不能存贮一个中文汉字？**
　char型变量是用来存储Unicode编码的字符的，unicode编码字符集中包含了汉字，所以，char型变量中当然可以存储汉字啦。不过，如果某个特殊的汉字没有被包含在unicode编码字符集中，那么，这个char型变量中就不能存储这个特殊汉字。补充说明：`unicode编码的汉字占用两个字节`，所以，char类型的变量也是占用两个字节。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1adedb499236b9bf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  编译后
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c60a0b7762ca4fc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**7、使用final关键字修饰一个引用变量时，是引用不能变，还是引用的对象不能变？**
　使用final关键字修饰一个变量时，是指引用变量不能变，引用变量所指向的对象中的内容还是可以改变的。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c5f2e3e9a3b67a12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**8、java中构造对象的几种方式**

- 用`new`语句创建对象，这是最常见的创建对象的方法。显式的调用构造函数 
-  运用`反射`手段,调用java.lang.Class或者java.lang.reflect.Constructor类的newInstance()实例方法。
- 调用对象的`clone()`方法。是在内存上对已有对象的影印，所以不会调用构造函数 
- 运用`反序列化`手段，调用java.io.ObjectInputStream对象的 readObject()方法。是从文件中还原类的对象，也不会调用构造函数。

**9、ArrayList list = new ArrayList(20);中的list扩容次数**
我们知道ArrayList 的初始容量为10，加载因子为0.75，扩容为原来的1.5倍。但是这里构造list的时候传入了20为初始容量，所以不会进行扩容

**10、为什么泛型不可以有基本类型**
因为Java中的泛型是通过编译时的`类型擦除`来完成的，当泛型被类型擦除后都变成Object类型。但是Object类型不能指代像int，double这样的基本类型只能指代Integer，Double这样的引用类型。

