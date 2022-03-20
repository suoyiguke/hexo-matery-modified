---
title: CompletableFuture--方法分类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: CompletableFuture--方法分类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
CompletableFuture 大约有50种不同处理串行，并行，组合以及处理错误的方法。小弟屏幕不争气，方法之多，一个屏幕装不下，看到这么多方法，是不是瞬间要直接 收藏——>吃灰 2连走人？别担心，我们按照相应的命名和作用进行分类，分分钟搞定50多种方法

##CompletableFuture静态方法

 //返回一个新的CompletableFuture，该Future在所有给定CompletableFutures完成时完成。如果任何给定的CompletableFutures异常完成，那么返回的CompletableFutures也会这样做，CompletionException将此异常作为其原因。否则，给定的可完成期货的结果（如果有的话）不会反映在返回的可完成期货中，而是可以通过单独检查它们来获得。如果未提供CompletableFutures，则返回值为null的CompletableFutures。
这种方法的应用之一是在继续一个程序之前等待一组独立的CompletableFuture的完成，如：CompletableFuture。allOf（c1，c2，c3）。join（）；。
CompletableFuture<Void> voidCompletableFuture = CompletableFuture.allOf();


//返回一个新的CompletableFuture，该Future在任何给定CompletableFutures完成时完成，结果相同。否则，如果异常完成，则返回的CompletableFuture也会这样做，CompletionException将此异常作为其原因。如果未提供CompletableFutures，则返回一个不完整的CompletableFutures。
CompletableFuture<Object> objectCompletableFuture =CompletableFuture.anyOf(voidCompletableFuture);

//异线程执行
CompletableFuture.supplyAsync(() -> null);
//同线程执行
CompletableFuture.runAsync()


##CompletableFuture实例方法
###函数式接口
 run -> Runnable  无参无rerturn
 apply-> Function 一参一返回
 accept->Consumer 一参无返回

###单线程和异步
有Async和没有Async的方法有区别
CompletableFuture<Void> thenRun(Runnable action)
CompletableFuture<Void> thenRunAsync(Runnable action)

###链式调用类型
####串行关系
then 直译【然后】，也就是表示下一步，所以通常是一种串行关系体现, then 后面的单词（比如 run /apply/accept）就是上面说的函数式接口中的抽象方法名称了，它的作用和那几个函数式接口的作用是一样一样滴
~~~
//then
CompletableFuture<Void> thenRun(Runnable action)
CompletableFuture<Void> thenRunAsync(Runnable action)
CompletableFuture<Void> thenRunAsync(Runnable action, Executor executor)
  
<U> CompletableFuture<U> thenApply(Function<? super T,? extends U> fn)
<U> CompletableFuture<U> thenApplyAsync(Function<? super T,? extends U> fn)
<U> CompletableFuture<U> thenApplyAsync(Function<? super T,? extends U> fn, Executor executor)
  
CompletableFuture<Void> thenAccept(Consumer<? super T> action) 
CompletableFuture<Void> thenAcceptAsync(Consumer<? super T> action)
CompletableFuture<Void> thenAcceptAsync(Consumer<? super T> action, Executor executor)
  
<U> CompletableFuture<U> thenCompose(Function<? super T, ? extends CompletionStage<U>> fn)  
<U> CompletableFuture<U> thenComposeAsync(Function<? super T, ? extends CompletionStage<U>> fn)
<U> CompletableFuture<U> thenComposeAsync(Function<? super T, ? extends CompletionStage<U>> fn, Executor
~~~




####聚合 And 关系
 combine... with... 和 both...and... 都是要求两者都满足，也就是 and 的关系了
- Both 指的是两个Future都要完成，runAfterBoth、runAfterBothAsync；thenAcceptBoth、thenAcceptBothAsync；thenAcceptAsync、thenAcceptBothAsync
- combine 指的是两个Future都要完成，只有 thenCombine、thenCombineAsync 
~~~
//combine
<U,V> CompletableFuture<V> thenCombine(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn)
<U,V> CompletableFuture<V> thenCombineAsync(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn)
<U,V> CompletableFuture<V> thenCombineAsync(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn, Executor executor)

//Both
<U> CompletableFuture<Void> thenAcceptBoth(CompletionStage<? extends U> other, BiConsumer<? super T, ? super U> action)
<U> CompletableFuture<Void> thenAcceptBothAsync(CompletionStage<? extends U> other, BiConsumer<? super T, ? super U> action)
<U> CompletableFuture<Void> thenAcceptBothAsync( CompletionStage<? extends U> other, BiConsumer<? super T, ? super U> action, Executor executor)
  
CompletableFuture<Void> runAfterBoth(CompletionStage<?> other, Runnable action)
CompletableFuture<Void> runAfterBothAsync(CompletionStage<?> other, Runnable action)
CompletableFuture<Void> runAfterBothAsync(CompletionStage<?> other, Runnable action, Executor executor)
~~~



####聚合 Or 关系
Either...or... 表示两者中的一个，自然也就是 Or 的体现了
~~~
//Either
<U> CompletableFuture<U> applyToEither(CompletionStage<? extends T> other, Function<? super T, U> fn)
<U> CompletableFuture<U> applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T, U> fn)
<U> CompletableFuture<U> applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T, U> fn, Executor executor)

CompletableFuture<Void> acceptEither(CompletionStage<? extends T> other, Consumer<? super T> action)
CompletableFuture<Void> acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action)
CompletableFuture<Void> acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action, Executor executor)

CompletableFuture<Void> runAfterEither(CompletionStage<?> other, Runnable action)
CompletableFuture<Void> runAfterEitherAsync(CompletionStage<?> other, Runnable action)
CompletableFuture<Void> runAfterEitherAsync(CompletionStage<?> other, Runnable action, Executor executor)
~~~


####异常处理
~~~
CompletableFuture<T> exceptionally(Function<Throwable, ? extends T> fn)
CompletableFuture<T> exceptionallyAsync(Function<Throwable, ? extends T> fn)
CompletableFuture<T> exceptionallyAsync(Function<Throwable, ? extends T> fn, Executor executor)
        
CompletableFuture<T> whenComplete(BiConsumer<? super T, ? super Throwable> action)
CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T, ? super Throwable> action)
CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T, ? super Throwable> action, Executor executor)
        
       
<U> CompletableFuture<U> handle(BiFunction<? super T, Throwable, ? extends U> fn)
<U> CompletableFuture<U> handleAsync(BiFunction<? super T, Throwable, ? extends U> fn)
<U> CompletableFuture<U> handleAsync(BiFunction<? super T, Throwable, ? extends U> fn, Executor executor)
~~~
这个异常处理看着还挺吓人的，拿传统的 try/catch/finally 做个对比也就瞬间秒懂了
exceptionally-->try/catch
Complete和handle --> try/finally




###简要



**应用场景**

**描述依赖关系：**

1.  thenApply() 把前面异步任务的结果，交给后面的Function
2.  thenCompose()用来连接两个有依赖关系的任务，结果由第二个任务返回

**描述and聚合关系：**

1.  thenCombine:任务合并，有返回值
2.  thenAccepetBoth:两个任务执行完成后，将结果交给thenAccepetBoth消耗，无返回值。
3.  runAfterBoth:两个任务都执行完成后，执行下一步操作（Runnable）。

**描述or聚合关系：**

1.  applyToEither:两个任务谁执行的快，就使用那一个结果，有返回值。
2.  acceptEither: 两个任务谁执行的快，就消耗那一个结果，无返回值。
3.  runAfterEither: 任意一个任务执行完成，进行下一步操作(Runnable)。

**并行执行：**

CompletableFuture类自己也提供了anyOf()和allOf()用于支持多个CompletableFuture并行执行

总结 CompletableFuture 几个关键点：

1、计算可以由 Future ，Consumer 或者 Runnable 接口中的 apply，accept或者 run 等方法表示。

2、计算的执行主要有以下

a. 默认执行

b. 使用默认的 CompletionStage 的[异步执行](https://www.zhihu.com/search?q=%E5%BC%82%E6%AD%A5%E6%89%A7%E8%A1%8C&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22answer%22%2C%22sourceId%22%3A2295290317%7D)提供者异步执行。这些方法名使用 someActionAsync 这种格式表示。

c. 使用 Executor 提供者异步执行。这些方法同样也是 someActionAsync 这 种格式，但是会增加一个 Executor 参数。

**CompletableFuture的API非常丰富，不用全部掌握，大概了解有哪些功能，使用时会查API就行**
