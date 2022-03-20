---
title: spring-aop方式打印日志.md
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
title: spring-aop方式打印日志.md
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
   @Bean
    @ConditionalOnExpression("#{'true'.equals(environment['print.server.http.log.enabled'])}")
    public BrokerAspectInController brokerAspectInController() {
        return new BrokerAspectInController();
    }
~~~


~~~
package org.szwj.ca.identityauthsrv.log;

import javax.servlet.http.HttpServletRequest;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;


/**
 * @description: AOP日志实现
 * @author: yinkai
 * @create: 2020/7/28 9:38
 */
@Aspect
public class BrokerAspectInController {


    /**
     * 定义切入点，切入点为IAS中所有Controller中的所有方法
     */
    @Pointcut("execution(public * org.szwj.ca.identityauthsrv.controller.*.*(..)))")
    public void BrokerAspectInController() {

    }

    /**
     * @description 环绕通知打印IAS中所有的Controller的信息
     */
    @Around("BrokerAspectInController()")
    public Object controllerAround(ProceedingJoinPoint jp) throws Throwable {
        Logger logger = LoggerFactory.getLogger(jp.getTarget().getClass());

        logger.warn(
            "############################收到http请求开始############################################");
        Object proceed = null;
        try {
            ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder
                .getRequestAttributes();
            HttpServletRequest request = attributes.getRequest();
            // 获取url
            logger.warn("url={}", request.getRequestURL());
            // 获取请求method
            logger.warn("method={}", request.getMethod());
            // 获取ip
            logger.warn("ip={}", request.getRemoteAddr());
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
            "############################收到http请求结束############################################");

        return proceed;
    }


}
~~~


打印慢接口日志

~~~
package org.szwj.ca.identityauthsrv.log;

import java.util.Arrays;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.szwj.ca.identityauthsrv.constants.Constants;
import org.szwj.ca.identityauthsrv.dao.DataDao;
import org.szwj.ca.identityauthsrv.entity.dao.BizConfig;
import org.szwj.ca.identityauthsrv.entity.dao.SlowInterface;
import org.szwj.ca.identityauthsrv.service.intfc.BizConfigService;

@Aspect
@Configuration
public class TimeConsumAspect {

    @Autowired
    private DataDao dataDao;
    @Autowired
    private BizConfigService bizConfigService;
    private final static Logger logger = LoggerFactory.getLogger(TimeConsumAspect.class);

    @Pointcut("execution(* org.szwj.ca.identityauthsrv.controller.*.*(..))")
    public void excudeService() {
    }

    @Around("excudeService()")
    public Object doAround(ProceedingJoinPoint pjp) throws Throwable {
        Object[] o = pjp.getArgs();
        String param = Arrays.toString(o);
        // 请求开始时间
        long startTime = System.currentTimeMillis();
        try {
            return pjp.proceed();
        } catch (Exception e) {
            logger.error(e.toString());
            throw e;
        } finally {
            // 请求结束时间
            Long endTime = System.currentTimeMillis();
            double time = ((endTime - startTime) * 1.000) / 1000;
            BizConfig bizConfigByKey = bizConfigService.getBizConfigByKey(
                Constants.INTERFACE_RESPONSE_TIME_ENABLE);
            if (bizConfigByKey != null) {
                Integer value = Integer.valueOf(bizConfigByKey.getValue());
                if (time >= value) {
                    SlowInterface slowInterface = new SlowInterface();
                    slowInterface.setTime(time);
                    slowInterface.setMethodName(
                        ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes())
                            .getRequest().getServletPath());
                    slowInterface.setParam(param);
                    dataDao.addSlowInterface(slowInterface);
                }
            }
        }

    }
}

~~~
