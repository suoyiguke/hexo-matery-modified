---
title: stream()-peek的用法和-与-stream()-map区别.md
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
peek对应Consumer   没返回值，map对应Function  有返回值
   ~~~
Stream.of("one", "two", "three","four").peek(u -> u.toUpperCase())
                .forEach(e -> System.out.print(e+"\t"));

        Stream.of("one", "two", "three","four").map(u -> u.toUpperCase())
                .forEach(e -> System.out.print(e+"\t"));
~~~
>one	two	three	four	ONE	TWO	THREE	FOUR	

可以发现peek不会对流有所改变，而map却是更改了流

再看下面代码
~~~
    List<Integer> list1 = Stream.of("one", "two", "three", "four").map(String::hashCode).collect(Collectors.toList());
   List<String> list2 = Stream.of("one", "two", "three", "four").peek(String::hashCode).collect(Collectors.toList());
~~~
> map对流有修改，生成的List泛型是Integer，而peek还是String


因此，peek适合做一些中间操作。比如打印日志。将值set到其他对象。但是对m参数进行set也是能影响流的结果

~~~

    @Data
    @AllArgsConstructor
    private static class ff {
        private Integer id;
    }

    public static void main(String[] args) throws InterruptedException {

        List<ff> tempList = new ArrayList<>();
        List<ff> list2 = Stream.of( new ff(1),  new ff(2),  new ff(3),  new ff(4)).peek(m -> {
            Integer id = m.getId();
            m.setId(++id);
            tempList.add(m);
        }).collect(Collectors.toList());

        System.out.println(list2);
        System.out.println(tempList);

    }
}
~~~


下面的反例，这样用map是错误的。可以直接使用peek.这样就不用return了！
> .map(indexName -> { LOG.debug("Marking index {} to be reopened using alias.", indexName); return indexName; })

~~~
  public void upgrade() {
        this.indexSetService.findAll()
            .stream()
            .map(mongoIndexSetFactory::create)
            .flatMap(indexSet -> getReopenedIndices(indexSet).stream())
            .map(indexName -> { LOG.debug("Marking index {} to be reopened using alias.", indexName); return indexName; })
            .forEach(indices::markIndexReopened);
    }
~~~

例子2
~~~
    @AllArgsConstructor
    @Data
    private static class Student{
        private Integer id;
        private Integer age;
        private String name;
    }

    public static void main(String[] args) {
        HashMap<String, Integer> stringStringHashMap = new HashMap<>();
        stringStringHashMap.put("张三", 100);
        Student stu1 = new Student(1, 19, "张三");
        Student stu2 = new Student(2, 23, "李四");
        Student stu3 = new Student(3, 28, "王五");
        List<Student> list = new ArrayList<>();
        list.add(stu1);
        list.add(stu2);
        list.add(stu3);
        List<Student> collect = list.stream().filter(student->ToolUtil.isNotEmpty(stringStringHashMap.get(student.getName()))).peek(student -> {
            Integer num = stringStringHashMap.get(student.getName());
            student.setAge(num);
        }).collect(Collectors.toList());
        System.out.println(collect);
    }
~~~


###peek、foreach区别
peek不会中断流，后面可以对流继续操作，foreach会中断流，只能进行遍历
~~~
void forEach(Consumer<? super T> action);
Stream<T> peek(Consumer<? super T> action);
~~~
