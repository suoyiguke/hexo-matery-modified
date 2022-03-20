---
title: spring-aop-不能对静态方法进行增强解决.md
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
title: spring-aop-不能对静态方法进行增强解决.md
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

想要通过aop的方式记录HttpUtils发出的post请求日志，但是 aop 不能对静态方法进行增强。只能对实例方法进行增强。。


如果一定要增强静态方法，我们可以对目标类使用单例模式，然后通过调用实例方法去调用那个静态方法，而且对应的对象实例必须纳入spring容器管理，因此可以使用@Component申明下`(注意不能直接new，直接new的对象不会纳入ioc管理，这样就不会被aop识别)`，然后在set实例方法上使用 @Autowired，将对象注入到 static修饰的 静态类对象。这样就可以使用 HttpsClientUtils.getHttpsClientUtils().HttpsPost() 实例方法来调用了，随后HttpsPost()方法就会被aop所拦截。


目标类：

~~~
@Component
public class HttpsClientUtils {
    private static HttpsClientUtils httpsClientUtils;

    @Autowired
    public void setHttpsClientUtils(
        HttpsClientUtils httpsClientUtils) {
        HttpsClientUtils.httpsClientUtils = httpsClientUtils;
    }


    public static HttpsClientUtils getHttpsClientUtils() {
        return httpsClientUtils;
    } 

   /**
     * 在上面添加的一个实例方法，用于aop识别
     */
    public String HttpsPost(String url, String param) throws CaHelperException {
        Map<String, String> header = new HashMap<>();
        header.put("Content-Type", "application/json");
        return HttpsPost(url, param, header);
    }

    /**
     * 需要被aop增强的静态方法
     */
    public static String HttpsPost(String url, String param, Map<String, String> header)
        throws CaHelperException {
        return HttpsRequest(url, param, header);
    }

}
~~~

aop类，实现记录日志记录的逻辑
~~~
package org.szwj.ca.identityauthsrv.log;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @description: AOP日志实现
 * @author: yinkai
 * @create: 2020/7/28 9:38
 */
@Aspect
public class BrokerAspectInHttpSend {

    /**
     * 定义切入点，拦截所有发起的第三方证书商的请求 拦截指定工具类 org.szwj.ca.identityauthsrv.util.common.http.HttpsClientUtils
     */
    @Pointcut("execution(public * org.szwj.ca.identityauthsrv.util.common.http.HttpsClientUtils.*(..)))")
    public void BrokerAspectInHttpSend() {

    }


    /**
     * @description 环绕通知打印IAS中所有的Controller的信息
     */
    @Around("BrokerAspectInHttpSend()")
    public Object httpUtilAround(ProceedingJoinPoint jp) throws Throwable {
        Logger logger = LoggerFactory.getLogger(jp.getTarget().getClass());

        logger.warn(
            "############################发起证书商http请求开始############################################");
        Object proceed = null;
        try {
            // 获取处理请求的类方法
            logger.warn("class_method={}",
                jp.getSignature().getDeclaringTypeName() + "." + jp.getSignature()
                    .getName() + "()");
            // 获取请求方法传入的参数
            logger.warn("args={}", ToStringBuilder.reflectionToString(jp.getArgs()));
            proceed = jp.proceed();
            logger.warn("retrun={}", proceed);
        } catch (Throwable throwable) {
            logger.error("出现异常 {}", throwable.getMessage());
        }

        logger.warn(
            "############################发起证书商http请求结束############################################");

        return proceed;
    }


}

~~~
