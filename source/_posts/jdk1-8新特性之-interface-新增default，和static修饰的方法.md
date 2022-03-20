---
title: jdk1-8新特性之-interface-新增default，和static修饰的方法.md
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
新 interface 的方法可以用default 或 static修饰，这样就可以有方法体，实现类也不必重写此方法。一个 interface 中可以有多个方法被它们修饰，这 2 个修饰符的区别主要也是普通方法和静态方法的区别。
- default修饰的方法，是普通实例方法，可以用this调用，可以被子类继承、重写。相当于是一个接口的默认实现，实现类即使不去实现default修饰的方法也不会报错。（这个特性可以让我们不用去写空实现）
- static修饰的方法，使用上和一般类静态方法一样。但它不能被子类继承，只能用Interface调用。



我们来看一个实际的例子。
~~~
public interface InterfaceNew {

    static void sm() {
        System.out.println("static sm");
    }

    static void sm2() {
        System.out.println("static sm2");
    }

    default void def() {
        System.out.println("default def");
    }

    default void def2() {
        System.out.println("default def2");
    }

    void f();
}

class A implements InterfaceNew {

    /**
     * def和def2不是必须要实现的
     */
//    @Override
//    public void def() {
//
//    }
//    @Override
//    public void def2() {
//
//    }

    /**
     * f必须要实现
     */
    @Override
    public void f() {
        System.out.println("A.f()");
    }

    public static void main(String[] args) {
        InterfaceNew a = new A();
        //调用 普通
        a.f();

        //调用 default
        a.def();
        a.def2();

        //调用static
        InterfaceNew.sm();
        InterfaceNew.sm2();
    }
}
~~~


~~~
public interface InterfaceNew {
    static void sm() {
        System.out.println("interface提供的方式实现");
    }
    static void sm2() {
        System.out.println("interface提供的方式实现");
    }

    default void def() {
        System.out.println("interface default方法");
    }
    default void def2() {
        System.out.println("interface default2方法");
    }
    //须要实现类重写
    void f();
}

public interface InterfaceNew1 {
    default void def() {
        System.out.println("InterfaceNew1 default方法");
    }
}

~~~
如果有一个类既实现了 InterfaceNew 接口又实现了 InterfaceNew1接口，它们都有def()，并且 InterfaceNew 接口和 InterfaceNew1接口没有继承关系的话，这时就必须重写def()。不然的话，编译的时候就会报错：`java: 类 A从类型 InterfaceNew 和 InterfaceNew1 中继承了def2() 的不相关默认值`。
~~~

class A implements InterfaceNew,InterfaceNew1 {

    /**
     * def和def2不是必须要实现的
     */
//    @Override
//    public void def() {
//
//    }
//    @Override
//    public void def2() {
//
//    }

    /**
     * f必须要实现
     */
    @Override
    public void f() {
        System.out.println("A.f()");
    }

    public static void main(String[] args) {
        InterfaceNew a = new A();
        //调用 普通
        a.f();

        //调用 default
        a.def();
        a.def2();

        //调用static
        InterfaceNew.sm();
        InterfaceNew.sm2();
    }
}
~~~
**在 Java 8 ，接口和抽象类有什么区别的？**
很多小伙伴认为：“既然 interface 也可以有自己的方法实现，似乎和 abstract class 没多大区别了。”
其实它们还是有区别的

interface 和 class 的区别，好像是废话，主要有：
- 接口多实现，类单继承
- 接口的方法是 public abstract 修饰，变量是 public static final 修饰。 abstract class 可以用其他修饰符
interface 的方法是更像是一个扩展插件。而 abstract class 的方法是要继承的。

开始我们也提到，interface 新增default，和static修饰的方法，为了解决接口的修改与现有的实现不兼容的问题，并不是为了要替代abstract class。在使用上，该用 abstract class 的地方还是要用 abstract class，不要因为 interface 的新特性而降之替换。

记住接口永远和类不一样。
