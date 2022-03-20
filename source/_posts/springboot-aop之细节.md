---
title: springboot-aop之细节.md
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
title: springboot-aop之细节.md
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
1、ProceedingJoinPoint对象详解
~~~

    /**
     * @description 使用环绕通知
     */
    @Around("BrokerAspect()")
    public Object doAroundFunction(ProceedingJoinPoint point) throws Throwable {

        String kind = point.getKind();
        System.out.println(kind);

        Object aThis = point.getThis();
        System.out.println(aThis);

        Class<? extends ProceedingJoinPoint> aClass = point.getClass();
        System.out.println(aClass);

        JoinPoint.StaticPart staticPart = point.getStaticPart();
        System.out.println(staticPart);

        Object target1 = point.getTarget();
        System.out.println(target1);

        SourceLocation sourceLocation = point.getSourceLocation();
        System.out.println(sourceLocation);

        Signature signature = point.getSignature();
        System.out.println(signature);


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

2、@within和@annotation的区别：
@within 对象级别

@annotation 方法级别
