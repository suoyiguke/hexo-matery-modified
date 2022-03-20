---
title: java-刷题.md
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
1、byte b = (byte)129;  
  -127

其实可以把每个数据类型范围画成一个圈，byte是从-128-127，可以这样想，从-128开始，向上加就是一步一步画圈，知道加到127，这个圆圈刚好补满了，所以127再加一就又到了-128，再加一就是129，也就是-127

2、java中的泛型相关结论
1、虚拟机中没有泛型，只有普通类和普通方法
2、所有泛型类的类型参数在编译时都会被擦除
3、创建泛型对象时请指明类型，让编译器尽早的做参数检查

3、获得参数的方法区分：如何获取ServletContext设置的参数值？
getInitParameter();

getParameter()是获取POST/GET传递的参数值；
getInitParameter获取Tomcat的server.xml中设置Context的初始化参数
getAttribute()是获取对象容器中的数据值；
getRequestDispatcher是请求转发。


4、java8中，忽略内部接口的情况，不能用来修饰interface里的方法的有（ ）
正确答案: A C   
A private
B public
C protected
D static

Java8的接口方法可以有如下定义
only public, abstract, default, static and strictfp are permitted
`java ``1.8``开始支持接口中定义静态方法


5、如果一个list初始化为{5，3，1}，执行以下代码后，其结果为（B）？
nums.add(6);
nums.add(0,4);
nums.remove(1);

 A[5, 3, 1, 6]
B [4, 3, 1, 6]
 C[4, 3, 6]
 D[5, 3, 6]

1、add(int)和两个重载
add(int) 是往后面加一位元素；
add(int a,int b) 将b插入到指定索引a处，原来a处的元素和后面的元素向后移动一位。注意不是单纯的替换
2、remove(int index) 和 remove(Object a) 两种重载
即可移除指定位置，又可按元素内容移除。移除后，后面元素往都要往前补一位

将题目修改下nums.remove((Object)1); 最终输出就是[4, 5, 3, 6]了，因为这次调用的是remove(Object a)重载乃，直接移除指定元素。


6、表达式(short)10/10.2*2运算后结果是什么类型？

double。java中默认的浮点就是double。除不断的除法运算计算结果也是double。除的断的结果是int。
~~~
double v = 10 / 2.1;
int i = 10 / 2;
~~~

10、关于protected 修饰的成员变量，以下说法正确的是
可以被该类自身、与它在同一个包中的其它类、在其它包中的该类的子类所访问


11、抽象类可以被抽象类继承

12、javac 命令参数

-d destination 目的地
-s source 起源地
javac -d 指定放置生成的类文件的位置
javac -s 指定放置生成的源文件的位置


13、构造函数不能被继承，构造方法只能被显式或隐式的调用。


14、

~~~
class Animal{
    public void move(){
        System.out.println("动物可以移动");
    }
}
class Dog extends Animal{
    public void move(){
        System.out.println("狗可以跑和走");
    }
    public void bark(){
        System.out.println("狗可以吠叫");
    }
}
public class TestDog{
    public static void main(String args[]){
        Animal a = new Animal();
        Animal b = new Dog(); 
        a.move();
        b.move();
        b.bark();
    }
}
~~~

编译错误！

>编译看左边，运行看右边。 父类型引用指向子类型对象，无法调用只在子类型里定义的方法
