---
title: Java-hashCode和equals方法与对象比较和去重(一).md
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
> 事实胜于雄辩

###什么时候需要重写hashCode 和 equals 方法呢？
>如果想使用equals比较对象，那么请将equals方法和hashCode方法重写

######情景模式一
`在使用Set进行集合元素去重的时候，请将hashCode 和 equals 方法重写。`

如下代码，不重写hashCode 和 equals 。看看使用set是否能去重成功
~~~
package io.renren;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {
    private Integer id;
    private String name;
    private Integer age;
    public Test(){}
    public Test(Integer id, String name, Integer age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return "Test{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
    public static void main(String[] args) {
        ArrayList<Test> list = new ArrayList<>();
        Collections.addAll(list,
                new Test(1,"yinkai",23),
                new Test(1,"yinkai",23),
                new Test(2,"yinkai",25)
        );
        Set<Test> set = new HashSet<>(list);
        System.out.println(set);
    }
}
~~~
可以看到list里有两个new Test(1,"yinkai",23)，那么使用set去重应该能够干掉一个。运行程序，打印如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-df829b4d0196706e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
还是存在两个相同的对象
那么，我们再使用idea生成下两个方法，代码如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ee1f131d899a096f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
之后的代码如下
~~~
package io.renren;

import java.util.*;

/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {
    private Integer id;
    private String name;
    private Integer age;
    public Test(){}
    public Test(Integer id, String name, Integer age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Test test = (Test) o;
        return Objects.equals(id, test.id) &&
                Objects.equals(name, test.name) &&
                Objects.equals(age, test.age);
    }
    @Override
    public int hashCode() {
        return Objects.hash(id, name, age);
    }
    @Override
    public String toString() {
        return "Test{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
    public static void main(String[] args) {
        ArrayList<Test> list = new ArrayList<>();
        Collections.addAll(list,
                new Test(1,"yinkai",23),
                new Test(1,"yinkai",23),
                new Test(2,"yinkai",25)
        );
        Set<Test> set = new HashSet<>(list);
        System.out.println(set);
    }
}
~~~
再次运行程序如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e0d8bf0f1db2f6f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
问题完美解决 ~

######情景模式二
`使用自定义对象作为作为 Map 的键，请将 hashCode 和 equals方法重写。`

如下代码，若不重写 hashCode 和 equals方法看看会发生什么情况~
~~~
package io.renren;
import java.util.*;
/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {
    private Integer id;
    private String name;
    private Integer age;
    public Test(){}
    public Test(Integer id, String name, Integer age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }
    @Override
    public String toString() {
        return "Test{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
    public static void main(String[] args) {
        HashMap<Test,Object> hashMap = new HashMap<Test,Object>() {{
           put(new Test(1,"yinkai",23),1);
           put(new Test(1,"yinkai",23),1);
           put(new Test(3,"yinkai",25),1);
        }};
        System.out.println(hashMap);
    }
}
~~~
上面的代码两次将new Test(1,"yinkai",23)作为HashMap的key，而我们知道HashMap的key是不会重复的。但是运行下程序：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b7f669b62f24658f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可见这个HashMap的key在这种情况是重复的，其实此时HashMap它自己认为二者key是不相同的，因为HashMap内部判断key是否重复的算法仅仅使用的是对象的引用。而我们程序员希望它根据字段来判断是否重复。

那么，我们使用idea生成一下Test类的hashCode 和 equals 方法，代码如下：
~~~
package io.renren;
import java.util.*;
/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {
    private Integer id;
    private String name;
    private Integer age;
    public Test(){}
    public Test(Integer id, String name, Integer age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }
    @Override
    public String toString() {
        return "Test{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Test test = (Test) o;
        return Objects.equals(id, test.id) &&
                Objects.equals(name, test.name) &&
                Objects.equals(age, test.age);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, age);
    }

    public static void main(String[] args) {
        HashMap<Test,Object> hashMap = new HashMap<Test,Object>() {{
           put(new Test(1,"yinkai",23),1);
           put(new Test(1,"yinkai",23),1);
           put(new Test(3,"yinkai",25),1);
        }};
        System.out.println(hashMap);
    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ccc8bcc0e5592ec3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
ok，现在key总算是不重复了

###为什么使用equals比较对象就要将 hashCode 和 equals 方法一起重写？

我们可以看看Object类的源码。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b641867bd0543563.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


上面例子中的两个new Test(1,"yinkai",23) 对象的引用的确是不同的，但是引用的比较对我们来说根本没有意义，我们需要使用Test中的id,name,age字段一起进行比较！
>Object基类的equals方法的确只是比较对象的引用，但是我们程序员希望根据业务字段来进行比较。

那么可能有人就会问了，既然需要比较业务字段，那重写equals 就行了呀，为什么还要重写hashCode呢？
是的，如果单单只是使用equals来判断俩对象是否相等，我们可以不去重写hashCode，看代码：
~~~
package io.renren;
import java.util.*;
/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {
    private Integer id;
    private String name;
    private Integer age;
    public Test(){}
    public Test(Integer id, String name, Integer age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }
    @Override
    public String toString() {
        return "Test{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Test test = (Test) o;
        return Objects.equals(id, test.id) &&
                Objects.equals(name, test.name) &&
                Objects.equals(age, test.age);
    }

    public static void main(String[] args) {
        System.out.println(new Test(1,"yinkai",23) .equals(new Test(1,"yinkai",23)) );
    }
}
~~~
程序打印 true ，若按字段比较两个对象是相等的

 `但是，我们要在 HashMap、HashTable 的 key 和 HashSet 这种容器中使用时就必须重写hashCode方法了！`

在上面程序中添加一行代码，打印下两个字段相同对象的hashCode数值是否相同
~~~
System.out.println(new Test(1,"yinkai",23).hashCode() == new Test(1,"yinkai",23).hashCode());
~~~
打印了false，可见如果不重写hashCode。那么两个new Test(1,"yinkai",23)对象的hashCode()方法返回值是不同的。

很巧的是，HashMap和HashTable都是使用对象的hashCode()方法和equals 方法一起来进行key键对象重复判断的。我们可以看看HashMap put方法的源码：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-694aa59faf431f98.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这里调用了hash()方法，进去看看这个
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c3ec4ad01745c382.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
不出所料，的确是使用了hashCode。在跟进去putval看看
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2fd176e88eab27c2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
已经很清晰了，hashCode和equals 一起用在了HashMap的key键的重复判断中。

由此可见在 HashMap、HashTable 的 key 和 HashSet中必须将hashCode和equals 一起重写。如果违背这个原则，那么后果就是HashMap、HashTable 的key重复，HashSet无法完成去重任务。
