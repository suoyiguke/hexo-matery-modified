---
title: java-基础之try-catch-finally.md
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
####关于try-catch -finally异常处理语句块最基本的知识

1、catch 里的代码只有在try里抛出未处理异常时才会执行
~~~
class TestFinally{

    public static void test() {
        try {
            System.out.println("会执行吗？");//执行
        } catch (Exception e) {
            System.out.println(e);//不会执行
        } finally {
            System.out.println("执行finally！");//执行

        }

    }

    public static void main(String[] args) {
        test();
    }
}
~~~
2、try里抛出异常代码行下面的代码不会被执行
~~~
class TestFinally{

    public static void test() {
        try {
            int a = 1 / 0;//抛出异常的代码
            System.out.println("会执行吗？");//不会执行
        } catch (Exception e) {
            System.out.println(e);
        } finally {
            System.out.println("执行finally！");//执行

        }

    }

    public static void main(String[] args) {
        test();

    }
}
~~~

3、try中抛出异常，catch成功捕获执行后。在try-catch-finally后的代码也会得到执行
~~~
class TestFinally {

    public static Integer test() {
        try {

            int i = 1 / 0;
        } catch (Exception e) {
            System.out.println(e);//执行
        } finally {
            System.out.println("执行finally！");//执行
        }

        System.out.println("我会执行吗?");//执行
        return 2;//执行

    }

    public static void main(String[] args) {
        System.out.println(test());//2
    }
}
~~~

4、catch 中使用throw 向调用者抛出异常，则在try-catch-finally后的代码不会执行
~~~
class TestFinally {

    public static Integer test() {
        try {

            int i = 1 / 0;
        } catch (Exception e) {
            throw e;//方法跳出
        }
        System.out.println("我会执行吗?");//不会执行
        return 2;//不会执行

    }

    public static void main(String[] args) {

        try {
            System.out.println(test());
        }catch (Exception e){
            System.out.println(e);//执行
        }
    }
}
~~~

###try-catch-finally 和return语句不得不说的关系


######1、finally中有return语句
`finally中的return语句优先级是最高的！函数最终的返回值以finally中的return语句为准`
①、来看try和finally中return语句的优先级

~~~
class TestFinally{

    public static Integer test() {

        try {
            return 0;//不执行
        } catch (Exception e) {
            System.out.println(e);
            return 2;//因为没有抛出异常，不执行
        } finally {
            System.out.println("执行finally！");
            return 1;//执行
        }

    }

    public static void main(String[] args) {
        Integer test = test();
        System.out.println(test);

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-79aae1697576444e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


②、再来看catch和finally中的return语句优先级

~~~
class TestFinally{

    public static Integer test() {

        try {
            int a = 1/0;
        } catch (Exception e) {
            System.out.println(e);
            return 2;// 被finally中的return覆盖！
        } finally {
            System.out.println("执行finally！");
            return 1;//执行
        }

    }

    public static void main(String[] args) {
        Integer test = test();
        System.out.println(test);

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ac50efd72841e6fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


③、在finally里的return导致finally中后面的语句不被执行
~~~
class TestFinally {

    public static Integer test() {
        try {
            int a = 1/0;
        } catch (Exception e) {
            System.out.println(e);//执行
        } finally {
            if (true) {
                return 1;
            }
            System.out.println("我会执行吗！"); //不会执行

        }
        return 0;//不会执行

    }

    public static void main(String[] args) {
        System.out.println(test());//1

    }
}
~~~





######2、try/catch 中有return语句，finally块中没有return语句

①、`这里情况很特殊`程序执行的顺序被打乱了。代码运行到 return 1;会将return 的结果暂时保留，并没有立刻返回。先去执行finally 区域中的代码，然后返回return 1;
~~~
class TestFinally {

    public static Integer test() {
        try {
            int a = 1 / 0;
        } catch (Exception e) {
            System.out.println(e);
            return 1;//执行了
        } finally {
            System.out.println("执行finally！");//执行了

        }
        System.out.println("会执行吗?");//没有执行
        return 0;//没有执行

    }

    public static void main(String[] args) {
        Integer test = test();
        System.out.println(test);//输出1

    }
}
~~~
执行结果
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f75f91cc278ed363.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

②、所谓的`返回值暂时保留`可以再看一个例子：
~~~
class TestFinally{

    public static Integer test() {
        int i = 0;
        try {
            int a = 1 / 0;
        } catch (Exception e) {
            System.out.println(e);
            return i;// 保留返回值为 0
        } finally {
            i++;
            System.out.println("执行finally！");//执行了

        }
        System.out.println("会执行吗?");//没有执行
        return -1;//没有执行

    }

    public static void main(String[] args) {
        Integer test = test();
        System.out.println(test);//输出0

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cadbfdc7705e2587.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
最终的返回值是 0 。而不是1，有人肯定会说明明执行了i++，之后才返回为什么？ 因为在finally 执行之前的return语句的返回值会被`返回值暂时保留`


③、catch 中的return 优先级大于try-catch-finally后面的
~~~
class TestFinally {

    public static Integer test() {
        try {
            int a = 1/0;

            if (true) {
                return 1;//不会执行
            }
        } catch (Exception e) {
            System.out.println(e);//执行
            return 2;//执行
        } finally {
            System.out.println("finally执行"); //执行

        }
        System.out.println("我会执行吗?");//不会执行
        return 3;//不会执行
    }

    public static void main(String[] args) {
        System.out.println(test());//2

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9dee15767f4c8bbb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

④、try中的return 优先级高于try-catch-finally后面的
~~~
class TestFinally {

    public static Integer test() {
        try {
            if (true) {
                return 1;//执行
            }
        } finally {
            System.out.println("finally执行");//执行
        }

        return  3;//不会执行

    }

    public static void main(String[] args) {
        System.out.println(test());//1

    }
}
~~~






######try/catch/finally和return 关系总结
- finally中的return 优先级最高。如果finally中有return 1，那么方法的返回值就是1了
- try和catch中return 的优先级无法比较
- try中的return 优先级高于try-catch-finally后面的
- catch 中的return 优先级大于try-catch-finally后面的
- 注意`返回值保留`问题


###### try/catch/finally和 throw抛出异常的关系
~~~
class TestFinally {

    public static void test() {
       try {

           int i = 1 / 0; //执行
       }catch (Exception e){
           System.out.println(e);//执行
           throw e;//执行
       }finally {
           System.out.println("finally被执行"); //执行
       }

        System.out.println("我会执行吗？");//不执行



    }

    public static void main(String[] args) {
        test();

    }
}
~~~

###大总结
1、finally 不受 try、catch、throw 、return的影响，一定会执行
2、finally前有return，会先执行return语句，并将结果保存下来，再执行finally块，最后return
3、finally前有return，finally中也有return，先执行前面的return，保存下来，再执行finally的return，覆盖之前的return结果，并返回

###使用try/catch/finally/throw 处理对线程执行流程的影响
1、如果某`运行时异常`没有被捕获，那么直接中断线程执行
~~~
   public static void main(String[] args) {

        String str = (String) new Object();
        System.out.println("不会被执行");

    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e131bec77d0bad69.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、某异常被try-catch-finally捕获，线程会继续执行finally之后的代码
~~~
    public static void main(String[] args) {

        try {
            String str = (String) new Object();
        }catch ( Exception e ){
          e.printStackTrace();
        }finally {

        }
        System.out.println("继续执行！");

    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0ef546950bea3028.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、如果使用throw抛出异常，则finally之后的代码不会执行
