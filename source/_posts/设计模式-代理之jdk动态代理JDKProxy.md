---
title: 设计模式-代理之jdk动态代理JDKProxy.md
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
title: 设计模式-代理之jdk动态代理JDKProxy.md
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
使用JDK动态代理，目标类必须实现的某个接口，如果某个类没有实现接口则不能生成代理对象。 java动态代理主要依靠InvocationHandler接口实现；实际上JDK Proxy是不会去产生源代码的，而是直接生成类的原始数据

实现方式： 目标类 + 目标类接口 + 实现 InvocationHandler接口的类 


######使用jdk动态代理

创建UserService 接口和实现类UserServiceImpl
~~~
package com.company;

/**
 *@description: UserService 被代理的类中的接口
 *@author: yinkai
 *@create: 2020/3/1 18:35
 */
public interface UserService {
    Integer multiply (Integer a,Integer b);
}

package com.company;
 /**
  *@description: UserServiceImpl 被代理的类
  *@author: yinkai
  *@create: 2020/3/1 18:48
  */
public class UserServiceImpl implements UserService {
    @Override
    public Integer multiply(Integer x, Integer y) {
        int i = x * y;
        System.out.println("计算结果" + i );

        return i;
    }
}
~~~
创建CustomerService接口和实现类CustomerServiceImpl

~~~
package com.company;

/**
 * @author ceshi
 * @Title:
 * @Package
 * @Description:
 * @date 2020/3/120:58
 */
public interface CustomerService {
    Integer add(Integer a,Integer b);
}
package com.company;

/**
 *@program: testjava
 *@description:
 *@author: yinkai
 *@create: 2020-03-01 20:58
 */
public class CustomerServiceImpl implements CustomerService {
    @Override
    public Integer add(Integer a, Integer b) {
        int i = a + b;
        System.out.println("计算结果" + i );
        return i;
    }
}
~~~

创建方法拦截器类（类似于spring中的切面类）
> 需要实现InvocationHandler 接口，实现其中的invoke()方法;该方法就可以理解为spring中的环绕通知； method.invoke(target, args);就是调用代理对象的目标方法
> 需要定义一个Object类型的实例属性，程序运行期其实就是UserServiceImpl的实例；并为其设置一个set方法
~~~
package com.company;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;

/**
 *@description: Handler 方法拦截器; 必须实现java.lang.reflect.InvocationHandler接口，重写invoke方法
 *@author: yinkai
 *@create: 2020/3/1 18:49
 */
public class Handler implements InvocationHandler {
    //需要被代理的对象
    private Object target;

    public void setTarget(Object target) {
        this.target = target;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws IllegalAccessException, IllegalArgumentException, InvocationTargetException {
        System.out.println("打印方法"+ method);
        System.out.println("打印参数列表"+ Arrays.toString(args));

        System.out.println("前置通知");
        //调用方法
        Object result = method.invoke(target, args);
        System.out.println("后置通知");
        return result;
    }
}
~~~

创建代理工厂类
>   return Proxy.newProxyInstance(target.getClass().getClassLoader(), target.getClass().getInterfaces(), handler);
> 三个参数解释
>- ClassLoader loader 指定当前目标对象使用类加载器,获取加载器的方法是固定的 
>- Class<?>[] interfaces 目标对象实现的接口的类型,使用泛型方式确认类型 
>- InvocationHandler h 事件处理,执行目标对象的方法时,会触发事件处理器的方法,会把当前执行目标对象的方法作为参数传入

~~~
package com.company;
import java.lang.reflect.Proxy;
public class MyProxyFactory {
    /**
     * 为制定的target生成动态代理对象
     */
    public static Object getProxy(Object target) {
        //创建一个Handler对象
        Handler handler = new Handler();
        //Handler对象设置target对象
        handler.setTarget(target);
        //创建并返回一个动态代理
        return Proxy.newProxyInstance(target.getClass().getClassLoader(), target.getClass().getInterfaces(), handler);
    }
}

~~~

测试类
~~~
package com.company;

/**
 *@description: Main 测试类
 *@author: yinkai
 *@create: 2020/3/1 19:04
 */
public class Main {

    public static void main(String[] args){
        //创建一个原始的UserServiceImpl对象，作为target
        UserServiceImpl userServiceImpl = new UserServiceImpl();
        //以制定的target来创建动态代理对象,并将代理对象赋值给UserService 接口
        UserService userService = (UserService) MyProxyFactory.getProxy(userServiceImpl);
        //使用代理对象调用multiply()方法
        userService.multiply (4, 5);

        System.out.println("=================================");

        CustomerServiceImpl customerServiceImpl = new CustomerServiceImpl();
        CustomerService customerService = (CustomerService) MyProxyFactory.getProxy(customerServiceImpl);
        //使用代理对象调用add()方法
        customerService.add(1,2);
    }
}
~~~
运行结果
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b75b2c04b972a81c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

debug下可以看到生成的UserService 对象是 $Proxy（代理）的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-08dc4a9679e7706b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


