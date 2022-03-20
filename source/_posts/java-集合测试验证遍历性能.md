---
title: java-集合测试验证遍历性能.md
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
###foreach的编译后实现

对比源码和反编译后的代码

####使用foreach遍历List
~~~

  // 源码
   public static void main(String[] args) {
        ArrayList<String> arrayList = new ArrayList();
        Collections.addAll(arrayList, "1", "2", "3", "4", "5");

        for (String s : arrayList) {
            System.out.println(s);
        }
    }

    // 反编译后的代码
    public static void main(String[] args) {
        ArrayList<String> arrayList = new ArrayList();
        Collections.addAll(arrayList, new String[]{"1", "2", "3", "4", "5"});
        Iterator var2 = arrayList.iterator();

        while(var2.hasNext()) {
            String s = (String)var2.next();
            System.out.println(s);
        }

    }
~~~
结论：对于遍历List，foreach底层还是调用的Iterator

###使用foreach遍历数组
~~~
    //源码
    public static void main(String[] args) {
        String[] arr = {"1", "2", "3", "4", "5"};

        for (String s : arr) {
            System.out.println(s);
        }
    }
  //反编译后
 public static void main(String[] args) {
        String[] arr = new String[]{"1", "2", "3", "4", "5"};
        String[] var2 = arr;
        int var3 = arr.length;

        for(int var4 = 0; var4 < var3; ++var4) {
            String s = var2[var4];
            System.out.println(s);
        }

    }
~~~
结论：foreach遍历数组最后使用的是for循环

###RandomAccess接口的原理

可以看看jdk源码的注释文档
~~~
/**
 * Marker interface used by <tt>List</tt> implementations to indicate that
 * they support fast (generally constant time) random access.  The primary
 * purpose of this interface is to allow generic algorithms to alter their
 * behavior to provide good performance when applied to either random or
 * sequential access lists.
 *
 * <p>The best algorithms for manipulating random access lists (such as
 * <tt>ArrayList</tt>) can produce quadratic behavior when applied to
 * sequential access lists (such as <tt>LinkedList</tt>).  Generic list
 * algorithms are encouraged to check whether the given list is an
 * <tt>instanceof</tt> this interface before applying an algorithm that would
 * provide poor performance if it were applied to a sequential access list,
 * and to alter their behavior if necessary to guarantee acceptable
 * performance.
 *
 * <p>It is recognized that the distinction between random and sequential
 * access is often fuzzy.  For example, some <tt>List</tt> implementations
 * provide asymptotically linear access times if they get huge, but constant
 * access times in practice.  Such a <tt>List</tt> implementation
 * should generally implement this interface.  As a rule of thumb, a
 * <tt>List</tt> implementation should implement this interface if,
 * for typical instances of the class, this loop:
 * <pre>
 *     for (int i=0, n=list.size(); i &lt; n; i++)
 *         list.get(i);
 * </pre>
 * runs faster than this loop:
 * <pre>
 *     for (Iterator i=list.iterator(); i.hasNext(); )
 *         i.next();
 * </pre>
 *
 * <p>This interface is a member of the
 * <a href="{@docRoot}/../technotes/guides/collections/index.html">
 * Java Collections Framework</a>.
 *
 * @since 1.4
 */
~~~

- RandomAccess 是一个标志接口，表明实现这个这个接口的 List 集合是支持快速随机访问的。也就是说，`实现了这个接口的集合是支持 快速随机访问 策略的。`

- 如果是实现了这个接口的 List，那么使用for循环的方式获取数据会优于用迭代器获取数据。

- 实现RandomAccess接口的集合类
java.util.ArrayList、java.util.Vector、java.util.Stack（以为继承自Vector）、java.util.Arrays.ArrayList、java.util.concurrent.CopyOnWriteArrayList、java.util.RandomAccessSubList、java.util.Collections.SingletonList、java.util.Collections.CopiesList、java.util.ArrayList.SubList
- 没有实现RandomAccess接口的集合类
java.util.LinkedList
