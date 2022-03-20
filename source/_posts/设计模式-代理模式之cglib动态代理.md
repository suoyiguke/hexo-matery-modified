---
title: 设计模式-代理模式之cglib动态代理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 设计模式
categories: 设计模式
---
---
title: 设计模式-代理模式之cglib动态代理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 设计模式
categories: 设计模式
---
######cglib动态代理和jdk动态代理的区别
>- jdk动态代理是基于接口的方式，换句话来说就是代理类和目标类都实现同一个接口，那么代理类和目标类的方法名就一样了；
>- cjlib动态代理是代理类去继承目标类，然后重写其中目标类的方法啊，这样也可以保证代理类拥有目标类的同名方法；
>- 从执行效率上看，cjlib 动态代理效率较高。




###测试cglib动态代理的使用
创建需要被代理的类UserServiceImpl和CustomerServiceImpl ；他们分别实现了两个数相乘和两个数相加
~~~
package com.company;
 /**
  *@description: UserServiceImpl 被代理的类
  *@author: yinkai
  *@create: 2020/3/1 18:48
  */
public class UserServiceImpl {
    public Integer multiply(Integer x, Integer y) {
        int i = x * y;
        System.out.println("计算结果" + i );
        return i;
    }
}

package com.company;

/**
 *@program: testjava
 *@description:
 *@author: yinkai
 *@create: 2020-03-01 20:58
 */
public class CustomerServiceImpl {
    public Integer add(Integer a, Integer b) {
        int i = a + b;
        System.out.println("计算结果" + i );
        return i;
    }
}
~~~


创建拦截类MyMethodInterceptor实现MethodInterceptor接口重写intercept()方法；这个MethodInterceptor接口即是cjlib动态代理的核心！

~~~
package com.company;

import org.springframework.cglib.proxy.MethodInterceptor;
import org.springframework.cglib.proxy.MethodProxy;

import java.lang.reflect.Method;

/**
 *@program: MyMethodInterceptor
 *@description:
 *@author: yinkai
 *@create: 2020-03-02 11:33
 */
public class MyMethodInterceptor implements MethodInterceptor {
    @Override
    public Object intercept(Object object, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
        System.out.println("前置通知");
        Object re = methodProxy.invokeSuper(object, args);
        System.out.println("后置通知");
        return re;
    }
}
~~~

创建测试类

~~~
package com.company;
import org.springframework.cglib.proxy.Enhancer;

/**
 *@description: Main 测试类
 *@author: yinkai
 *@create: 2020/3/1 19:04
 */
public class Main {

    public static void main(String[] args) {
        Enhancer enhancer = new Enhancer();


        enhancer.setSuperclass(UserServiceImpl.class);
        enhancer.setCallback(new MyMethodInterceptor());
        UserServiceImpl userServiceImpl = (UserServiceImpl)enhancer.create();
         userServiceImpl.multiply(2, 4);

        System.out.println("==================================");
        enhancer.setSuperclass(CustomerServiceImpl.class);
        enhancer.setCallback(new MyMethodInterceptor());
        CustomerServiceImpl customerServiceImpl = (CustomerServiceImpl)enhancer.create();
        customerServiceImpl.add(2, 4);
    }
}
~~~

执行结果
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5505f419e57d7c64.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
使用debug看看customerServiceImpl 对象是个什么东西，里面显示了 CGLIB$的字眼
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3b883a28f2c7549e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######可以生成一下代理类来看看

~~~
 System.setProperty(DebuggingClassWriter.DEBUG_LOCATION_PROPERTY, "D:\\");
~~~
![](https://upload-images.jianshu.io/upload_images/13965490-eaf4a69695b0a7e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

用idea反编译如下
~~~
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package $java.lang;

import java.lang.reflect.InvocationTargetException;
import org.springframework.cglib.core.Signature;
import org.springframework.cglib.reflect.FastClass;

public class Object$$FastClassByCGLIB$$3f697993 extends FastClass {
    public Object$$FastClassByCGLIB$$3f697993(Class var1) {
        super(var1);
    }

    public int getIndex(Signature var1) {
        String var10000 = var1.toString();
        switch(var10000.hashCode()) {
        case 1826985398:
            if (var10000.equals("equals(Ljava/lang/Object;)Z")) {
                return 0;
            }
            break;
        case 1913648695:
            if (var10000.equals("toString()Ljava/lang/String;")) {
                return 1;
            }
            break;
        case 1984935277:
            if (var10000.equals("hashCode()I")) {
                return 2;
            }
        }

        return -1;
    }

    public int getIndex(String var1, Class[] var2) {
        switch(var1.hashCode()) {
        case -1776922004:
            if (var1.equals("toString")) {
                switch(var2.length) {
                case 0:
                    return 1;
                }
            }
            break;
        case -1295482945:
            if (var1.equals("equals")) {
                switch(var2.length) {
                case 1:
                    if (var2[0].getName().equals("java.lang.Object")) {
                        return 0;
                    }
                }
            }
            break;
        case 147696667:
            if (var1.equals("hashCode")) {
                switch(var2.length) {
                case 0:
                    return 2;
                }
            }
        }

        return -1;
    }

    public int getIndex(Class[] var1) {
        switch(var1.length) {
        case 0:
            return 0;
        default:
            return -1;
        }
    }

    public Object invoke(int var1, Object var2, Object[] var3) throws InvocationTargetException {
        Object var10000 = var2;
        int var10001 = var1;

        try {
            switch(var10001) {
            case 0:
                return new Boolean(var10000.equals(var3[0]));
            case 1:
                return var10000.toString();
            case 2:
                return new Integer(var10000.hashCode());
            }
        } catch (Throwable var4) {
            throw new InvocationTargetException(var4);
        }

        throw new IllegalArgumentException("Cannot find matching method/constructor");
    }

    public Object newInstance(int var1, Object[] var2) throws InvocationTargetException {
        Object var10000 = new Object;
        Object var10001 = var10000;
        int var10002 = var1;

        try {
            switch(var10002) {
            case 0:
                var10001.<init>();
                return var10000;
            }
        } catch (Throwable var3) {
            throw new InvocationTargetException(var3);
        }

        throw new IllegalArgumentException("Cannot find matching method/constructor");
    }

    public int getMaxIndex() {
        return 2;
    }
}

~~~
