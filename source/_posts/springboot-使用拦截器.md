---
title: springboot-使用拦截器.md
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
title: springboot-使用拦截器.md
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
> 天生我材必有用，千金散尽还复来

创建拦截器类Interceptor1 、Interceptor2 、Interceptor3 ，它们仅仅是类名不同而已。并实现HandlerInterceptor 接口
>- 实现接口中的preHandle、postHandle和afterCompletion方法
>- preHandle方法将在Controller方法执行之前进行调用，preHandle返回true则执行Controller方法；多个拦截器先后注册的话就`按注册顺序执行`
>- postHandle方法 在Controller方法执行之后执行；多个拦截器先后注册的话就`按注册顺序的相反方向执行`
>- afterCompletion方法 在DispatcherServlet进行视图的渲染之后执行；多个拦截器先后注册的话就`按注册顺序的相反方向执行`



~~~
package com.springboot.study.demo1.Interceptor;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
public class Interceptor1 implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object o) throws Exception {
        System.out.println(getClass() + "AAAAAAAAAAAAAAAAAAAAA");
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println(getClass() + "BBBBBBBBBBBBBBBBBBBB");
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        System.out.println(getClass() + "CCCCCCCCCCCCCCCCCCC");
    }
}
~~~

再实现WebMvcConfigurer 接口类的addInterceptors方法中
注册拦截器链
> addPathPatterns 添加拦截url
> excludePathPatterns 排除拦截url
> 拦截规则这里使用的是`/manager/**` 表示访问的url包含/manager/的都会被拦截；使用正则表达式也可

~~~
package com.springboot.study.demo1.config;
import com.alibaba.fastjson.serializer.SerializerFeature;
import com.alibaba.fastjson.support.config.FastJsonConfig;
import com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter;
import com.springboot.study.demo1.Interceptor.Interceptor1;
import com.springboot.study.demo1.Interceptor.Interceptor2;
import com.springboot.study.demo1.Interceptor.Interceptor3;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import java.util.ArrayList;
import java.util.List;

@Configuration
public class WebAppConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {


        /**
         * 拦截所有请求
         */
        registry.addInterceptor(new Interceptor1()).addPathPatterns("/manager/**");
        registry.addInterceptor(new Interceptor2()).addPathPatterns("/manager/**");
        registry.addInterceptor(new Interceptor3()).addPathPatterns("/manager/**");


    }
}
~~~
启动工程，访问http://localhost:8080/test/manager/test1 打印如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7e59cdc60fef7142.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以得出拦截器链执行顺序

>Interceptor1 preHandle ===> Interceptor2 preHandle=====>Interceptor3 preHandle
=====>Interceptor3 postHandle=====>Interceptor2 postHandle=====>Interceptor1 postHandle
=====>Interceptor3 afterCompletion=====>Interceptor2 afterCompletion=====>Interceptor1 afterCompletion

######使用自定义注解来规定拦截范围

可以在controller方法上使用自定义注解，表示该方法要被拦截

定义注解
~~~
package com.springboot.study.demo1.Interceptor;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target({ElementType.METHOD})// 用在方法上
@Retention(RetentionPolicy.RUNTIME)
public @interface IsInterceptor {

}
~~~

使用如下
~~~
package com.springboot.study.demo1.Interceptor;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
/**
 * @description: Interceptor1
 * @author: yinkai
 * @create: 2020/3/13 16:09
 */
public class Interceptor1 implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        IsInterceptor methodAnnotation = (((HandlerMethod) handler).getMethod()).getAnnotation(IsInterceptor.class);
        //存在注解
        if (methodAnnotation != null) {
            System.out.println(getClass() + "AAAAAAAAAAAAAAAAAAAA");
            return true;
        }
        return true;
    }


    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println(getClass() + "BBBBBBBBBBBBBBBBBBBB");
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        System.out.println(getClass() + "CCCCCCCCCCCCCCCCCCC");
    }
}
~~~


######拦截器中注入对象失败
![image.png](https://upload-images.jianshu.io/upload_images/13965490-eff86c702d89dded.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
因是 注册拦截器时重新new了一个，拦截器加载的时间点在springcontext之前，所以在拦截器中注入自然为null 。
所以就不能直接new 一个拦截器对象然后注册，需要将拦截器bean纳入搭配spring容器的管理才行，所以registry.addInterceptor(new...) 这个代码需要改成


~~~

    @Bean(name="LoginInterceptor")
    public HandlerInterceptor getLoginInterceptor(){
        return new LoginInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(getLoginInterceptor()).excludePathPatterns("/user/checkUser");
    }

~~~
