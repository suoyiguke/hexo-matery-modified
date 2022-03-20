---
title: java-jdk1-8新特性之Stream流.md
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

jdk8提供的Stream流能够方便操作集合、数组
java.util.stream包即是Stream流式计算的核心

###Stream流的特点
- Stream自己不会存储元素
- Stream `不会改变源对象`，相反，他们会返回一个持有结果的新Stream 
- Stream 操作总是延迟执行的。这意味着他们会等到需要结果的时候才执行

###基础用法
①、从数据源中获得流 ==> 一个数据源(数组、List)
~~~
arrayList.stream()
~~~
②、中间操作==>处理数据源数据
~~~
 .map(e -> e.get("a"))
~~~
③、终止操作==>执行中间操作链，产生结果
~~~
 .collect(Collectors.toList());
~~~
###获得流
######普通流stream()
~~~
import java.util.Arrays;
import java.util.List;

public class Test {
    public static void main(String[] args) {
        List<String> strings = Arrays.asList("abc", "", "bc", "efg", "abcd", "", "jkl");
        // 获取空字符串的数量
        int count = (int) strings.stream().filter(string -> string.isEmpty()).count();
        System.out.println(count);
    }
}
~~~
######并行流 parallelStream()
parallelStream 是流并行处理程序的代替方法。以下实例我们使用parallelStream 来输出空字符串的数量：
~~~
import java.util.Arrays;
import java.util.List;

public class Test {
    public static void main(String[] args) {
        List<String> strings = Arrays.asList("abc", "", "bc", "efg", "abcd", "", "jkl");
        // 获取空字符串的数量
        int count = (int) strings.parallelStream().filter(string -> string.isEmpty()).count();
        System.out.println(count);
    }
}
~~~

###中间操作
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6d3cbd62a24e4d26.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-af3b89b1daaf040a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-757a575b70c295aa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###### forEach

Stream 提供了新的方法 'forEach' 来迭代流中的每个数据。以下代码片段使用forEach 输出了10个随机数：
~~~
import java.util.Random;

public class Test {

    public static void main(String[] args) {
        Random random = new Random();
        random.ints().limit(10).forEach(System.out::println);
    }
}
~~~

###### map


map 方法用于映射每个元素到对应的结果，以下代码片段使用 map 输出了元素对应的平方数：

~~~
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Test {

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(3, 2, 2, 3, 7, 3, 5);
        // 获取对应的平方数
        List<Integer> squaresList = numbers.stream().map(i -> i * i).collect(Collectors.toList());
        squaresList.forEach(System.out::println);
    }
}
~~~

######filter
filter 方法用于通过设置条件过滤出元素。以下代码片段使用filter 方法过滤出空字符串，然后统计数量：
~~~
import org.apache.commons.lang3.StringUtils;

import java.util.Arrays;
import java.util.List;

public class Test {

    public static void main(String[] args) {
        List<String>strings = Arrays.asList("abc", " ", null,"bc", "efg", "abcd"," ", "jkl");
        // 获取空字符串的数量
        int count = (int) strings.stream().filter(string -> StringUtils.isBlank(string)).count();
        System.out.println(count);

    }
}
~~~


######Limit

limit 方法用于获取指定数量的流。以下代码片段使用 limit 方法打印出 10 条数据：
~~~
import java.util.Random;

public class Test {
    public static void main(String[] args) {
        Random random = new Random();
        random.ints().limit(10).forEach(System.out::println);

    }
}
~~~

######sorted

sorted 方法用于对流进行排序。以下代码片段使用 sorted 方法对输出的 10 个随机数进行排序：
~~~
import java.util.Random;

public class Test {
    public static void main(String[] args) {
        Random random = new Random();
        random.ints().limit(10).sorted().forEach(System.out::println);
    }
}
~~~

###终止操作
######Collectors 转化为集合、聚合元素、字符串

Collectors 类实现了很多归约操作，例如将流转换成集合和聚合元素。Collectors可用于返回列表或字符串：
~~~
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Test {
    public static void main(String[] args) {
        List<String> strings = Arrays.asList("abc", "", "bc", "efg", "abcd", "", "jkl");
        List<String> filtered = strings.stream().filter(string -> !string.isEmpty()).collect(Collectors.toList());
        System.out.println("筛选列表: " + filtered);

        String mergedString = strings.stream().filter(string -> !string.isEmpty()).collect(Collectors.joining(", "));
        System.out.println("合并字符串: " + mergedString);
    }
}
~~~

######summaryStatistics 统计
另外，一些产生统计结果的收集器也非常有用。它们主要用于int、double、long等基本类型上，它们可以用来产生类似如下的统计结果。
~~~
import java.util.Arrays;
import java.util.IntSummaryStatistics;
import java.util.List;
import java.util.stream.Collectors;

public class Test {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(3, 2, 2, 3, 7, 3, 5);
        IntSummaryStatistics stats = numbers.stream().mapToInt((x) -> x).summaryStatistics();
        System.out.println("列表中最大的数 : " + stats.getMax());
        System.out.println("列表中最小的数 : " + stats.getMin());
        System.out.println("所有数之和 : " + stats.getSum());
        System.out.println("平均数 : " + stats.getAverage());
    }
}
~~~

###Stream流使用实战
1、从List<Map>中抽离出map中特定key对应的value所组成的List
~~~
import java.util.*;
import java.util.stream.Collectors;

public class Test {
    public static void main(String[] args) {

        List<Map<String, String>> arrayList = new ArrayList();

        arrayList.add(new HashMap<String,String>(){{
            put("a","hhhhhhhhh");
            put("b","kkkkkkkkk");
        }});
        arrayList.add(new HashMap<String,String>(){{
            put("a","fffffffff");
            put("b","gggggggggg");
        }});


        List<String> list = arrayList.stream()
                .map(e -> e.get("a"))
                .collect(Collectors.toList());

        list.forEach(System.out::println);
    }
}
~~~

2、List<Map> 根据key查找
~~~
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
public class Test {
    public static void main(String[] args) {

        List<Map<String, String>> arrayList = new ArrayList();

        arrayList.add(new HashMap<String,String>(){{
            put("a","hhhhhhhhh");
            put("b","kkkkkkkkk");
        }});
        arrayList.add(new HashMap<String,String>(){{
            put("a","fffffffff");
            put("b","gggggggggg");
        }});

        List<Map<String, String>> list = arrayList.stream().filter(e -> e.keySet().contains("a")).collect(Collectors.toList());
        System.out.println(list);

    }


}
~~~

3、过滤掉List<Java Bean>中符合过滤条件的Java Bean
~~~
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Test {
    private String name;
    private Integer age;
    public static void main(String[] args) {
        ArrayList<Test> list = new ArrayList<>();
        Collections.addAll(list,new Test("yink",24),new Test("yinx",12), new Test("hh",13));
        List<Test> testList = list.stream().filter(test -> !test.getName().equals("hh")&&test.getAge()!=13).collect(Collectors.toList());
        System.out.println(testList);
    }


}
~~~

~~~
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.function.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
class User {
    private Integer id;
    private String userName;
    private int age;
}

/**
 * @create 2019-02-26 22:24
 * <p>
 * 题目：请按照给出数据，找出同时满足
 * 偶数ID且年龄大于24且用户名转为大写且用户名字母倒排序
 * 最后只输出一个用户名字
 */
public class StreamDemo {
    public static void main(String[] args) {
        User u1 = new User(11, "a", 23);
        User u2 = new User(12, "b", 24);
        User u3 = new User(13, "c", 22);
        User u4 = new User(14, "d", 28);
        User u5 = new User(16, "e", 26);

        List<User> list = Arrays.asList(u1, u2, u3, u4, u5);

        list.stream().filter(p -> {
            return p.getId() % 2 == 0;
        }).filter(p -> {
            return p.getAge() > 24;
        }).map(f -> {
            return f.getUserName().toUpperCase();
        }).sorted((o1, o2) -> {
            return o2.compareTo(o1);
        }).limit(1).forEach(System.out::println);

    }
}
~~~

4、List<Java Bean>根据Java Bean的一个属性去重
~~~
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.*;
import java.util.stream.Collectors;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Test {
    private String name;
    private Integer age;
    public static void main(String[] args) {
        ArrayList<Test> list = new ArrayList<>();
        Collections.addAll(list,new Test("yink",24),new Test("yink",12), new Test("hh",13));

        ArrayList<Test> collect = list.stream().collect(
                Collectors.collectingAndThen(Collectors.toCollection(() -> new TreeSet<>(Comparator.comparing(Test::getName))), ArrayList::new)
        );

        System.out.println(collect);
    }
}
~~~

~~~
       /**
         * 按platformOrderNo去重excel集合
         */
        dataList = dataList.stream().collect(Collectors.collectingAndThen(Collectors.toCollection(()
                -> new TreeSet<>(Comparator.comparing(JgOriginalOrder::getPlatformOrderNo))), ArrayList::new));
~~~



5、根据具体属性查找list中的对象

~~~
 TbBox tbBox = boxs.stream().filter(u -> u.getSbNumber().equals("123456")).findAny().get();
~~~

6、List按字段分组
~~~
  Map<String, List<CertInfoPO>> collect = certSet.stream()
                    .collect(Collectors.groupingBy(CertInfoPO::getIdentityNumber));
~~~

7、List<Bean>转 key-vue 形式的Map`列转行`
~~~
       List<SysDictData> face = sysDictDataService.selectDictDataByType("face");
        Map<String, String> collect = face.stream()
            .collect(Collectors.toMap(SysDictData::getDictLabel, SysDictData::getDictValue));
~~~


**收集对象实体本身**
在开发过程中我们也需要有时候对自己的list中的实体按照其中的一个字段进行分组（比如 id ->List），这时候要设置map的value值是实体本身。
~~~
public Map<Long, Account> getIdAccountMap(List<Account> accounts) {
    return accounts.stream().collect(Collectors.toMap(Account::getId, account -> account));
}
~~~
account -> account是一个返回本身的lambda表达式，其实还可以使用Function接口中的一个默认方法 Function.identity()，这个方法返回自身对象，更加简洁

**重复key的情况。**
在list转为map时，作为key的值有可能重复，这时候流的处理会抛出个异常：Java.lang.IllegalStateException:Duplicate key。这时候就要在toMap方法中指定当key冲突时key的选择。(这里是选择第二个key覆盖第一个key)
~~~
public Map<String, Account> getNameAccountMap(List<Account> accounts) {
    return accounts.stream().collect(Collectors.toMap(Account::getUsername, Function.identity(), (key1, key2) -> key2));
}
~~~
**用groupingBy 或者 partitioningBy进行分组**
根据一个字段或者属性分组也可以直接用groupingBy方法，很方便。
~~~
Map<Integer, List<Person>> personGroups = Stream.generate(new PersonSupplier()).
 limit(100).
 collect(Collectors.groupingBy(Person::getAge));
Iterator it = personGroups.entrySet().iterator();
while (it.hasNext()) {
 Map.Entry<Integer, List<Person>> persons = (Map.Entry) it.next();
 System.out.println("Age " + persons.getKey() + " = " + persons.getValue().size());
}
~~~


8、count 统计
~~~
                List<Map> reList = ((StockProductDetailRepository) stockProductDetailService.getBaseMapper()).getSupplierNoByk3Code(k3Code);
                final long count = reList.stream()
                        .map(m -> m.get("firstTag"))
                        .filter(e -> Objects.equals(e, 0))
                        .count();
~~~


9、Map 过滤方法流

~~~
        /**
         * 得到自定义字段
         */
        //jg_order_field_relationship 里的相关模板的数据除开这个枚举的之外就是自定义字段了
        Map<Integer, String> myDefinitionMap = fieldMap.entrySet().stream()
                .filter((e) -> !definitionMap.keySet().contains(e.getValue()))
                .collect(Collectors.toMap(
                        (e) -> e.getKey(),
                        (e) -> e.getValue()
                ));

~~~
