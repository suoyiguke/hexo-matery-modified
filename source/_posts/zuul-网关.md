---
title: zuul-网关.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springcloud
categories: springcloud
---
---
title: zuul-网关.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springcloud
categories: springcloud
---
zuul的功能主要包括 
>路由和过滤
- 路由就类似于 ngnix的反向代理
- 过滤

> 这个代理服务，可以放到任意组件之前。之前我的理解就是放到服务提供者之前，这是不全面的！只要是一个http服务它都可以被代理

###路由


~~~

eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8888/eureka/
  instance:
    hostname: localhost
    prefer-ip-address: true # 使用ip地址注册。否则会默认使用主机名
    instance-id: ${spring.cloud.client.ip-address}:${server.port}
zuul:
#需要忽略的头部信息，不在传播到其他服务
    sensitive-headers: Access-Control-Allow-Origin
    ignored-headers: Access-Control-Allow-Origin,H-APP-Id,Token,APPToken
    routes:
     apis1:
      path: /feign/**
      serviceId: spring-cloud-study-demo # 方法二，配置serviceId 根据serviceId自动重注册中心获取服务地址并转发请求
     apis2:
      path: /feign1/**
      url: http://127.0.0.1:9999/ # 方法一，直接配置被代理的 url
    ignored-patterns: /**/order/**  # URL 地址排除，排除所有包含/order的路径。这样就访问不到了
    ignored-services: order-service # 直接排除一个微服务的所有url，指定serviceId
    prefix: /api # 路由前缀。请求前要加这个
~~~

如上配置就会将 
http://192.168.6.1:7777/api/feign/demo/getMyTest/12
代理到
spring-cloud-study-demo(serviceId)/demo/getMyTest/12
###网关过滤器


- pre  请求被路由到源服务器之前执行的过滤器
- routing 转发到源服务器的过滤器
- post  返回时执行的过滤器
- error 前几部出错都会到这来
~~~
/**
 * 网关过滤器
 */
@Component
public class F extends ZuulFilter {

    @Override
    public Object run() {
        RequestContext ctx = RequestContext.getCurrentContext();
        HttpServletRequest request = ctx.getRequest();
        HttpServletResponse response = ctx.getResponse();

        System.out.println(String
            .format("%s AccessUserNameFilter request to %s", request.getMethod(),
                request.getRequestURL().toString()));

        String token = request.getParameter("token");
        boolean notBlank = StringUtils.isNotBlank(token);
        response.setContentType("application/json;charset=UTF-8");
        if(notBlank){
            try {
                response.getWriter().write("有权限");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }else{
            try {
                response.getWriter().write("无权限");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return null;
    }


    @Override
    public boolean shouldFilter() {
        return true;// 是否执行该过滤器，此处为true，说明需要过滤
    }

    @Override
    public int filterOrder() {
        return 0;// 优先级为0，数字越大，优先级越低
    }

    @Override
    public String filterType() {
        return "pre";// 前置过滤器
    }
}
~~~





###定义一个网关的异常处理filter
类似于单体应用中的全局异常处理器！就理解为微服务中的全局异常处理器就行了

之前
{"errorCode":"01","errorMessage":"服务器异常","returnObject":["/ by zero"]}

添加之后



~~~
zuul:
    SendErrorFilter:
      error:
        disable: true
~~~
~~~
package com.softdev.system.zuul.config;

import com.netflix.zuul.ZuulFilter;
import com.netflix.zuul.exception.ZuulException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import lombok.SneakyThrows;
import org.apache.http.protocol.RequestContent;
import com.netflix.zuul.context.RequestContext;
import org.springframework.cloud.netflix.zuul.filters.post.SendErrorFilter;
import org.springframework.stereotype.Component;

/**
 * 异常过滤器
 */
@Component
public class Error  extends SendErrorFilter {

    @Override
    public String filterType() {
        return "error";
    }

    @Override
    public int filterOrder() {
        return 0;
    }

    @Override
    public boolean shouldFilter() {
        return true;
    }

    @SneakyThrows
    @Override
    public Object run()   {
        HttpServletResponse response = RequestContext.getCurrentContext().getResponse();
        RequestContext ctx = RequestContext.getCurrentContext();

        ExceptionHolder exception = findZuulException(ctx.getThrowable());

        //这里可对不同异常返回不同的错误码
        response.getWriter().write("{\"code\":\"999999\",\"msg\":\"" + exception.getErrorCause() + "\"}");

        return super.run();
    }
}


~~~
