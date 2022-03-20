---
title: java-基础之switch语句细节.md
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

###switch所允许的数据类型
![image.png](https://upload-images.jianshu.io/upload_images/13965490-73a8c2501dba91d6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

基本数据类型：byte, short, char, int
包装数据类型：Byte, Short, Character, Integer
枚举类型：Enum
字符串类型：String（jdk 7 开始支持）

不支持boolean和double、float类型
###switch语句的执行特征
1、switch 分支是由上到下执行的
2、程序会继续执行下一条 case 语句，直到出现 break 语句，当遇到 break 语句时，switch 语句终止
3、switch 语句可以包含一个 default 分支，该分支一般是 switch 语句的最后一个分 支（可以在任何位置，但一般在最后一个）。
4、default 在没有 case 语句的值和变量值相等的时候执行。
5、default放到最后的话就不需要 break 语句，如果放到前面情况就不同了。

######实例
1、没有break 语句，程序将由上至下执行 case。直到遇到break 
~~~
    public static void main(String[] args) {
        switch (0) {
            case 0:
                System.out.println("zero");
            case 1:
                System.out.println("one");
            case 2:
                System.out.println("two");
            default:
                System.out.println("default");

        }
    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7ba0d9ac4735e357.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、再来看有break会怎么样
~~~
public static void main(String[] args) {
        switch (0) {
            case 0:
                System.out.println("zero");
            case 1:
                System.out.println("one");
            case 2:
                System.out.println("two");
                break;
            default:
                System.out.println("default");

        }
    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cba3e313503979b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、default在没有匹配时执行
~~~
    public static void main(String[] args) {
        switch (8) {
            case 0:
                System.out.println("zero");
            case 1:
                System.out.println("one");
            case 2:
                System.out.println("two");
            default:
                System.out.println("default");

        }
    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-554953b5d84faa0d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、如果default语句块写在上面，因为没有遇到break，全都执行一遍~
~~~
  public static void main(String[] args) {
        switch (8) {
            default:
                System.out.println("default");
            case 0:
                System.out.println("zero");
            case 1:
                System.out.println("one");
            case 2:
                System.out.println("two");


        }
    }
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-884fb296a3207e4b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

