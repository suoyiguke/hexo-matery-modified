---
title: JAVA-垃圾回收之-强引用（二）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
---
title: JAVA-垃圾回收之-强引用（二）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
>锲而舍之，朽木不折

强引用是最传统的`引用`的定义， 是指在程序代码之中普遍存在的引用赋值，我们写的代码，99.9999%都是强引用。 即类似`Object obj=new Object()` 这种引用关系。 

>无论任何情况下， 只要强引用关系还存在， 垃圾收集器就永远不会回收掉被引用的对象。JVM宁愿抛出OOM，也不会去回收。

那么什么时候才可以被回收呢？当强引用和对象之间的关联被中断了，就可以被回收了。如下把 obj 赋值为null，那么在下次GC就会将obj对象回收了

> obj =  null;

我们可以亲自动手实验一下，重写Object类的finalize方法。可以直观的感知到test 对象被回收了
~~~
package io.renren;
/**
 *@author: yinkai
 *@create: 2020-03-20 10:53
 */
public class GC {
    public static void main(String[] args) {
        Test test = new Test();
        test = null;
        System.gc();
    }
}
class Test {
    /**
     *重写Object类的finalize方法
     */
    @Override
    protected void finalize() {
        System.out.println("Test 被回收了");
    }
}
~~~
执行如下，
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6bc62f42663cb05f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如果将 `test = null;` 注释掉，那么并不会回收test对象

######强引用对象在什么时候会被回收？

这里有一个疑惑：是不是强引用对象只有将之赋值的变量赋为null后才可能被GC回收？
如下，将obj变量赋值为null
>Object obj = new Object();
obj = null;

如果不赋值为null那就不会被GC回收？按照我们的开发常识来看绝对是会回收的，咱们工程中那么多直接使用new的代码后面都没有赋值为null，那不也好好的没报OOM嘛。如果知道`可达性分析算法`的原理就很好理解了。

从GC roots根对象开始找引用，只要找不到obj，就代表这个obj可以被回收了。Object obj = new Object();这种写法，通常obj在方法栈帧的局部变量表local variables里面，随着方法的开始而创建，退出而销毁，那么obj就无法从GC roots根对象上面找到了（假设没有设置为field或被其它引用）。那么此obj就是不可达的，然后就会被GC回收了。

