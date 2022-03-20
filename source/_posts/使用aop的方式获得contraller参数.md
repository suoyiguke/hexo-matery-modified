---
title: 使用aop的方式获得contraller参数.md
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
title: 使用aop的方式获得contraller参数.md
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
~~~
package org.szwj.ca.identityauthsrv.timeconsum;

import com.alibaba.fastjson.JSON;
import javax.servlet.http.HttpServletRequest;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

@Aspect
@Configuration
public class CheckAspect {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    // 定义切点Pointcut  自行写入对应的controller包路径
    @Pointcut("execution(* org.szwj.ca.identityauthsrv.controller.*.*(..))")
    public void excudeService() {
    }

    @Around("excudeService()")
    public Object doAround(ProceedingJoinPoint pjp) throws Throwable {
        RequestAttributes ra = RequestContextHolder.getRequestAttributes();
        ServletRequestAttributes sra = (ServletRequestAttributes) ra;
        HttpServletRequest request = sra.getRequest();

        String url = request.getRequestURL().toString();
        String method = request.getMethod();
        String uri = request.getRequestURI();
        String queryString = request.getQueryString();
        //这里可以获取到get请求的参数和其他信息
        logger.info("请求开始, 各个参数, url: {}, method: {}, uri: {}, params: {}", url, method, uri,
            queryString);
        //重点 这里就是获取@RequestBody参数的关键  调试的情况下 可以看到o变量已经获取到了请求的参数
        Object[] o = pjp.getArgs();
        for (Object o1 : o) {

            try {
                String s = JSON.toJSONString(o1);
                System.out.println(s);
            } catch (Exception e) {
                System.out.println(o1);
            }

        }

        // result的值就是被拦截方法的返回值
        Object result = pjp.proceed();
        return result;
    }

}

~~~
