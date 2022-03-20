---
title: stream其它的.md
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
~~~
         HashMap<String, Integer> stringStringHashMap = new HashMap<>();
        stringStringHashMap.put("张三", 100);
        Student stu1 = new Student(01, 19, "张三",null);
        Student stu2 = new Student(02, 23, "李四",null);
        Student stu3 = new Student(01, 28, "王五",null);
        List<Student> list = new ArrayList<>();
        list.add(stu1);
        list.add(stu2);
        list.add(stu3);

        Student student = list.stream().findFirst().orElse(null);
        Student student1 = list.stream().findAny().orElse(null);
        list.stream().max((o1, o2) -> 0);
        list.stream().sorted((o1, o2) -> 0);
        list.stream().limit(0);
        list.stream().skip(1);
        list.stream().distinct();
        list.stream().min((o1, o2) -> 0);
        list.stream().toArray();
        list.stream().filter();
        list.stream().count();

        list.stream().min((o1, o2) -> 0);


            //总数据
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).average()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).boxed()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).sequential()
     
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).spliterator()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).summaryStatistics()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).isParallel()

            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).toArray()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).asDoubleStream()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).asLongStream()
                    
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).mapToDouble()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).mapToLong()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).mapToObj()
            int sum = orderList.stream().mapToInt(JgWarehouseOrder::getNum).allMatch()



~~~





~~~
    public static void main(String[] args) {
        List<Integer> numList = Arrays.asList(1, 2, 3, 4, 5, 6);
        ArrayList<String> result = numList.stream().reduce(new ArrayList<String>(), (a, b) -> {
            a.add("element-" + Integer.toString(b));
            return a;
        }, (a, b) -> null);
        System.out.println(result);

    }
~~~


skip 0 limit 10 ,  就类似于mysql limit 0,10 
~~~
 final List<Kuaidi100Vo.DataBean> addList = resultList.stream().skip(0).limit(num).collect(Collectors.toList());
~~~



求和
~~~
BigDecimal:
BigDecimal bb =list.stream().map(Plan::getAmount).reduce(BigDecimal.ZERO,BigDecimal::add);
int、double、long:
double max = list.stream().mapToDouble(User::getHeight).sum();
~~~





###分组求和、分组求最值、分组求数量。就类似于sql里的分组
~~~
        String collect = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").map(Object::toString).collect(Collectors.joining(","));
        System.out.println(collect);

        //HashSet
        Set<Object> collect1 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(Collectors.toSet());
        System.out.println(collect1);

        //ArrayList
        List<Object> collect2 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(Collectors.toList());
        System.out.println(collect2);

        //ConcurrentMap
        ConcurrentMap<Integer, Object> collect3 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(Collectors.toConcurrentMap(m -> m.hashCode(), m -> m, (v1, v2) -> v2));
        System.out.println(collect3);

        Double collect4 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(Collectors.averagingInt(new ToIntFunction<Object>() {
            @Override
            public int applyAsInt(Object value) {
                return value.hashCode();
            }
        }));
        System.out.println(collect4);

        /**
         * 分组
         */
        //分成2组，使用 Collectors.partitioningBy效率更高
        Map<Boolean, List<Object>> collect5 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(Collectors.partitioningBy(m -> m instanceof String));
        System.out.println(collect5);

        //分成多组
        Map<? extends Class<?>, List<Object>> collect6 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(groupingBy(Object::getClass));
        System.out.println(collect6);

        //分组，统计组内元素的数量
        Map<? extends Class<?>, Long> collect7 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(groupingBy(Object::getClass, Collectors.counting()));
        System.out.println(collect7);

        //分组，求和组内元素
        Map<? extends Class<?>, Integer> collect8 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(groupingBy(Object::getClass, summingInt(Object::hashCode)));
        System.out.println(collect8);


        //分组，取最值组内元素
        Map<? extends Class<?>, Optional<Object>> collect9 = Stream.of(1, new Object(), "3", "4", "5", "6", "7", "8", "9", "10").collect(groupingBy(Object::getClass, maxBy(Comparator.comparing(Object::hashCode))));
        System.out.println(collect9);


        
        //自定义的聚合操作 reducing
        String s = Stream.of("3", "4", "5", "6", "7", "8", "9", "10")
                .collect(reducing((x, y) -> x+y)).get();
        System.out.println(s);

~~~

###使用流简易构造连续的数组
~~~
        int[] ints = Stream.iterate(1, k -> ++k)
            .limit(100).flatMapToInt(stream -> IntStream.of(stream)).toArray();

        long[] longs = Stream.iterate(1, k -> ++k)
            .limit(100).flatMapToLong(stream -> LongStream.of(stream)).toArray();

        double[] doubles = Stream.iterate(1, k -> ++k)
            .limit(100).flatMapToDouble(stream -> DoubleStream.of(stream)).toArray();

        List<String> collect = Stream.iterate(1, k -> ++k)
            .limit(100).map(m -> String.valueOf(m)).collect(Collectors.toList());
        String[] strings = collect.toArray(new String[0]);

        System.out.println(strings);
~~~
