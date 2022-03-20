---
title: springboot-集成aop面向切面编程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: springboot-集成aop面向切面编程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
###aop的应用场景
像spring的申明式事务、spring缓存实现、权限管理、多数据源、数据库读写分离、统计请求执行时间、系统日志等可用aop的方式实现。利于解耦

###aop的相关概念
> **切面（Aspect）**
 `需要封装的代码`，比如事务开启和关闭这样和业务没有直接依赖关系的模板代码

>  **通知（Advice）**
`何时使用切面`。spring中五中类型的通知：
前置通知（Before）：在目标方法被调用之前调用通知功能
后置通知（After）：在目标方法完成之后调用通知，不关心方法的输出是什么。是“返回通知”和“异常通知”的并集。
返回通知（After-returning）：在目标方法成功执行之后调用通知
异常通知（After-throwing）：在目标方法抛出异常后调用通知
环绕通知（Around）通知包裹了被通知的方法，可同时定义前置通知和后置通知、异常通知。



> **切点（Pointcut）**
`何地使用通知`。切点的定义会匹配通知所有要织入的一个或多个连接点。我们通常使用明确的`类和方法名称`，或是利用`切点表达式`甚至是`自定义注解`来定义所匹配的类和方法名称来指定这些切点。
 关于使用`自定义注解`做切点，我的这篇文章有讲解https://www.jianshu.com/p/6e02cf0822a5



###springboot集成aop功能

######引入依赖
~~~
        <!--引入AOP依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>
~~~

######定义目标切入点
通常是类的方法。这里使用controller中的一个方法
~~~
package com.springboot.study.demo1.controller;
import com.baomidou.mybatisplus.extension.api.R;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
/**
 /**
 *@description: AopController 
 *@author: yinkai
 *@create: 2020/2/25 9:51
 */
@RestController
@RequestMapping("/aop")
public class AopController {
    /**
     *@description: AopController 
     *@author: yinkai
     *@create: 2020/2/27 11:55
     */
    @RequestMapping("/testAop")
    public R testAop(){

        System.out.println("执行业务逻辑");
        return R.ok("ok");
    }
}
~~~

######定义切面类
>-  定义一个切面类需要使用@Aspect和@Component注解  
>-  使用   @Pointcut注解定义切入点，内部参数需要传入`切点表达式`
>-  使用 @Before、@After、 @AfterThrowing、  @AfterThrowing、@Around 定义五种类型的通知方法；注意注解里面的参数即是定义切入点@Pointcut注解所申明的方法名，我这里就是 BrokerAspect()

~~~
package com.springboot.study.demo1.aop;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;
/**
 * @desc: 定义切面
 * @author: yinkai
 **/
@Aspect
@Component
public class BrokerAspect {

    /**
     * 定义切入点，切入点为com.springboot.study.demo1.controller.AopController中的所有函数
     *通过@Pointcut注解声明频繁使用的切点表达式
     */
    @Pointcut("execution(public * com.springboot.study.demo1.controller.AopController.*(..)))")
    public void BrokerAspect(){

    }

    /**
     * @description  前置通知
     */
    @Before("BrokerAspect()")
    public void doBeforeFunction(){
        System.out.println("前置通知执行！");
    }

    /**
     * @description  后置通知
     */
    @After("BrokerAspect()")
    public void doAfterFunction(){
        System.out.println("后置通知执行！");
    }

    /**
     * @description  返回通知
     */
    @AfterReturning("BrokerAspect()")
    public void doAfterReturningFunction(){
        System.out.println("返回通知执行！");
    }

    /**
     * @description  异常通知
     */
    @AfterThrowing("BrokerAspect()")
    public void doAfterThrowingFunction(){
        System.out.println("异常通知执行！");
    }

}
~~~

配置完毕后运行工程，访问 url，http://localhost:8080/test/aop/testAop 调用切点方法testAop()
看看控制台
![image.png](https://upload-images.jianshu.io/upload_images/13965490-52cfcc973de8d19d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######使用环绕通知
环绕通知功能强大，包括了前置通知，返回通知 和 异常通知的功能
> - 使用 @Around注解申明环绕通知
> - 方法参数ProceedingJoinPoint point，调用point.proceed()方法即是调用切点方法testAop()，而且这个方法的返回值就是testAop()的返回值

修改切面类，添加方法
~~~

   
    /**
     * @description  使用环绕通知
     */
    @Around("BrokerAspect()")
    public void doAroundFunction(ProceedingJoinPoint point){
        try{
            System.out.println("环绕通知： 前置");
            R proceed = (R) point.proceed();
            System.out.println(proceed);
            System.out.println("环绕通知： 后置");
        }
        catch(Throwable e){
            System.out.println("环绕通知： 出现异常");
        }
    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-391e443e8d7085e1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果出现异常，则异常通知代替了后置通知。后置通知不会被执行
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e63cbcb873dc17d0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######切点表达式说明
![image.png](https://upload-images.jianshu.io/upload_images/13965490-788e034df9020ead.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######通知方法中得到目标方法的参数
目标方法修改，添加 int cs 参数
~~~
    @RequestMapping("/testAop")
    public R testAop(int cs){

        System.out.println("执行业务逻辑");
        return R.ok("ok");
    }
~~~

通知方法中如何得到目标方法testAop()的参数 int cs？

**方法1：**


定义切入点处修改
> 注意切点表达式添加了参数。BrokerAspect()方法也添加了形参
~~~
    @Pointcut("execution(public * com.springboot.study.demo1.controller.AopController.*(int)) && args(cs))")
    public void BrokerAspect(int cs){

    }

~~~
通知方法修改

> - doAroundFunction() 方法添加形参int cs。
> - 这里的cs参数就是controller中目标方法testAop()的cs参数了
~~~
    /**
     * @description  使用环绕通知
     */
    @Around("BrokerAspect(cs)")
    public void doAroundFunction(ProceedingJoinPoint point,int cs) throws Throwable {
            System.out.println("获得参数cs==>"+cs);
            R proceed = (R) point.proceed();
            System.out.println(proceed);
    }
~~~

修改完毕后，重启工程。访问 http://localhost:8080/test/aop/testAop?cs=123

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7fc484f4713386c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**方法2：**
~~~
 /**
     * @description 使用环绕通知
     */
    @Around("BrokerAspect()")
    public Object doAroundFunction(ProceedingJoinPoint point) throws Throwable {
        Object target = point.getTarget().getClass().getName();
        System.out.println("调用者==>" + target);
        //通过joinPoint.getArgs()获取Args参数
        Object[] args = point.getArgs();//2.传参
        for (int i = 0; i < args.length; i++) {
            System.out.println("参数==>" + args[i]);

        }
        return point.proceed();
    }
~~~
