---
title: stream()-flatMap用法和stream()-map的区别.md
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
>flatMap在流里面还有流时使用

- flatMap可以扁平化流，把流给压扁
- flatMap的参数只能是流对象
- flatMap相当于把操作流的主题从第一个转为（第二个）第一个对象的属性流
~~~
        HashMap<String, List<String>> map = new HashMap<>();
        List<String> strings1 = new ArrayList<>();
        strings1.add("A");
        strings1.add("B");
        strings1.add("C");


        List<String> strings2 = new ArrayList<>();
        strings2.add("e");
        strings2.add("f");
        strings2.add("g");


        List<String> strings3 = new ArrayList<>();
        strings3.add("b");
        strings3.add("n");
        strings3.add("m");

        map.put("1",strings1);
        map.put("2",strings2);
        map.put("3",strings3);

        List<String> collect = map.values().stream().flatMap(Collection::stream).collect(Collectors.toList());
        System.out.println(collect);

~~~
>[A, B, C, e, f, g, b, n, m]

- map.values()是Collection， flatmap() 参数 传入Collection::stream，
- flatmap 收集 HashMap<String, List<String>>的value中的所有List元素，单独组成一个List



###List<List> 的扁平化
~~~
        List<List<String>> strings = new ArrayList<>();

        List<String> strings1 = new ArrayList<>();
        strings1.add("A");
        strings1.add("B");
        strings1.add("C");
        strings.add(strings1);
        List<String> strings2 = new ArrayList<>();
        strings2.add("e");
        strings2.add("f");
        strings2.add("g");
        strings.add(strings2);


        List<String> strings3 = new ArrayList<>();
        strings3.add("b");
        strings3.add("n");
        strings3.add("m");
        strings.add(strings3);

        List<String> collect = strings.stream().flatMap(List::stream).collect(Collectors.toList());
        System.out.println(collect);

~~~
>[A, B, C, e, f, g, b, n, m]





写到好的例子：
将类集合interfaces、Method 传入。
遍历interfaces，匹配类的getMethods（方法数组）的方法名、参数列表。
匹配到了，取第一个方法数组中的方法，add到methods （List) 中
~~~
    public static void main(String[] args) {


        Class<? extends ImgbUndertakesOrderListener> aClass = ImgbUndertakesOrderListener.class;
        ArrayList<Class> list = new ArrayList<>();
        list.add(aClass);
        Method method = Arrays.stream(aClass.getMethods()).findFirst().orElse(null);

        getMethodAndInterfaceDeclarations(method,list);
    }


    static Collection<Method> getMethodAndInterfaceDeclarations(Method method, Collection<Class> interfaces) {
        final List<Method> methods = new ArrayList<>();
        methods.add(method);

        // we search for matching method by iteration and comparison vs getMethod to avoid repeated NoSuchMethodException
        // being thrown, while interface typically only define a few set of methods to check.
        interfaces.stream()
                .map(Class::getMethods)
                .flatMap(Arrays::stream)
                .filter(m -> m.getName().equals(method.getName()) && Arrays.equals(m.getParameterTypes(), method.getParameterTypes()))
                .findFirst()
                .ifPresent(methods::add);

        return methods;
    }

~~~
