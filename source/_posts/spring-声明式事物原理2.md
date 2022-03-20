---
title: spring-声明式事物原理2.md
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
title: spring-声明式事物原理2.md
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
**Why?**

这要从动态代理的底层原理说起（请参考之前动态代理相关的文章），简而言之就是下面这幅图：

![image](https://upload-images.jianshu.io/upload_images/13965490-a5e2ebabc0e73a1f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

动态代理的原理是，我们可以在InvocationHandler的invoke()方法中使用target目标对象调用目标方法，最终得到的效果和静态代理是一样的：

![image](https://upload-images.jianshu.io/upload_images/13965490-152e5b4e71bdf99d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

所以在add()方法里使用this，其实得到的是target，也就是目标对象，而不是代理对象。

Spring自动注入时，其实是把代理对象注入到每一个@Autowired private UserService userService中。我们在Controller调用userService代理对象的add()方法时，最终会转到目标对象的add()方法。

讲完上面方法1的原理，方法2和方法3就无需多言了吧。只不过方法3得到代理对象的方式有点奇特：

![image](https://upload-images.jianshu.io/upload_images/13965490-9b1bb282ddf25d78.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最后的最后，在讨论事务控制是否起效时，本文的一切论点都是基于以下2点：

*   首先，要是代理对象
*   其次，方法上要有@Transactional（或者xml配置形式）

至于为什么代理对象的方法上加了@Transactional就会触发事务，需要去看Spring的AOP源码，里面涉及到了责任链模式和递归算法。大体思路是：

0.在Spring AOP的世界里，一个个增强方法（增强代码）会被包装成一个个拦截器，放在拦截器链中。

1.**代理对象**调用**每个**方法时，其实最终都会被导向一个叫CglibAopProxy.intercept()的方法，而这个方法会判断当前方法有没有需要执行的拦截器链chain。

![image](https://upload-images.jianshu.io/upload_images/13965490-5217564e1dccc5f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

简单来说就是：

<pre data-language="java" id="kJwYQ" class="ne-codeblock language-java" style="border: 1px solid #e8e8e8; border-radius: 2px; background: #f9f9f9; padding: 16px; font-size: 13px; color: #595959">// 获取拦截器链

if(chain.isEmpty() && Modifier.isPublic(method.getModifiers())){
    // 执行目标方法
} else {
    // 走拦截器链...
}</pre>

点进去else分支的代码，会看到：

![image](https://upload-images.jianshu.io/upload_images/13965490-42d096844528a8db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

“方法为public”时才会返回methodProxy，也能被代理。也验证了@Transactional失效的另一个情况：方法不为public时，@Transactional失效。

2.当public方法加了@Transactional，事务控制的代码就会被加入到拦截器链中，最终就会出现在事务方法的前后调用。

![image](https://upload-images.jianshu.io/upload_images/13965490-5dc0dbf936a733cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/13965490-66d29522805a8b63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

特别要注意，任何Java代码层面的事务控制其实还是依赖于setAutoCommit(false)，也就是先关闭默认提交，此时MySQL底层就会通过日志把一连串操作先记录起来，最后一起提交。如果中间失败了，仍可根据日志回滚。具体实现细节可以去查阅MySQL事务相关资料。

另外大家可以关注下上面invokeWithinTransaction()的第二行代码，里面有一句

tas.getTransactionAttribute(method, targetClass)

本质就是传入当前事务方法和Class对象，读取上面@Transactional的注解属性，比如我们对rollbackFor和propagation的设置。

![image](https://upload-images.jianshu.io/upload_images/13965490-d1f549b7ea7b2912.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后再往下会调用

TransactionInfo txInfo = createTransactionIfNecessary(tm, txAttr, joinpointIdentification);

传入一些参数判断决定是否真的开启事务（名字很形象，createTransactionIfNecessary），如果我们没有使用@Transactional，就不会开启事务了。

# 重新理解rollbackFor和propagation

相信大家以前也看了很多类似的文章，但是看完就忘了。既然花了时间，肯定还是希望能一劳永逸。所以本文也不打算这么蜻蜓点水般结束，而是来个回马枪，和大家一起重新看看这两个属性，相信理解会更深刻。

先说结论：

*   并不是所有的异常都会触发事务回滚，所以最好指定rollbackFor（一般图省事都直接指定Exception.class）
*   propagation是写给调用者看的，而不是写给被调用者看的（一句话解释有点晦涩，后面展开）

## 最好指定rollbackFor

我们来看看rollbackFor的注释：

![image](https://upload-images.jianshu.io/upload_images/13965490-2eaef0d5c2edd6ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

也即是说，虽然rollbackFor默认指定了异常类型，但仅仅包括Error和RuntimeException。如果是其他自定义的业务异常，就不会触发回滚（理论上是这样，但通常业务异常都会继承自RuntimeException，因为运行时异常无需强制处理）。

## propagation的案例

接下来结合上面的selectUser()，我们来看看propagation每种情况的具体演示。

### Propagation.REQUIRED

如果当前存在事务，则加入该事务，如果当前不存在事务，则创建一个新的事务。**(** 也就是说如果A方法和B方法都添加了注解，在默认传播模式下，A方法内部调用B方法，会把两个方法的事务合并为一个事务 **）**

**selectUser()和updateUser()都加上事务控制时，虽然内部调用还是this.updateUser()，是普通方法调用，但整体上在selectUser()的事务中。**

### Propagation.SUPPORTS

如果当前存在事务，则加入该事务；如果当前不存在事务，则以非事务的方式继续运行。

![image](https://upload-images.jianshu.io/upload_images/13965490-8da892500bd50e89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/13965490-dc2bb5c8d141e135.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

事务失效了。

原因是test方法调用userService.selectUser()时，本身是没有事务的，而刚好selectUser()使用了SUPPORT：**当前**存在事务，则加入事务；如果不存在事务，则以非事务方式继续运行。

这里所谓的**当前**，其实就是指**调用方**，即调用selectUser()的方法是否存在事务。由于test不存在事务，于是selectUser()也就没有事务，而this.updateUser()本身事务失效，所以最终整个调用事务失效。

如果希望selectUser()事务起效，SUPPORTS的情况下，可以给调用方加@Transactional：

![image](https://upload-images.jianshu.io/upload_images/13965490-32c635a354deeb0d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/13965490-1516049536a87b1c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### Propagation.MANDATORY

**mandatory：强制的。**

如果当前存在事务，则加入该事务；如果当前不存在事务，则抛出异常。**也就是要求调用方必须存在事务。**

![image](https://upload-images.jianshu.io/upload_images/13965490-ab1bad2f6b70ac3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同理，给test方法加上事务，那么selectUser()就会处于test的事务中，不会抛异常。

看到这里，大家是不是同意本小节开头说的那句话了呢：

propagation是写给调用者(test)看的，而不是写给被调用者(updateUser)看的

### Propagation.REQUIRES_NEW

重新创建一个新的事务，和外面的事务相互独立。

比如：

<pre data-language="java" id="ImnHk" class="ne-codeblock language-java" style="border: 1px solid #e8e8e8; border-radius: 2px; background: #f9f9f9; padding: 16px; font-size: 13px; color: #595959">@Transactional(rollbackFor = Exception.class, propagation = Propagation.REQUIRED)
methodA(){
    // 1.插入a表
    ...
    // 2.调用methodB
    methodB();
    // 3.在methodA抛异常，回滚
    int i = 1/0;
}

@Transactional(rollbackFor = Exception.class, propagation = Propagation.REQUIRES_NEW)
methodB(){
    // 4.插入b表
}</pre>

methodA抛异常了，回滚了，但是methodB还是会插入记录。因为methodB是REQUIRES_NEW，自己起了一个事务。也就是说，methodA和methodB各管各的，无论是谁的内部抛异常都不会影响外部回滚。

### Propagation.NOT_SUPPORTED

以非事务的方式运行，无论调用者是否存在事务，自己都不受其影响。和Propagation.REQUIRES_NEW有点像，但NOT_SUPPORTED自己是没有事务的。

### Propagation.NEVER

以非事务的方式运行，如果当前存在事务，则抛出异常。即如果methodB设置了NEVER，而methodA设置了事务，那么调用methodB时就会抛异常。它不想在有事务的方法内运行。

### Propagation.NESTED

和Propagation.REQUIRED效果一样。

最后说一句，我平时就看过第一、第二种。99%情况下都是默认REQUIRED，只需注意rollbackFor即可。

本文讨论是**同类**内的**非事务方法**调用**事务方法**，而不是调用其他类的事务方法，那和代理对象调用没区别。

<pre data-language="java" id="RXMOP" class="ne-codeblock language-java" style="border: 1px solid #e8e8e8; border-radius: 2px; background: #f9f9f9; padding: 16px; font-size: 13px; color: #595959">@Service
class UserServiceImpl implements UserService {
    @Autowired
    private StudentService studentService;

    public void methodA(){
        // 方法内部的一些操作
        ...

        // 调用同类的methodB()
        methodB();

        // 调用StudentService的方法
        studentService.methodC();     
    }

    @Transactional(rollbackFor = Exception.class)
    public void methodB(){

    }
}</pre>

另外，大家以前可能在各种平台看过@Async注解也存在同类方法调用失效的问题。看完这篇文章，你觉得是为什么呢~
