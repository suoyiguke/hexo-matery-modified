---
title: javaweb知识回顾之servlet的线程不安全性（二）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: javaweb知识回顾之servlet的线程不安全性（二）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
> 居安思危

在上篇文章使用idea创建了一个servlet工程实例https://www.jianshu.com/p/bcda275e80a0 这次来点高级内容
######问题1：servlet是单实例还是多实例的？

是不是单例的做一下测试即可，在上篇文章的代码基础上修改serlvet类代码如下
~~~
package com.servlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.concurrent.atomic.AtomicInteger;
public class HelloWorld extends HttpServlet {
    static HelloWorld helloWorld;
    static AtomicInteger ai= new AtomicInteger(0);

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {
        System.out.println("第"+ai.incrementAndGet()+" 次请求打印的hashCode==> "+this.hashCode());

        if(helloWorld == this ){
            System.out.println("两次请求使用同一servlet对象");
        }
        helloWorld = this;

    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) {

        System.out.println("你发起了post请求");
    }

}
~~~
运行工程后连续访问2次 http://localhost:8088/test/helloworld
控制台打印如下，两次请求的hashcode相同，且两次请求的servlet实例 使用 等号比较返回了true。 这足矣证明servlet多次请求均使用同一实例的吧~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0713fd49e868c627.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但是，若给同一个servlet在web.xml中配置了多个，那么就有多个实例。可以做下实验

修改web.xml文件
~~~
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <servlet>
        <servlet-name>HelloWorld</servlet-name>
        <servlet-class>com.servlet.HelloWorld</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>HelloWorld</servlet-name>
            <url-pattern>/helloworld</url-pattern>
    </servlet-mapping>


<!--    添加配置-->
    <servlet>
        <servlet-name>HelloWorld2</servlet-name>
        <servlet-class>com.servlet.HelloWorld</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>HelloWorld2</servlet-name>
        <url-pattern>/helloworld2</url-pattern>
    </servlet-mapping>
</web-app>
~~~

重启工程，分别访问一次 http://localhost:8088/test/helloworld
和http://localhost:8088/test/helloworld2
控制台打印如下，两次访问的hashcode不同且 等号比较返回false
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cf94968eb60fd84e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


所以，做下总结
servlet是单例的，如果在web.xml文件里配置了多个同样的servlet类那么该servlet就是多例的

######问题2：既然servlet是单例的，那么servlet会出现线程安全问题吗？

是的，因为servlet是单例的，那么servlet类的类实例属性也是单实例的。它会被多个请求（对应多个线程）所共享。它会存在和springmvc controller一样的线程安全问题


我们来看下面实验


修改serlvet代码如下，给类实例属性num叠加100000 次
~~~
package com.servlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.concurrent.TimeUnit;

public class HelloWorld extends HttpServlet {
    //由于servlet是单例，则它的实例属性num也只有一个实例。但却要被多个线程并发修改，肯定出现线程安全问题
    Integer num = 0;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {
        for (int i = 0; i <100000 ; i++) {
            num ++;
        }
        System.out.println(num);

    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) {
        System.out.println("你发起了post请求");
    }

}
~~~

然后写个测试客户端，开10个线程，使用httpClient 发起对 http://localhost:8088/test/helloworld 请求
~~~
package io.renren;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import java.io.IOException;

/**
 *@program: ymzhi
 *@description:
 *@author: yinkai
 *@create: 2020-03-15 16:36
 */
public class Testrr {


    public static void main(String[] args) throws IOException {
        HttpGet httpGet = new HttpGet("http://localhost:8088/test/helloworld");
        CloseableHttpClient httpClient = HttpClients.createDefault();

        //开10个线程去请求接口
        for (int i = 0; i <10 ; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        httpClient.execute(httpGet);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }
            }).start();
        }

    }

}
~~~

可以看到控制台的打印
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3b1f3f84cc8b4f46.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
最后结果小于预期值100000 * 10 ，说明出现了线程安全问题


###如何解决servlet中的线程安全问题？
这种因为多线程操作共享变量是典型的`原子性`问题

######servlet自带解决方案
将sevlet类实现SingleThreadModel 接口

~~~
package com.servlet;

import javax.servlet.SingleThreadModel;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class HelloWorld extends HttpServlet implements SingleThreadModel {
    int num = 0;
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {
        for (int i = 0; i <100000 ; i++) {
                num++;

        }
        System.out.println(num);

    }
}
~~~

但这个接口已经过时了。文档中不推荐使用。如下
~~~
/**
 * Ensures that servlets handle only one request at a time. This interface has
 * no methods.
 * <p>
 * If a servlet implements this interface, you are <i>guaranteed</i> that no two
 * threads will execute concurrently in the servlet's <code>service</code>
 * method. The servlet container can make this guarantee by synchronizing access
 * to a single instance of the servlet, or by maintaining a pool of servlet
 * instances and dispatching each new request to a free servlet.
 * <p>
 * Note that SingleThreadModel does not solve all thread safety issues. For
 * example, session attributes and static variables can still be accessed by
 * multiple requests on multiple threads at the same time, even when
 * SingleThreadModel servlets are used. It is recommended that a developer take
 * other means to resolve those issues instead of implementing this interface,
 * such as avoiding the usage of an instance variable or synchronizing the block
 * of the code accessing those resources. This interface is deprecated in
 * Servlet API version 2.4.
 *
 * @deprecated As of Java Servlet API 2.4, with no direct replacement.
 */
~~~
如果servlet实现此接口，则可以保证在servlet的 service方法中不会同时执行两个线程。 servlet容器可以通过同步对servlet单个实例的访问或维护一个servlet实例池并将每个新请求分派给一个自由servlet来保证这一点。 请注意，`SingleThreadModel不能解决所有线程安全问题`。例如，即使使用 SingleThreadModel servlet，`会话属性`和`静态变量`仍然可以同时由多个线程上的多个请求访问。`建议开发人员采用其他方法来解决这些问题`，而不是实现此接口，例如，避免使用实例变量或同步访问这些资源的代码块。 * Servlet API版本2.4中不推荐使用此接口。

######无锁技术
1、使用AtomicInteger 原子类，它内部的cas算法能够解决这种原子类问题
~~~
package com.servlet;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.concurrent.atomic.AtomicInteger;

public class HelloWorld extends HttpServlet {
    AtomicInteger num = new AtomicInteger(0);

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {
        for (int i = 0; i <100000 ; i++) {
            num.incrementAndGet();
        }
        System.out.println(num);

    }
}
~~~

2、使用线程本地变量 ThreadLocal。但是注意最终叠加代码num += integer;不是线程安全的。严格的说仅仅使用ThreadLocal无法保证这种多线程求和的线程安全

~~~
package com.servlet;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class HelloWorld extends HttpServlet {
    ThreadLocal<Integer> tl = new ThreadLocal<>();
    int num = 0;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {

        tl.set(0);
        Integer integer = tl.get();
        for (int i = 0; i <100000 ; i++) {
            integer++;
        }

        //这一步不是线程安全的
        // num += integer;

        System.out.println(num);

    }


}

~~~

######有锁技术
1、使用synchronized同步块，但是这种方式不推荐使用
~~~
package com.servlet;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class HelloWorld extends HttpServlet {
    int num = 0;

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {
        for (int i = 0; i <100000 ; i++) {
            synchronized (this){
               num++;
            }
        }
        System.out.println(num);

    }
}
~~~

2、使用java.util.concurrent.locks.Lock
~~~
package com.servlet;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class HelloWorld extends HttpServlet {
    int num = 0;
    Lock lock = new ReentrantLock();

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)  {
        for (int i = 0; i <100000 ; i++) {

            lock.lock();
            try {
                num++;
            } finally {
                lock.unlock();
            }

        }
        System.out.println(num);

    }
}
~~~
