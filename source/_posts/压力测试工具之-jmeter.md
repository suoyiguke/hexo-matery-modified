---
title: 压力测试工具之-jmeter.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 测试
categories: 测试
---
---
title: 压力测试工具之-jmeter.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 测试
categories: 测试
---
>jmeter 很重要！在开发高并发应用是必须使用jmter压测一下！看看有没有性能问题，有没有线程安全问题


###线程组

元件描述：一个线程组可以看做一个虚拟用户组，线程组中的每个线程都可以理解为一个虚拟用户。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-eb851eb90016d185.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/13965490-2117383d49ef3e96.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.gif](https://upload-images.jianshu.io/upload_images/13965490-f9b6bed00c508259.gif?imageMogr2/auto-orient/strip)


>1、线程数：即虚拟用户数。设置多少个线程数也就是设置多少虚拟用户数
2、Ramp-Up时间(秒)：设置虚拟用户数全部启动的时长。如果线程数为20,准备时长为10秒,那么需要10秒钟启动20个线程。也就是平均每秒启动2个线程。
3、循环次数：每个线程发送请求的个数。如果线程数为20,循环次数为10,那么每个线程发送10次请求。总请求数为20*10=200。如果勾选了“永远”, 那么所有线程会一直发送请求,直到手动点击工具栏上的停止按钮,或者设置的线程时间结束。

####HTTP请求
定义需要测试的http接口基本信息
![image.png](https://upload-images.jianshu.io/upload_images/13965490-716bf41d2a8d233b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-be05f32982055434.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#####响应断言
定义什么情况下是成功请求。这里，是 状态码是200时，请求成功
![image.png](https://upload-images.jianshu.io/upload_images/13965490-503f9980cebf4d3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c89031f116224e41.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#####http信息头部管理器
当需要post json数据时，需要配置这个content-type=application/json
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1284745e672da971.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-01de97d4bb517d33.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#####新增监听器之 查看结果树
可以查看http请求的 请求和响应报文

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f5dcba4d475cffd0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####新增监听器之 聚合报告

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ab71d5b6ee06854f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面分别说下各个数据的意义，其中标成红色的是需要特别关注的。Label:请求的名称，就是我们在进行测试的httprequest sampler的名称

1、Samples  样本数 总共发给服务器的请求数量，如果模拟10个用户，每个用户迭代10次，那么总的请求数为：10*10 =100次；
2、Average:默认情况下是单个 Request 的平均响应时间，当使用了 Transaction Controller 时，以Transaction 为单位显示平均响应时间 ，单位是毫秒
3、Median: 50%用户的请求的响应时间，中位数
4、90%Line:90%的请求的响应时间
5、95%Line:95%的请求的响应时间
6、99%Line:99%的请求的响应时间
7、Min:最小的响应时间
8、Max:最大的响应时间
9、Error%:错误率=错误的请求的数量/请求的总数
10、  `重要` Throughput: 默认情况下表示每秒完成的请求数（Request per Second），当使用了 Transaction Controller 时，也可以表示类似 LoadRunner 的 Transaction per Second 数（类似QPS/TPS）
11、Received KB/sec: 每秒从服务器端接收到的数据量
12、Sent KB/sec： 每秒发生至服务器的数据量

最近测得
> tps:  8.4870911343846 次每秒
