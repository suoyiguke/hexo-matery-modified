---
title: jvm-Jconsole.md
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
title: jvm-Jconsole.md
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
G:\Jdk\jdk1.8\bin\jconsole.exe

###可以选择监控的内存分代和内存区域
![image.png](https://upload-images.jianshu.io/upload_images/13965490-91de7dfc1debe4b2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###垃圾回收对类的成员属性的影响
1、先设置堆内存大小为10m，如果内存大了。可能就不会触发GC了
~~~
-Xms10m -Xmx10m 
~~~

2、运行下面的程序
~~~
package test;


import org.junit.Test;
import java.util.ArrayList;
import java.util.List;

public class TestGc {

    public byte[] arr = new byte[128*1024];//128k

    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(30000);

        send(1000);//1024个对象 占用大小>128m

    }

    public static  void send(int n) throws InterruptedException {
        for (int i = 0; i <n ; i++) {
            Thread.sleep(10);
            TestGc testGc = new TestGc();
        }
    }
}

~~~

3、监控

**堆内存变化情况**
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ee2ff71a6105c7cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**伊甸区变化情况**
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9edc7132a26f5421.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**幸存者区变化情况**
![image.png](https://upload-images.jianshu.io/upload_images/13965490-039a6358e55b4ed9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**养老代变化情况**
![image.png](https://upload-images.jianshu.io/upload_images/13965490-00c850ff7e0c2ae0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





