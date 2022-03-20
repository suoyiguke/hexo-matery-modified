---
title: ReflectionUtils-反射工具类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: ReflectionUtils-反射工具类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
ReflectionUtils


1、反射调用方法

~~~
	/**
	 * Make the given method accessible, explicitly setting it accessible if
	 * necessary. The {@code setAccessible(true)} method is only called
	 * when actually necessary, to avoid unnecessary conflicts with a JVM
	 * SecurityManager (if active).
	 * @param method the method to make accessible
	 * @see java.lang.reflect.Method#setAccessible
	 */
	public static void makeAccessible(Method method) {
		if ((!Modifier.isPublic(method.getModifiers()) ||
				!Modifier.isPublic(method.getDeclaringClass().getModifiers())) && !method.isAccessible()) {
			method.setAccessible(true);
		}
	}
~~~

调用：
ReflectionUtils.makeAccessible(this.method);
this.method.invoke(this.target);

~~~
package org.szwj.ca.identityauthsrv;


import java.lang.reflect.Method;
import java.util.concurrent.TimeUnit;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.util.ReflectionUtils;

@Configuration
@EnableScheduling
public class Test {


    @Scheduled(cron = "0/1 * * * * ?")
    public void queryQRCodeStatus() throws InterruptedException {

        System.out.println("13");

        TimeUnit.SECONDS.sleep(1);
    }

    public  void print(String z) {
        System.out.println(z);
    }

    public static void printS(String z) {
        System.out.println(z);

    }

    public static void main(String[] args) {
        Method method1 = ReflectionUtils
            .findMethod(Test.class, "print", String.class);
        ReflectionUtils.invokeMethod(method1, new Test(), "实例方法");


        Method method2 = ReflectionUtils
            .findMethod(Test.class, "printS", String.class);
        ReflectionUtils.invokeMethod(method2, null, "静态方法");
    }
}



~~~
