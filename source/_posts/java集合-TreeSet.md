---
title: java集合-TreeSet.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java源码分析
categories: java源码分析
---
---
title: java集合-TreeSet.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java源码分析
categories: java源码分析
---
###**1、基本属性**
- 数据结构- 红黑树
- 支持自定义排序
- 元素不能为null
- 使用TreeMap实现

###**2、TreeSet与hashSet的区别**
- TreeSet背后的结构是TreeMap,也就是红黑树，能够实现自动排序。通过equals和compareTo方法进行内容的比较。
- HashSet背后是HashMap,key是无序的，只能做外部排序。既然是Hash,那么就要重写其对象的hashCode和equals方法。

- HashSet可以接受null值，有且只有一个
- TreeSet默认不可以接受null值，会直接抛出空指针异常
- set里没有重复数据，TreeSet里连虚无都没有


~~~

    public static void main(String[] args) {
        System.out.println("=======TreeSet可以自定义排列属性，要求元素实现Comparator接口的compare方法=======");
        Set<Integer> treeSet = new TreeSet<>(new Comparator(){
            @Override
            public int compare(Object o1, Object o2) {
                return (Integer) o2-(Integer) o1;
            }
        });
        treeSet.add(11);
        treeSet.add(1);
        treeSet.add(2);
        treeSet.add(3);
        treeSet.add(4);
        for (Integer integer : treeSet) {
            System.out.println(integer);
        }

        System.out.println("========HashSet是无序的，只是像数字序列、字母序列这样的hashcode刚好是有顺序罢了========");
        Set<Integer> hashSet = new HashSet<>();
        hashSet.add(11);
        hashSet.add(1);
        hashSet.add(2);
        hashSet.add(3);
        hashSet.add(4);
        for (Integer integer : hashSet) {
            System.out.println(integer);
        }


        System.out.println("========linkedHashSet能保证元素按添加顺序排列========");
        Set<Integer> linkedHashSet = new LinkedHashSet<>();
        linkedHashSet.add(11);
        linkedHashSet.add(1);
        linkedHashSet.add(2);
        linkedHashSet.add(3);
        linkedHashSet.add(4);
        for (Integer integer : linkedHashSet) {
            System.out.println(integer);
        }

    }
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-76e7328c8eec5361.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###**3、怎么理解HashSet的无序？**
要理解这个问题应该考虑到Set是个接口。接口的契约很单纯，不会做过多的保证。Set的契约重点就是“元素不重复的集合”，而对顺序不做保证（也就是不做限制，有序无序都可以）。实现该接口的类既可以提供有序的实现，也可以提供无序的实现。 
**HashSet在保存数据的时候显然还是得按一定顺序放入其背后的数组中，但顺序不是用户可控制的，对用户来说就是“无序”。** 

与之相对，SortedSet接口的契约就包含了“元素不重复，且按照用户指定的方式排序的集合”的意义。SortedSet接口满足Set接口的契约，并额外添加的“有序”的契约。TreeSet就是实现了SortedSet（以及Set）接口的实现，它就是有序的。

**4、hashSet内部顺序实现**
JDK8版java.util.HashMap内的hash算法混淆程度低；在[0, 2^32-1]范围内经过HashMap.hash()之后还是得到自己。我的例子正好落入这个范围内。
