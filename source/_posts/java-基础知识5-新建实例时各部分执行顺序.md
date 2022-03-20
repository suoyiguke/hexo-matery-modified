---
title: java-基础知识5-新建实例时各部分执行顺序.md
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
我们先来看一个例子
~~~
package test;


class HelloA {
    public HelloA() {
        System.out.println("父类构造器执行");
    }

    {
        System.out.println("父类实例块 1 执行");
    }
    {
        System.out.println("父类实例块 2 执行");
    }

    static {
        System.out.println("父类静态块 1 执行");
    }
    static {
        System.out.println("父类静态块 2 执行");
    }

}

 class HelloB extends HelloA {
    public HelloB() {
        System.out.println("子类构造器执行");
    }

    {
        System.out.println("子类实例块 1 执行");
    }
     {
         System.out.println("子类实例块 2 执行");
     }

    static {
        System.out.println("子类静态块 1 执行");
    }
     static {
         System.out.println("子类静态块 2 执行");
     }

    public static void main(String[] args) {
        System.out.println("执行 new HelloB()");
        new HelloB();//①
        System.out.println("new HelloB() 执行完毕");

        System.out.println("===========================");

        System.out.println("执行 new HelloA()");
        new HelloA();//②
        System.out.println("new HelloA() 执行完毕");

    }

}
~~~
####运行结果
父类静态块 1 执行
父类静态块 2 执行
子类静态块 1 执行
子类静态块 2 执行
执行 new HelloB()
父类实例块 1 执行
父类实例块 2 执行
父类构造器执行
子类实例块 1 执行
子类实例块 2 执行
子类构造器执行
new HelloB() 执行完毕
===========================
执行 new HelloA()
父类实例块 1 执行
父类实例块 2 执行
父类构造器执行
new HelloA() 执行完毕

####上面代码的执行流程可以分析成这样流程
父类静态块 > 子类静态块 > main方法开始执行 > 执行 new 子类() ①>执行new 父类()②

①：父类实例块>父类构造器>子类实例块>子类构造器
②：子类实例块>子类构造器

- 静态块只执行一次，在main方法之前便执行
- 父类静态块在子类静态块之前执行
- 多个静态块执行顺序就是定义的顺序，由上到下执行
- 多个实例块执行顺序就是定义的顺序，由上到下执行
- 实例块在构造方法之前执行
- 父类的实例块和构造器在子类的实例块和构造器之前执行




####误区：
  1、在父类静块中访问子类静态属性，只会的到子类静态属性的默认值，因为子类还没有初始化；int类型的默认值是0，所以下面的例子打印出HelloB.i的值为0
如：
~~~

class HelloA {
    public HelloA() {
        System.out.println("父类构造器执行");
    }

    {
        System.out.println("父类实例块 1 执行");

    }
    {
        System.out.println("父类实例块 2 执行");
    }

    static {
        System.out.println("父类静态块 1 执行");
        int i = HelloB.i;
        System.out.println(i);
    }
    static {
        System.out.println("父类静态块 2 执行");
    }

}

 class HelloB extends HelloA {
    static  int i  = 1;
    public HelloB() {
        System.out.println("子类构造器执行");
    }

    {
        System.out.println("子类实例块 1 执行");
    }
     {
         System.out.println("子类实例块 2 执行");
     }

    static {
        System.out.println("子类静态块 1 执行");
    }
     static {
         System.out.println("子类静态块 2 执行");
     }

    public static void main(String[] args) {


    }

}
~~~

执行结果：
父类静态块 1 执行
0
父类静态块 2 执行
子类静态块 1 执行
子类静态块 2 执行


2、在实例块中访问构造器中赋值的类属性，只会的到实例属性的默认值；
~~~
class HelloA {
    public HelloA() {
        System.out.println("父类构造器执行");
    }

    {
        System.out.println("父类实例块 1 执行");

    }
    {
        System.out.println("父类实例块 2 执行");
    }

    static {
        System.out.println("父类静态块 1 执行");

    }
    static {
        System.out.println("父类静态块 2 执行");
    }

}

 class HelloB extends HelloA {
    int i ;
    public HelloB() {
        i = 1;
        System.out.println("子类构造器执行");
    }

    {
        System.out.println("子类实例块 1 执行");
        System.out.println(i);
    }
     {
         System.out.println("子类实例块 2 执行");
     }

    static {
        System.out.println("子类静态块 1 执行");
    }
     static {
         System.out.println("子类静态块 2 执行");
     }

    public static void main(String[] args) {
        new HelloB();


    }

}
~~~
执行结果：

父类静态块 1 执行
父类静态块 2 执行
子类静态块 1 执行
子类静态块 2 执行
父类实例块 1 执行
父类实例块 2 执行
父类构造器执行
子类实例块 1 执行
0
子类实例块 2 执行
子类构造器执行

3、在静态块中访问实例属性,idea直接报错了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3422b25d4e1a364d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###静态块执行即类被虚拟机加载
什么时候类会被加载？可以看看我的这篇文章
https://www.jianshu.com/p/558750148f36
