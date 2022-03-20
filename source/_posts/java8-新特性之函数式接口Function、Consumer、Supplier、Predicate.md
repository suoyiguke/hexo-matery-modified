---
title: java8-新特性之函数式接口Function、Consumer、Supplier、Predicate.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
java8引入了四大函数式接口：Function、Consumer、Supplier、Predicate；这几个接口在Optional类中有大量应用，之前我们刚好学习了Optional的用法 https://www.jianshu.com/p/3b23034416f9。这次在这里可以举一反三了。

###还有一个Runnabel
既没有出参也没有入参
###Function<T, R> 
Function<T, R> T：入参类型，R：出参类型
~~~
    public static void main(String[] args) {
        // 定义Function
        Function<Integer, Integer> func = p -> p * 10;
        //调用
        Integer apply = func.apply(11);
        System.out.println(apply);
    }
~~~

Optional类中有:Optional.map()、Optional.flatMap()
~~~
    public<U> Optional<U> map(Function<? super T, ? extends U> mapper) {
        Objects.requireNonNull(mapper);
        if (!isPresent())
            return empty();
        else {
            return Optional.ofNullable(mapper.apply(value));
        }
    }
~~~

###Consumer<T>
>因为没有出参，常用于打印、发送短信等消费动作

Consumer<T>  T：入参类型；没有出参
~~~
  public static void main(String[] args) {
        // 定义Consumer
        Consumer<String> consumer= p -> System.out.println(p);
        //调用
        consumer.accept("18800008888");
    }
~~~
Optional类中有: Optional.Consumer()
~~~
    public void ifPresent(Consumer<? super T> consumer) {
        if (value != null)
            consumer.accept(value);
    }
~~~
##Supplier<T>

>常用于业务“有条件运行”时，符合条件再调用获取结果的应用场景；运行结果须提前定义，但不运行。

Supplier<T> T：出参类型；没有入参
~~~
    public static void main(String[] args) {
       //定义
        Supplier<Integer> supplier= () -> 100;
        //调用
        Integer integer = supplier.get();
        System.out.println(integer);
    }
~~~

Optional类中有:Optional.orElseGet() 和 Optional.orElseThrow()
~~~
    public T orElseGet(Supplier<? extends T> other) {
        return value != null ? value : other.get();
    }
    public <X extends Throwable> T orElseThrow(Supplier<? extends X> exceptionSupplier) throws X {
        if (value != null) {
            return value;
        } else {
            throw exceptionSupplier.get();
        }
    }
~~~
orElseGet、orElseThrow 中表达式运行的条件是：如果前面用了map(m->m.get(xx))，那么就是m.get(xx)为空时；如果前面用的filter(xxx) 那么就是xxx表达式返回false时。


###Predicate<T>

Predicate<T> T：入参类型；出参类型是Boolean
~~~
    public static void main(String[] args) {
        //定义Predicate
        Predicate<Integer> predicate = p -> p % 2 == 0;
        //调用
        predicate.test(100);
    }

~~~

Optional类中有:Optional.filter()
~~~
    public Optional<T> filter(Predicate<? super T> predicate) {
        Objects.requireNonNull(predicate);
        if (!isPresent())
            return this;
        else
            return predicate.test(value) ? this : empty();
    }
~~~
