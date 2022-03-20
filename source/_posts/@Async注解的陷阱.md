---
title: Async注解的陷阱.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: @Async注解的陷阱.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---


之前在java并发编程中实现异步功能，一般是需要使用`线程`或者`线程池`。

线程池的底层也是用的线程。

而实现一个线程，要么继承`Thread`类，要么实现`Runnable`接口，然后在run方法中写具体的业务逻辑代码。

开发spring的大神们，为了简化这类异步操作，已经帮我们把异步功能封装好了。spring中提供了`@Async`注解，我们可以通过它即可开启异步功能，使用起来非常方便。

具体做法如下：

1.在`springboot`的启动类上面加上`@EnableAsync`注解。

<pre data-tool="mdnice编辑器" style="margin: 10px 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box !important; overflow-wrap: break-word !important; color: rgb(63, 63, 63); font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: 0.544px; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-style: initial; text-decoration-color: initial; border-radius: 5px; box-shadow: rgba(0, 0, 0, 0.55) 0px 2px 10px;">`@EnableAsync
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}` </pre>

2.在需要执行异步调用的业务方法加上`@Async`注解。

<pre data-tool="mdnice编辑器" style="margin: 10px 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box !important; overflow-wrap: break-word !important; color: rgb(63, 63, 63); font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: 0.544px; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-style: initial; text-decoration-color: initial; border-radius: 5px; box-shadow: rgba(0, 0, 0, 0.55) 0px 2px 10px;">`@Service
public class CategoryService {

     @Async
     public void add(Category category) {
        //添加分类
     }
}` </pre>

3.在controller方法中调用这个业务方法。

<pre data-tool="mdnice编辑器" style="margin: 10px 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box !important; overflow-wrap: break-word !important; color: rgb(63, 63, 63); font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: 0.544px; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-style: initial; text-decoration-color: initial; border-radius: 5px; box-shadow: rgba(0, 0, 0, 0.55) 0px 2px 10px;">`@RestController
@RequestMapping("/category")
public class CategoryController {

     @Autowired
     private CategoryService categoryService;

     @PostMapping("/add")
     public void add(@RequestBody category) {
        categoryService.add(category);
     }
}` </pre>

这样就能开启异步功能了。

是不是很easy？

但有个坏消息是：用@Async注解开启的异步功能，会调用`AsyncExecutionAspectSupport`类的`doSubmit`方法。

![图片](https://upload-images.jianshu.io/upload_images/13965490-f6337bb9f51802d1?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

默认情况会走else逻辑。

而else的逻辑最终会调用doExecute方法：

<pre data-tool="mdnice编辑器" style="margin: 10px 0px; padding: 0px; outline: 0px; max-width: 100%; box-sizing: border-box !important; overflow-wrap: break-word !important; color: rgb(63, 63, 63); font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: 0.544px; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-style: initial; text-decoration-color: initial; border-radius: 5px; box-shadow: rgba(0, 0, 0, 0.55) 0px 2px 10px;">`protected void doExecute(Runnable task) {
  Thread thread = (this.threadFactory != null ? this.threadFactory.newThread(task) : createThread(task));
  thread.start();
}` </pre>

我去，这不是每次都会创建一个新线程吗？

没错，使用@Async注解开启的异步功能，默认情况下，每次都会创建一个新线程。

如果在高并发的场景下，可能会产生大量的线程，从而导致OOM问题。

> 建议大家在@Async注解开启的异步功能时，请别忘了定义一个`线程池`。
