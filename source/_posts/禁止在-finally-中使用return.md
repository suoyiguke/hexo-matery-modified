---
title: 禁止在-finally-中使用return.md
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
###禁止在 finally 中使用return
当 try 语句和 finally 语句中都有 return 语句时，在方法返回之前，finally 语句的内容将被执行，并且 finally 语句的返回值将会覆盖原始的返回值。如下：
~~~
public class Test {
    public static int f(int value) {
        try {
            return value * value;
        } finally {
            if (value == 2) {
                return 0;
            }
        }
    }
}
~~~
如果调用 f(2)，返回值将是 0，因为 finally 语句的返回值覆盖了 try 语句块的返回值。



###try-catch-finally详解
try块： 用于捕获异常。其后可接零个或多个 catch 块，如果没有 catch 块，则必须跟一个 finally 块。
catch块： 用于处理 try 捕获到的异常。
finally 块： 无论是否捕获或处理异常，finally 块里的语句都会被执行。当在 try 块或 catch 块中遇到 return 语句时，finally 语句块将在方法返回之前被执行。


###在以下 3 种特殊情况下，finally 块不会被执行：

首先，try没有执行，那么finally也不会执行

- 在 try 或 finally块中用了 System.exit(int)退出程序。但是，如果 System.exit(int) 在异常语句之后，finally 还是会被执行。
- 程序所在的线程死亡。
- 关闭 CPU。
下面这部分内容来自 issue:https://github.com/Snailclimb/JavaGuide/issues/190。

####Throwable 类常用方法
public string getMessage():返回异常发生时的简要描述
public string toString():返回异常发生时的`详细信息`
public string getLocalizedMessage():返回异常对象的本地化信息。使用 Throwable 的子类覆盖这个方法，可以生成本地化信息。如果子类没有覆盖该方法，则该方法返回的信息与 getMessage（）返回的结果相同
public void printStackTrace():在控制台上打印 Throwable 对象封装的异常信息

>请使用e.toString() 打印详细信息而不是 e.getMessage()。
