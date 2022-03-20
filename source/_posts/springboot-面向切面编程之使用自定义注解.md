---
title: springboot-面向切面编程之使用自定义注解.md
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
title: springboot-面向切面编程之使用自定义注解.md
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
我们知道使用@Pointcut注解定义切点，它的value属性可以是`切点表达式` 或者 `注解的全限定名`；若使用注解的方式，直接在目标切入点方法上加上自定义注解即可纳入AOP的管理


在创建自定义注解时有看到三个注解，分别了解它们的作用
~~~
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
~~~
######定义使用注解的地方
我们先来看看这个枚举类java.lang.annotation.ElementType就是定义注解使用的地方。比如 @Target(ElementType.METHOD) 就是只能用在方法上了。不过可以同时指定多个ElementType的属性来达到既可以用在方法上也可以用在类上的目的： @Target({ElementType.TYPE, ElementType.METHOD})

>- TYPE 申明在类、接口、枚举类上面
>- FIELD 申明在类属性上
>- METHOD 申明在方法上
>- PARAMETER  申明在形式参数上
>- CONSTRUCTOR 申明在构造器上
>- LOCAL_VARIABLE 申明在局部表量上
>- ANNOTATION_TYPE 批注类型
>- PACKAGE 申明在包上
>- TYPE_PARAMETER
>- TYPE_USE

~~~

public enum ElementType {
    /** Class, interface (including annotation type), or enum declaration */
    TYPE,

    /** Field declaration (includes enum constants) */
    FIELD,

    /** Method declaration */
    METHOD,

    /** Formal parameter declaration */
    PARAMETER,

    /** Constructor declaration */
    CONSTRUCTOR,

    /** Local variable declaration */
    LOCAL_VARIABLE,

    /** Annotation type declaration */
    ANNOTATION_TYPE,

    /** Package declaration */
    PACKAGE,

    /**
     * Type parameter declaration
     *
     * @since 1.8
     */
    TYPE_PARAMETER,

    /**
     * Use of a type
     *
     * @since 1.8
     */
    TYPE_USE
}

~~~
######再来看看@Documented注解

Documented注解表明这个注释是由 javadoc记录的。 如果一个类型声明被注释了文档化，它的注释成为公共API的一部分。

######注解的生命周期
再来看这个枚举类 java.lang.annotation.RetentionPolicy。该类主要功能是定义注解的`生命周期`

>1、RetentionPolicy.SOURCE：注解只保留在源代码，源代码被编译成字节码时注解被干掉。做一些检查性的操作，比如 @Override 和 @SuppressWarnings；还有生成格外的源代码，如lombok中的@Data
2、RetentionPolicy.CLASS：`这是默认的生命周期`。注解被保留到字节码中，注解在字节码被ClassLoader加载时被干掉。
3、RetentionPolicy.RUNTIME：注解不仅被保存到字节码中，ClassLoader加载之后，仍然存在；`如果需要在运行时去动态获取注解信息，那只能用 RUNTIME 注解`
4、这3个生命周期分别对应于：源代码 ---> .class文件 ---> jvm中的指令；生命周期长度 SOURCE < CLASS < RUNTIME 



~~~
package java.lang.annotation;

/**
 * Annotation retention policy.  The constants of this enumerated type
 * describe the various policies for retaining annotations.  They are used
 * in conjunction with the {@link Retention} meta-annotation type to specify
 * how long annotations are to be retained.
 *
 * @author  Joshua Bloch
 * @since 1.5
 */
public enum RetentionPolicy {
    /**
     * Annotations are to be discarded by the compiler.
     */
    SOURCE,

    /**
     * Annotations are to be recorded in the class file by the compiler
     * but need not be retained by the VM at run time.  This is the default
     * behavior.
     */
    CLASS,

    /**
     * Annotations are to be recorded in the class file by the compiler and
     * retained by the VM at run time, so they may be read reflectively.
     *
     * @see java.lang.reflect.AnnotatedElement
     */
    RUNTIME
}

~~~

###编写自定义注解
创建注解类TestAnnotation。里面有一个name参数，默认是no；没错，该注解只能用在方法上，不能用在类、接口；而且是运行时类型的
~~~
package com.springboot.study.demo1.aop.annotation;
import java.lang.annotation.*;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface TestAnnotation {
    String name() default "no";
}

~~~

在目标方法上使用注解
> 分别指定testAop1()和testAop2()方法的注解属性name值为 yes 和 on
~~~
package com.springboot.study.demo1.controller;
import com.baomidou.mybatisplus.extension.api.R;
import com.springboot.study.demo1.aop.annotation.TestAnnotation;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
/**
 /**
 *@description: UserController
 *@author: yinkai
 *@create: 2020/2/25 9:51
 */
@RestController
@RequestMapping("/aop")
public class AopController {
    @TestAnnotation(name="no")
    @RequestMapping("/testAop1")
    public R testAop1(){

        System.out.println("testAop1");
        return R.ok("ok");
    }


    @TestAnnotation(name="yes")
    @RequestMapping("/testAop2")
    public R testAop2(){
        System.out.println("testAop2");
        return R.ok("ok");
    }
}
~~~

创建切面类
> - @Pointcut注解定义切点，使用注解类的全限定名作为参数。表示只要在方法上用了该注解，那么该方法就会被aop管理
> - 在环绕通知方法中获得目标方法上申明的注解属性name，然后进行判断。分别进行不同的业务
~~~
package com.springboot.study.demo1.aop;

import com.springboot.study.demo1.aop.annotation.TestAnnotation;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.Signature;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.aspectj.lang.reflect.SourceLocation;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;

/**
 * @desc: 定义切面
 * @author: yinkai
 **/
@Aspect
@Component
public class BrokerAspect {

    @Pointcut("@annotation(com.springboot.study.demo1.aop.annotation.TestAnnotation)")
    public void BrokerAspect() {

    }


    /**
     * @description 使用环绕通知
     */
    @Around("BrokerAspect()")
    public Object doAroundFunction(ProceedingJoinPoint point) throws Throwable {

        MethodSignature signature = (MethodSignature) point.getSignature();
        //得到目标方法
        Method method = signature.getMethod();
        //得到方法之上的注解
        TestAnnotation testAnnotation = method.getAnnotation(TestAnnotation.class);
        //注解业务判断
        if ("yes".equals(testAnnotation.name())) {
            System.out.println("name的值为yes对应的业务");
        } else {
            System.out.println("name的值为no对应的业务");
        }
        return point.proceed();
    }
}
~~~

最后重启工程，访问http://localhost:8080/test/aop/testAop1和http://localhost:8080/test/aop/testAop2
![image.png](https://upload-images.jianshu.io/upload_images/13965490-13260947396c3f42.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
