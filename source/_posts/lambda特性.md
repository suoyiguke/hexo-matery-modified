---
title: lambda特性.md
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
1、捕获调用方法的变量
这里有一条规则：lambda 表达式中捕获的变量必须实际上是最终变量 ( effectivelyfinal。)
实际上的最终变量是指， 这个变量初始化之后就不会再为它赋新值。在这里，text 总是指示
同一个 String 对象，所以捕获这个变量是合法的。不过，i 的值会改变，因此不能捕获。

2、this
~~~
public class ApplicationO
{
public void init() {
ActionListener listener * event -> {
System.out.println(this.toStringO); 
}
~~~
表达式 this.toStringO 会调用 Application 对象的 toString方法， 而不是 ActionListener 实
例的方法。在 lambda 表达式中， this 的使用并没有任何特殊之处。lambda 表达式的作用域嵌
套在 init 方法中，与出现在这个方法中的其他位置一样， lambda 表达式中 this 的含义并没有
变化。

3、变量作用域

lambda 表达式的体与嵌套块有相同的作用域；这里同样适用命名冲突和遮蔽的有关规则。在 lambda 表达式中声明与一个局部变量同名的参数或局部变量是不合法的
