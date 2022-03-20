---
title: java-http请求工具问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: java-http请求工具问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
必须使用http连接池，而不能直接使用new connection的形式，否则当连接过，端口释放更不上就会导致
Caused by: java.net.SocketException: No buffer space available (maximum connections reached?): connect

以 javax.net.ssl.HttpsURLConnection为例，下面就是一段典型的问题代码。
~~~
HttpURLConnection  conn = (HttpURLConnection) realUrl.openConnection();
conn.close();
~~~

推荐使用成熟的二方库，如
apache httpclient

*   在你刚刚选择从HttpURLConnection转成Apache Httpclient时，发现好像新出了个okHttp了。
*   你还在犹豫要不要换成okHttp时，Android已经废除了Apache Httpclient改用okHttp了。
*   那这时你开始纠结继续用Apache Httpclient还是改用okHttp时，okHttp的公司Square又出了Retrofit，网友已经在说既然你都用了okHttp为何不直接使用Retrofit

![image](https://upload-images.jianshu.io/upload_images/13965490-6669050d9fee2041.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**1、HttpURLConnection：**

HttpURLConnection是java的标准类，什么都没封装，用起来太原始，不方便，比如重访问的自定义，以及一些高级功能等。

### 2、java.net.http.HttpClient

jdk11正式启用自带HttpClient，代替之前比较旧的HttpURLConnection。其实从java9的jdk.incubator.httpclient模块迁移到java.net.http模块，包名由jdk.incubator.http改为java.net.http。

### **3、Apache HttpClient：**

在Android中，AndroidSDK中集成了Apache的HttpClient模块，HttpClient就是一个增强版的HttpURLConnection，它只是关注于如何发送请求、接收响应，以及管理HTTP连接。如果做好封装或者使用android-async-http，Afinal，Xutils也能挺简单的完成http请求，但是Android6.0谷歌因为和Apache更新难以同步等原因吧已经放弃了HttpClient，改于了okHttp。

### **4、okHttp：**

OkHttp 是 Square 公司开源的针对 Java 和 Android 程序，封装的一个高性能 http 请求库。OKHttp 类似于 HttpUrlConnection， 是基于传输层实现应用层协议的网络框架。 而不止是一个 Http 请求应用的库。

**okHttp的优势：**

*   链接复用
*   Response 缓存和 Cookie
*   默认 GZIP
*   请求失败自动重连
*   DNS 扩展
*   Http2/SPDY/WebSocket 协议支持
*   默认情况下，OKHttp会自动处理常见的网络问题：像二次连接、SSL的握手问题。
*   从Android4.4开始HttpURLConnection的底层实现采用的是okHttp.

### 5、Retrofit：

Retrofit 是 Square 公司出品的默认基于 OkHttp 封装的一套 RESTful 网络请求框架，，RESTful 可以说是目前流行的一套 api 设计的风格，并不是标准。Retrofit 的封装可以说是很强大，里面涉及到一堆的设计模式，你可以通过注解直接配置请求，你可以使用不同的 http 客户端，虽然默认是用 OKhttp ，可以使用不同 Json Converter 来序列化数据，同时提供对 RxJava 的支持，使用 Retrofit + OkHttp + RxJava + Dagger2 可以说是目前比较潮的一套框架，但是需要有比较高的门槛。

```
Retrofit retrofit =
        new Retrofit.Builder()
            .baseUrl(API_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();
```

### 6、RestTemplate

RestTemplate是 Spring 提供的用于访问Rest服务的客户端， RestTemplate 提供了多种便捷访问远程Http服务的方法,能够大大提高客户端的编写效率。

### 7、OpenFeign

*   可插拔的注解支持，包括Feign注解和JAX-RS注解。
*   支持可插拔的HTTP编码器和解码器（Gson，Jackson，Sax，JAXB，JAX-RS，SOAP）。
*   支持Hystrix和它的Fallback。
*   支持Ribbon的负载均衡。
*   支持HTTP请求和响应的压缩。
*   灵活的配置：基于 name 粒度进行配置
*   支持多种客户端：JDK URLConnection、apache httpclient、okhttp，ribbon）
*   支持日志
*   支持错误重试
*   url支持占位符
*   可以不依赖注册中心独立运行

```
重点来了，总结！！！！！！
```

## 总结

*   在你还在纠结选择apache httpclient时，Android已经不用它了，改用okhttp了
*   当你还在纠结选择apache httpclient还是okhttp时，Square已经出了Retrofit，网友已经在说既然你都用了okhttp为何不直接使用Retrofit

**总的来说技术变化更新都比较快，得跟上技术的发展。一般来说没用使用springcloud话可以选择Retrofit，如果使用了springcloud可以使用OpenFeign+okHttp。**
