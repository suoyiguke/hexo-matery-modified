---
title: java-匿名内部类相关概念.md
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
###匿名内部类

~~~
public class MyThread {
    private MyRunnable target;
    public MyThread(MyRunnable target) {
        this.target = target;
    }

    public void run() {
        System.out.println("去12306买了一张票");
        System.out.println("坐火车...");
    }
    public void start() {
        if (target != null) {
            target.run();
        } else {
             this.run();
        }
    }
}
~~~

~~~
@FunctionalInterface
public interface MyRunnable {
    void run();
}
~~~


~~~
    public static void main(String[] args) {
        Integer i =1;
        new MyThread(new MyRunnable() {
            @Override
            public void run() {
                System.out.println("不用买票");
                System.out.println("骑电瓶车...");
                System.out.println(i);
            }
        }).start();
    }
~~~


####匿名内部类访问外部方法中定义的变量
jdk1.8后匿名部内部类访问外面方法中定义胡变量不需要加final了。记住，在1.7时还需加final否则编译不通过！
查看反编译代码，可见编译后的代码自动了帮我们加了final。
~~~
public class t1 {
    public t1() {
    }

    public static void main(String[] args) {
        final Integer i = 1;
        (new MyThread(new MyRunnable() {
            public void run() {
                System.out.println("不用买票");
                System.out.println("骑电瓶车...");
                System.out.println(i);
            }
        })).start();
    }
}
~~~

**为什么传递给匿名内部类的参数必须声明为final？**
局部变量在方法中，方法调用完毕即弹栈，会从内存消失。而匿名内部类的实例是在堆中，在未来某个时刻被垃圾回收。生命周期不同步会导致：一个实例持有一个已经不存在的变量引用...
由于对象的生命周期无法改变，所以只能是局部变量做出让步：加final变为常量，常驻内存。这样，变量的生命周期反而可能比实例更长久。

*我这个里还有个疑问：*
但是，这种情况。for循环中的循环计数器i如果要使用到匿名内部类里面去。编译会报错：
需要用int finalI = i; 接收下。
~~~
    public static void main(String[] args) {
        for (int i = 0; i <10 ; i++) {
            int finalI = i;
            new MyThread(new MyRunnable() {
                @Override
                public void run() {
                    System.out.println("不用买票");
                    System.out.println("骑电瓶车...");
                    System.out.println(finalI);
                }
            }).start();
        }
    }
~~~
why？
因为不能把final声明在i上，i毕竟还要自增。故只能再用一个final 变量接收i的值。而jdk1.8中final会自动加上，所以就是 int finalI = i; 

###Lambda
**只有一个抽象方法的匿名内部类(函数式接口)可以写作lambada**
上面的可以简写为如下：
~~~
    public static void main(String[] args) {
        for (int i = 0; i <10 ; i++) {
            final String finalI = String.valueOf(i);
            new MyThread(() -> {
                System.out.println("不用买票");
                System.out.println("骑电瓶车...");
                System.out.println(finalI);
            }).start();
        }
    }
~~~

1、说明Lambda表达式在身份上与匿名类对象等价。
2、说明Lambda表达式在作用上与方法等价。
>Lambda表达式，其实是一段可传递的代码。Lambda本质是以类的身份，干方法的活。
  
###函数式接口
介绍完Lambda表达式，最后提一下函数式接口。大家肯定会有疑问：难道所有接口都可以接收Lambda表达式吗？显然不是的，接口要想接收Lambda表达式，必须是一个函数式接口。所谓函数式接口，最核心的特征是：
>有且只有一个抽象方法。

这句话有两个重点：抽象方法、唯一。你可能觉得：啥玩意，Java的接口不就抽象方法吗？难道还有别的方法？是的，Java8的接口可以添加静态方法和默认方法，越来越像一个类。关于Java8为什么需要静态方法和默认方法，后面介绍Stream流操作时我们再来介绍。


也就是说，如果你希望一个接口能接收Lambda表达式充当匿名类对象，那么接口必须仅有一个抽象方法，这是函数式接口的定义。通常我们可以在接口上加一个@FunctionalInterface检测，作用于@Override一样。但函数式接口和@FunctionalInterface注解没有必然联系。

若接口包含多个抽象方法，则不是一个`函数式接口`，不能改写为`Lambda`。
下面的代码不会被idea置灰提示可以改写为Lambda。
~~~
public interface MyRunnable {
    void run();
    void rr();
}
~~~
~~~
    public static void main(String[] args) {
        for (int i = 0; i <10 ; i++) {
            final String finalI = String.valueOf(i);
            new MyThread(new MyRunnable() {
                @Override
                public void run() {
                    System.out.println("不用买票");
                    System.out.println("骑电瓶车...");
                    System.out.println(finalI);
                }

                @Override
                public void rr() {

                }
            }).start();
        }
    }
~~~

###Lambda与匿名内部类的区别
> 很多人可能在心里已经自动把Lambda等同于匿名内部类，认为Lambda是匿名内部类的语法糖。然而并不是。

1、只有仅仅包含一个抽象方法实现的匿名内部类才可以改写为Lambda。
2、使用匿名内部类编译后产生两个class`（t1.class、t1$1.class）`；Lambda编译产生一个`class(t1.class)`。
3、在抽象方法体打印this二者不同；匿名内部类的this指向匿名内部类对象`(t1$1@16f6e28)`；Lambda方法体this指向调用者`(t1@14c265e)`。


### this与闭包
