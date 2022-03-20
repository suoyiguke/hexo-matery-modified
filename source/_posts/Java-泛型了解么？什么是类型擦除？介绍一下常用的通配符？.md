---
title: Java-泛型了解么？什么是类型擦除？介绍一下常用的通配符？.md
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
Java 泛型（generics）是 JDK 5 中引入的一个新特性, 泛型提供了编译时类型安全检测机制，该机制允许程序员在编译时检测到非法的类型。泛型的本质是参数化类型，也就是说所操作的数据类型被指定为一个参数。


Java 的泛型是伪泛型，这是因为 Java 在编译期间，所有的泛型信息都会被擦掉，这也就是通常所说类型擦除 。
~~~
    public static void main(String[] args)
        throws  NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        List<Integer> list = new ArrayList<>();
        list.add(12);
        //这里直接添加会报错
        //list.add("a");
        Class<? extends List> clazz = list.getClass();
        Method add = clazz.getDeclaredMethod("add", Object.class);
        //但是通过反射添加，是可以的
        add.invoke(list, "kl");
        System.out.println(list);
    }
~~~


泛型一般有三种使用方式:泛型类、泛型接口、泛型方法。

1.泛型类：

~~~
//此处T可以随便写为任意标识，常见的如T、E、K、V等形式的参数常用于表示泛型
//在实例化泛型类时，必须指定T的具体类型
public class Generic<T> {

    private T key;

    public Generic(T key) {
        this.key = key;
    }

    public T getKey() {
        return key;
    }

    public static void main(String[] args) {
        Generic<Integer> genericInteger = new Generic<Integer>(123456);
        //自动获取Integer的eky
        Integer key1 = genericInteger.getKey();

        Generic<String> genericString = new Generic<String>("HELLO");
        //自动获取Integer的eky
        String key2 = genericString.getKey();

    }
}

~~~

2.泛型接口 ：
~~~
//此处T可以随便写为任意标识，常见的如T、E、K、V等形式的参数常用于表示泛型
//在实例化泛型类时，必须指定T的具体类型
public interface Generator<T> {
    public T method();
}

/**
 * 实现泛型接口，不指定类型
 */
class GeneratorImplA<T> implements Generator<T>{
    @Override
    public T method() {
        return null;
    }
}

/**
 * 实现泛型接口，指定类型
 */
class GeneratorImplB<T> implements Generator<String>{
    @Override
    public String method() {
        return "hello";
    }
}

class Main{

    public static void main(String[] args) {
        GeneratorImplA<Integer>  generatorImplA = new GeneratorImplA<>();
        //传入Integer泛型，获取了Integer类型值
        Integer method = generatorImplA.method();

        //实现类本身是指定了String的泛型，返回就是String
        Generator<String> stringGenerator = new GeneratorImplB<>();
        String method2 = stringGenerator.method();

    }
}
~~~

3、泛型方法
~~~
class Main {
    public static <E> void printArray(E[] inputArray) {
        for (E element : inputArray) {
            System.out.printf("%s ", element);
        }
        System.out.println();
    }

    public static void main(String[] args) {
        // 创建不同类型数组： Integer, Double 和 Character
        Integer[] intArray = { 1, 2, 3 };
        String[] stringArray = { "Hello", "World" };
        printArray( intArray  );
        printArray( stringArray  );
    }
}
~~~



**常用的通配符为： T，E，K，V，？


？ 表示不确定的 java 类型
T (type) 表示具体的一个 java 类型
K V (key value) 分别代表 java 键值中的 Key Value
E (element) 代表 Element

**? T 区别：**
T 是一个 确定的 类型，通常用于泛型类和泛型方法的定义，？是一个 不确定的类型，通常用于泛型方法的调用代码和形参，不能用于定义类和泛型方法。





