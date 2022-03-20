---
title: 使用-try-with-resources-代替try-catch-finally调用close关闭资源.md
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
类似于InputStream、OutputStream 、Scanner 、PrintWriter等的资源都需要我们调用close()方法来手动关闭，一般情况下我们都是通过try-catch-finally语句：
~~~
        //读取文本文件的内容
        Scanner scanner = null;
        try {
            scanner = new Scanner(new File("D://read.txt"));
            while (scanner.hasNext()) {
                System.out.println(scanner.nextLine());
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } finally {
            if (scanner != null) {
                scanner.close();
            }
        }
~~~
这样做是不是很麻烦？既要进行资源非空判断还要对close进行捕获异常，弄不好就可能有资源忘了关闭。
在 JDK 1.7 之后的 try-with-resources 可以完美解决这个问题。
改造上面的代码:
~~~
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(new File("test.txt"))) {
            while (scanner.hasNext()) {
                System.out.println(scanner.nextLine());
            }
        } catch (FileNotFoundException fnfe) {
            fnfe.printStackTrace();
        }finally {
            System.out.println("执行finally");
        }
    }
~~~
其实try-with-resources写法会自动加上close的代码，反编译一下：
~~~
    public static void main(String[] args) {
        try {
            Scanner scanner = new Scanner(new File("test.txt"));
            Throwable var2 = null;

            try {
                while(scanner.hasNext()) {
                    System.out.println(scanner.nextLine());
                }
            } catch (Throwable var20) {
                var2 = var20;
                throw var20;
            } finally {
                if (scanner != null) {
                    if (var2 != null) {
                        try {
                            scanner.close();
                        } catch (Throwable var19) {
                            var2.addSuppressed(var19);
                        }
                    } else {
                        scanner.close();
                    }
                }

            }
        } catch (FileNotFoundException var22) {
            var22.printStackTrace();
        } finally {
            System.out.println("执行finally");
        }

    }

~~~
- 自动生成了关闭资源的finally 代码块；
- 而且将scanner.close()抛出的异常和new Scanner()抛出异常，addSuppressed合并到了一起。解决了`异常屏蔽`；从JDK 1.7开始，Throwable 类新增了 addSuppressed 方法，支持将一个异常附加到另一个异常身上，从而避免异常屏蔽。
- 在try-with-resources后面定义的finally 代码块自动加到了最外层。



如果有多个资源呢，如何处理？
通过使用分号分隔，可以在try-with-resources块中声明多个资源。
~~~
       try (BufferedInputStream bin = new BufferedInputStream(
            new FileInputStream(new File("test.txt")));
            BufferedOutputStream bout = new BufferedOutputStream(
                new FileOutputStream(new File("out.txt")))) {
            int b;
            while ((b = bin.read()) != -1) {
                bout.write(b);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
~~~



###自定义AutoClosable 实现
这个try-with-resources结构里不仅能够操作java内置的类。你也可以在自己的类中实现java.lang.AutoCloseable接口，然后在try-with-resources结构里使用这个类。

AutoClosable 接口仅仅有一个方法，接口定义如下：
~~~
public interface AutoClosable {
    public void close() throws Exception;
}
~~~

未实现AutoCloseable接口的类无法使用在try-with-resources结构的try中，编译会报错：
~~~
java: 不兼容的类型: try-with-resources 不适用于变量类型
    (java.io.File无法转换为java.lang.AutoCloseable)
~~~

任何实现了这个接口的方法都可以在try-with-resources结构中使用。

下面是一个简单的例子：
~~~
public class MyAutoClosable implements AutoCloseable {
    public void doSome() {
        System.out.println("doSome");
    }
    @Override
    public void close() throws Exception {
        System.out.println("closed");
    }
}

~~~

~~~
    public static void main(String[] args) {
        try (MyAutoClosable myAutoClosable = new MyAutoClosable()) {
            myAutoClosable.doSome();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            System.out.println("finally执行");
        }
    }
~~~
doSome
closed
finally执行

使用try-with-resources以后就不要担心使用资源不关闭了。

>面对必须要关闭的资源，我们总是应该优先使用 try-with-resources 而不是try-finally。随之产生的代码更简短，更清晰，产生的异常对我们也更有用。try-with-resources语句让我们更容易编写必须要关闭的资源的代码，若采用try-finally则几乎做不到这点。
