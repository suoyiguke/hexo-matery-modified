---
title: jvm-类初始化场景.md
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
title: jvm-类初始化场景.md
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

###类初始化场景

- 执行main方法，main方法所在的类会先被初始化
- 执行new（创建对象）、getstatic(访问静态属性)、putstatic(设置静态属性)和invokestatic(调用静态方法)指令；
- 使用reflect对类进行反射调用；
- 初始化一个类的时候，父类还没有初始化，会事先初始化父类；



###不会触发类初始化的情况
- 通过子类引用父类的静态字段，只会触发父类的初始化，而不会触发子类的初始化。
- 定义对象数组，不会触发该类的初始化。
- 常量(static final声明的属性)在编译期间会存入调用类的常量池中，本质上并没有直接引用定义常量的类，不会触发定义常量所在的类。
- 通过类名获取Class对象（Class c_dog = Dog.class），不会触发类的初始化。
- 通过Class.forName加载指定类时，如果指定参数initialize为false时，也不会触发类初始化，其实这个参数是告诉虚拟机，是否要对类进行初始化。
- 通过ClassLoader默认的loadClass方法，也不会触发初始化动作；
####初始化场景例子
案例1、main方法所在的类首先被初始化；getstatic(访问静态属性)，静态属性所在的类也被初始化

~~~
class E{
    static int a = 1;
    static {
        System.out.println("E类静态块执行");
    }

}

class F{
    static {
        System.out.println("F类静态块执行");
    }
    public static void main(String[] args) {
        System.out.println("F类的main方法执行");
        System.out.println(E.a);
    }
}
~~~
执行结果：
F类静态块执行
F类的main方法执行
E类静态块执行
1

案例2、putstatic(设置静态属性)，属性所在的类被初始化

~~~
class G{
    static {
        System.out.println("G类静态块执行");
    }
    public static void main(String[] args) {
        System.out.println("G类的main方法执行");
        E.a = 2; 
    }
}

~~~
执行结果：
G类静态块执行
G类的main方法执行
E类静态块执行

案例3、invokestatic(调用静态方法)，静态方法所在类被初始化
~~~
class E{
    static int a = 1;
    static {
        System.out.println("E类静态块执行");
    }

    static int getA(){
        return a;
    }

}
class H{
    static {
        System.out.println("H类静态块执行");
    }
    public static void main(String[] args) {
        System.out.println("H类的main方法执行");
        E.getA();
    }
}
~~~
执行结果：
H类静态块执行
H类的main方法执行
E类静态块执行

案例4、使用反射构造对象，也会初始化类
~~~
class I{
    static {
        System.out.println("I类静态块执行");
    }
}

class J{
    static {
        System.out.println("J类静态块执行");
    }
    public static void main(String[] args) throws ClassNotFoundException, IllegalAccessException, InstantiationException {
        System.out.println("J类的main方法执行");

        Class iClass = Class.forName("test.I");
        I i = (I) iClass.newInstance();

    }
}
~~~
执行结果：
~~~
class I{
    static {
        System.out.println("I类静态块执行");
    }
}



class J{
    static {
        System.out.println("J类静态块执行");
    }
    public static void main(String[] args) throws ClassNotFoundException, IllegalAccessException, InstantiationException {
        System.out.println("J类的main方法执行");

        Class iClass = Class.forName("test.I");
        I i = (I) iClass.newInstance();

    }
}

~~~

###不会初始化类的例子
案例1：通过子类引用父类的静态字段，只会触发父类的初始化，而不会触发子类的初始化。
~~~

class Parent {
    static int a = 100;
    static {
        System.out.println("父类初始化");
    }
}

class Child extends Parent {
    static {
        System.out.println("子类初始化");
    }
}
 class Init{
    public static void main(String[] args){
        System.out.println(Child.a);  //不会初始化子类
    }
}
~~~
案例2：定义对象数组，不会触发该类的初始化。

~~~
class Init{
    public static void main(String[] args){
        Parent[] parents = new Parent[10]; //不会初始化Parent类
    }
~~~

案例3：常量在编译期间会存入调用类的常量池中，本质上并没有直接引用定义常量的类，不会触发定义常量所在的类。

~~~

class Const {
    //可以试一下将final干掉，结果Const被初始化！
    static final int A = 100; //编译阶段，常量A存储到Init类的常量池中
    static {
        System.out.println("Const 初始化");
    }
}

class Init{
    public static void main(String[] args){
        System.out.println(Const.A);
    }
}
~~~

案例4：通过类名获取Class对象，不会触发类的初始化。
~~~

class test {
    public static void main(String[] args) throws ClassNotFoundException {
        Class c_dog = Dog.class; //不会初始化Dog类
        Class clazz = Class.forName("test.Cat"); //会初始化Cat类
    }
}

class Cat {
    static {
        System.out.println("Cat is load");
    }
}

class Dog {
    static {
        System.out.println("Dog is load");
    }
}
~~~

案例5： Class.forName 如果指定参数initialize为false时，也不会触发类初始化
~~~
class test {
    public static void main(String[] args) throws ClassNotFoundException {
        Class clazz = Class.forName("test.Cat",false,test.class.getClassLoader()); //不会初始化Cat类
    }
}
~~~

案例6：通过ClassLoader默认的loadClass方法，也不会触发初始化动作；
~~~
   public static void main(String[] args) throws ClassNotFoundException {
        ClassLoader classLoader = test.class.getClassLoader();
        Class<?> c = classLoader.loadClass("test.Cat");
    }
~~~
