---
title: java8-流的异步迭代.md
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
java 8 提供了parallelStream并行流，我们可以结合forEach方法轻松实现多线程的迭代
~~~
        /**
         * 串行流
         */
        Stream.of("A","B","C", "D").forEach(s->System.out.println("串行流 forEach:"+s));
        Stream.of("A","B","C", "D").forEachOrdered(s->System.out.println("串行流 forEachOrdered:"+s));

        /**
         * 并行流
         */
        Stream.of("A","B","C", "D").parallel().forEach(s->System.out.println("并行流 forEach :"+s));
        Stream.of("A","B","C", "D").parallel().forEachOrdered(s->System.out.println("并行流 forEachOrdered:"+s));

~~~

forEachOrdered () 总是会按照元素给定的顺序执行操作，而 forEach () 方法是不确定的。
 
- 在并行流中， forEach () 方法未必顺序执行，而 forEachOrdered () 永远顺序执行。
- 在顺序流中，两种方法相同。 
- 所以想要动作在每个情况下都有序执行，我们应该使用 forEachOrdered () 方法。
>parallel 遇到 forEach  就不会保证顺序了

###Stream.forEach ()
java文档中forEach 方法声明。

void forEach(Consumer<? super T> action)

1. 执行一个动作, 消费者为每个元素的流。

2. 这是一个终端操作。

3. 这个操作的行为是不确定的。

4. 并行操作这种方法并不能保证顺序。

###Stream.forEachOrdered ()
java文档中forEachOrdered 方法声明。

void forEachOrdered(Consumer<? super T> action)

1. 如果流具有定义的执行顺序，则以此流的执行顺序为此流的每个元素执行操作。

2. 这是一个终端操作。

3. 这种方法保证在顺序和并行流中按顺序执行。




###parallel并行流里是其实是多线程迭代
而且包括主线程在内
~~~
        /**
         * 并行流
         */
        Stream.of("A", "B", "C", "D").parallel().forEach(s -> {
                    System.out.println(Thread.currentThread().getName()+" "+s);
                }
        );
~~~


main C
main D
ForkJoinPool.commonPool-worker-2 B
ForkJoinPool.commonPool-worker-1 A

###缺陷
1、不能使用break和continue这两个关键字

foreach和普通的for循环是不同的，它不是普通的遍历，要想实现continue的效果，可以直接使用return即可；
但是如何实现break的效果呢，然而foreach是无法实现的，只要你使用它，就一定会遍历完的，除非你可以把它放进一个try中，通过抛出异常进行终止它。或者我们实现fillter一下，将不需要遍历的筛选出去。保证流中一定是我们需要遍历的

~~~
        /**
         * 并行流
         */
        Stream.of("A", "B", "C", "D").parallel().forEachOrdered(s -> {
                    if (Objects.equals(s, "A")) {
                        return;
                    }
                    System.out.println(Thread.currentThread().getName() + " " + s);
                }
        );
~~~


2、流的迭代非安全

~~~
        ArrayList<String> strings = new ArrayList<>();
        strings.add("1");
        strings.add("2");
        strings.add("3");
        strings.add("4");
        strings.stream().forEach(e->{
            if(Objects.equals(e,"1")){
                strings.remove("1");
            }
        });

        System.out.println(strings);
~~~
以上程序的执行结果：

测试结果：Lambda 循环中删除数据非安全。Lambda 删除的正确方式：
~~~
        ArrayList<String> strings = new ArrayList<>();
        strings.add("1");
        strings.add("2");
        strings.add("3");
        strings.add("4");
        strings.removeIf(s -> Objects.equals("1", s));
        strings.stream().forEach(s -> {
            System.out.println(s);
        });
~~~
从上面的代码可以看出，可以先使用 Lambda 的 removeIf 删除多余的数据，再进行循环是一种正确操作集合的方式。






写法举例
~~~
        for (Map<String, Object> map : supplierNoOption) {
            String supplierNo = (String) map.get("supplierNo");
            if (StringUtils.equals(supplierNo, mbUndertakesOrderDto.getSupplierNo())) {
                map.put("isSelect", true);
            } else {
                map.put("isSelect", false);
            }
        }
~~~
改为
~~~
supplierNoOption.stream().forEach(map -> 
map.put("isSelect", Objects.equals(map.get("supplierNo"), mbUndertakesOrderDto.getSupplierNo())));
~~~

3、并行流里由于使用多线程。则会造成线程不安全
虽然不会出现异常，但是会丢数据。如下使用ArrayList会丢数据，请用CopyOnWriteArrayList代替之
~~~
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < 99999; i++) {
            list.add(i);
        }
        System.out.println(list.size());

       / List<Integer> objects = new ArrayList<>();
        List<Integer> objects = new CopyOnWriteArrayList<>();
        list.parallelStream().forEach(m -> {
            objects.add(m);
        });
        System.out.println(objects.size());
        if (objects.size() < list.size()) {
            System.out.println("丢数据了..");
        } else {
            System.out.println("没丢");

        }
~~~
