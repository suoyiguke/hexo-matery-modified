---
title: java-基础知识1-传值和传引用.md
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

######1、基本类型传复印件
~~~
public static void cr(int a){
    a++;
    System.out.println("进入方法打印");
    System.out.println(a);//2
}
public static void main(String[] args) {
    int a = 1;
    cr(a);
    System.out.println("调用方法后打印");
    System.out.println(a);//1
}
~~~
######2、基本类型的包装类型也传的是复印件
~~~
public static void cr(Integer a){
    a++;
    System.out.println("进入方法打印");
    System.out.println(a);//2
}
public static void main(String[] args) {
    Integer a = 1;
    cr(a);
    System.out.println("调用方法后打印");
    System.out.println(a);//1
}
~~~

######3、String 使用+拼接，也是不同的。String是不可变类
~~~
public static void cr(String a){
    a=a+" kai";
    System.out.println("进入方法打印");
    System.out.println(a);//yin kai
}
public static void main(String[] args) {
    String a = "yin";
    cr(a);
    System.out.println("调用方法后打印");
    System.out.println(a);//yin
}
~~~

######4、ArrayList这种复合对象传入的是对象的引用；修改list内部元素对所有引用都生效
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2fb39d3f3630e3f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
public static void cr(List a){
    a.add(4);
    System.out.println("进入方法打印");
    System.out.println(a);//[1, 2, 3, 4]

}
public static void main(String[] args) {
    ArrayList<Integer> a = new ArrayList();
    Collections.addAll(a, 1,2,3);
    cr(a);
    System.out.println("调用方法后打印");
    System.out.println(a);//[1, 2, 3, 4]
}
~~~

######5、ArrayList 在cr方法中用一个新new的对象赋值，则指向不同的堆内存块了；此时两个list修改不会影响对方
![image.png](https://upload-images.jianshu.io/upload_images/13965490-33f9138e35605045.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
public static void cr(List a){

    a = new ArrayList();
    Collections.addAll(a, 4,5,6);
    System.out.println("进入方法打印");
    System.out.println(a);//[4, 5, 6]
}
public static void main(String[] args) {
    ArrayList<Integer> a = new ArrayList();
    Collections.addAll(a, 1,2,3);
    cr(a);
    System.out.println("调用方法后打印");
    System.out.println(a);//[1, 2, 3]
}
~~~

######6、Integer[]、int[]数组传的也是引用
~~~
public static void cr(Integer[] a){
    a[3] = 4;
    System.out.println("进入方法打印");
    System.out.println(Arrays.toString(a));//[1, 2, 3, 4]

}
public static void main(String[] args) {
    Integer[] a = {1,2,3,null};
    cr(a);
    System.out.println("调用方法后打印");
    System.out.println(Arrays.toString(a));//[1, 2, 3, 4]
}

//

public static void cr(int[] a){
    a[3] = 4;
    System.out.println("进入方法打印");
    System.out.println(Arrays.toString(a));//[1, 2, 3, 4]

}
public static void main(String[] args) {
    int[] a = new int[4];
    a[0] = 1;
    a[1] = 2;
    a[2] = 3;
    cr(a);
    System.out.println("调用方法后打印");
    System.out.println(Arrays.toString(a));//[1, 2, 3, 4]
}
~~~

######7、自己写的类构造的对象中的传值和传引用
~~~
public class Test {
   private String name;

    public void setName(String name) {
        this.name = name;
    }

    public void changeName(String name) {
        name = "kaikai";
    }
    public void changeAge(Integer age) {
        age = 22;
    }

    private void changeTest(Test test){
        test.setName("kai");
    }

    public Test(String name) {
        this.name = name;
    }
    public Test() {
    }

    public static void main(String[] args) {
        Test test1 = new Test();
        int age = 20;
        test1.changeAge(age);
        System.out.println("age===>"+age); //20

        Test test2 = new Test("yin");
        test2.changeTest(test2);

        System.out.println("test2.name==>"+test2.name);// kai

        String str = "xuan";
        test2.changeName(str);

        System.out.println("str===>"+str);//xuan

    }
}
~~~

这个例子也可以这样理解：使用方法作用域来理解
1、我们学过JVM中的栈。每个方法都有一个栈帧，栈帧里面有对应的`局部变量表`。所以这里打印的age是main方法中的age,而不是changeAge方法中的age
~~~
Test test1 = new Test();
int age = 20;
test1.changeAge(age);
System.out.println("age===>"+age); //20
~~~

2、这里打印的name是test2对象实例中的name属性
~~~
Test test2 = new Test("yin");
test2.changeTest(test2);
System.out.println("test2.name==>"+test2.name);// kai
~~~

3、这里打印的str 和第一点一样,是main方法中的str 
~~~
String str = "xuan";
test2.changeName(str);
System.out.println("str===>"+str);//xuan
~~~
