---
title: spring--事务管理之传播行为对回滚的影响（二）.md
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
title: spring--事务管理之传播行为对回滚的影响（二）.md
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
>世上无难事，只要肯攀登

不同service中的A方法中调用了B方法。两个方法只有一个用到事务，那么程序的最终结果和代码的执行顺序有很大关系




######A方法创建了事务，B方法无事务运行


我曾经以为在A方法中抛出运行时异常，A方法事务被回滚。B方法因为没有纳入事务的管理，所以对B方法毫无影响。但是经过我的实践这个想法是错误的，程序的最终结果其实和代码的执行顺序有很大关系。下面准备实验:


> 我们给InsertUsers方法加上REQUIRED级别的传播行为，给InsertCuser方法加上NOT_SUPPORTED级别的传播行为。让InsertUsers方法使用事务，InsertCuser方法无事务状态执行。这下肯定有人问：InsertCuser方法不加事务注解不就能保证InsertCuser无事务运行了吗？事实上因为spring的事务传播行为，InsertUsers会将事务传播给InsertCuser，导致两个方法都使用InsertUsers上的事务，所以必须要给InsertCuser方法加上NOT_SUPPORTED级别的传播行为。不信可以看看我的这篇文章 https://www.jianshu.com/p/bc3cbacf9e70 里面有做对应实验
~~~
  @Transactional(propagation = Propagation.REQUIRED)
   public void InsertUsers(Users users) {
     。。。
    }

  @Transactional(propagation=Propagation.NOT_SUPPORTED)
   public void InsertCuser(Cuser cuser) {
     。。。
   }
~~~


然后分别将下列引发运行时异常的语句放到InsertUsers方法或InsertCuser方法中，观察事务回滚情况
~~~
//运行时异常
int i = 1/0;
~~~

情况一：
- 如图在InsertUsers方法中，将抛出异常的代码行放到调用InsertCuser方法之前。程序运行至此出现异常后根本不会再往下执行了，也就是说InsertCuser方法不会得到执行！即使InsertCuser方法没有纳入事务的管理，可以理解为此时它也是执行不成功的~ 查看cuser表数据为空验证了这个结论
![image.png](https://upload-images.jianshu.io/upload_images/13965490-86c40681ee1b41a0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 再来看抛出异常的代码行放到调用InsertCuser方法后，结果就不同了。此时InsertCuser方法会得到执行，因为InsertCuser方法没有纳入到事务管理，它不会回滚。执行程序后查看数据库cuser表数据多出了一行，users表中没有数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fb0627061f87e765.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

情况二： 
- 再将除0异常代码放到没有纳入事务管理的InsertCuser方法方法中，观察事务回滚情况
把出现异常代码行放到数据库操作之前，程序运行结果是 InsertUsers和InsertCuser方法数据库操作均失效。因为InsertUsers中存在事务，InsertCuser会隐式抛出运行时异常到InsertUsers中，InsertUsers事务得到回滚；而InsertCuser自身数据库操作失效的原因是数据库操作语句那行根本没有得到执行。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-70328223c3bcb335.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 若把异常代码行放到数据库操作之后，这次InsertUsers同样因为事务遇到异常而回滚，而InsertCuser操作成功执行。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c9b1da95312b1f70.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)








######A方法无事务运行，B创建事务
> 我们不给InsertUsers方法使用事务注解，给InsertCuser方法加上REQUIRED级别的传播行为。让InsertUsers无事务状态执行，InsertCuser方法创建事务。InsertUsers之所以没有纳入事务的管理是因为`事务不会从被调用者传播到调用者`
~~~
   public void InsertUsers(Users users)  {
     。。。
   }

   @Transactional(propagation=Propagation.REQUIRED)
   public void InsertCuser(Cuser cuser)  {
     。。。
   }
~~~

情况一：
- 在InsertUsers方法中，把异常代码行放到insert语句之前
两者都不会插入数据成功，都是因为没有执行到那里去就报异常了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f9dd914dd910a192.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 在InsertUsers方法中，把异常代码行放到insert语句之后，调用InsertCuser方法之前；程序运行结果是InsertUsers插入数据成功因为InsertUsers没有纳入事务的管理，InsertCuser插入数据失败因为没有执行到那里去
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2536f497c67b5787.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

-  在InsertUsers方法中，把异常代码行放到调用InsertCuser方法之后；此时程序的运行结果是：InsertUsers插入数据成功，因为InsertUsers没有纳入事务的管理。InsertCuser插入数据也成功，这里可能很多人不理解，因为这个`int i =1/0` 引发的运行时异常只在本方法中会影响回滚，也就是说它无法影响已经执行完毕提交的InsertCuser方法中的事务
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ccb0aff01015a05f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

情况二：
无论将`int i =1/0`放InsertCuser方法块中的哪里，结果都是一样的。
InsertUsers方法插入数据成功，因为它不在事务之内。InsertCuser方法插入数据失败，因为抛出异常事务回滚

###大总结
A方法调用B方法；这里的上指的是调用者，下指的是被调用者

- 异常总是向上抛出，B方法会将异常抛出到A方法
- 事务总是伴随着异常的抛出而回滚，而且B方法事务如果进行抛出会影响到A方法的事务。 `方法中如果将异常抛出给上层调用者方法，那么当前方法的事务会回滚` 像除0异常这种运行时异常是隐式抛出的不用管、受检异常就必须显式抛出，本方法的事务才会回滚
- 事务总是向下传播，A方法中有事务，B方法中没事务。A方法可能会将事务传播给B方法
