---
title: java-深拷贝和浅拷贝.md
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
浅拷贝： **不额外创建子对象，**只是把子对象的引用拷贝过去
深拷贝： 创建新的子对象并拷贝属性

如果把java bean划分为 DTO、DO、VO 的话就避免不了对象的copy了。一般选择的spring的工具类都是浅拷贝。当`对象内部还有对象` 时只能copy内部对象的引用，这样的话不利于灵活修改。

浅拷贝模式，分两步：
*   先创建一个新的同类型对象
*   把原对象的各个属性值拷贝到对应字段

spring 的BeanUtils.copyProperties(sourceBean, destBean)只针对Person对象，所以只会把左边Person对象的属性值拷贝到右边，至于子对象department，也只是拷贝了引用。具体看下面的BeanUtils.copyProperties例子。
~~~
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.BeanUtils;

public class MyBeanUtilsTest {

    private static List<Person> list;

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class Person implements Serializable {
        private String name;
        private Integer age;
        private Department department;
    }

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class Department implements Serializable{
        private String name;
    }

    static {
        list = new ArrayList<>();
        list.add(new Person("小明", 18, new Department("行政部")));
    }

    public static void main(String[] args) {
        Person bean = list.get(0);
        Person copyBean = new Person();
        BeanUtils.copyProperties(bean, copyBean);
        System.out.println(bean == copyBean);

        System.out.println("==== copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());

        bean.setName("小亮");
        bean.getDepartment().setName("研发部");

        System.out.println("==== sourceBean修改后，copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());
    }
}
~~~
>false
==== copyBean的属性 ====
小明
行政部
==== sourceBean修改后，copyBean的属性 ====
小明
研发部

修改bean的department 同时也把copyBean 的department 修改了。
使用Spring提供的BeanUtils进行数据拷贝，但它有两个问题：
-  没有提供额外的映射关系，所以两个实体类字段名必须完全一致
- 不支持深拷贝



###深拷贝如何实现

1、ObjectOutputStream.writeObject()

~~~
    public static <T> T deepCopyObj(T object) throws IOException, ClassNotFoundException {
        ByteArrayOutputStream byteOut = new ByteArrayOutputStream();
        ObjectOutputStream out = new ObjectOutputStream(byteOut);
        out.writeObject(object);
        ByteArrayInputStream byteIn = new ByteArrayInputStream(byteOut.toByteArray());
        ObjectInputStream in = new ObjectInputStream(byteIn);
        T dest = (T) in.readObject();
        return dest;
    }

~~~

这次修改为调用深拷贝实现：
~~~

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Person bean = list.get(0);
        Person copyBean = MyBeanUtils.deepCopyObj(bean);
        System.out.println(bean == copyBean);

        System.out.println("==== copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());

        bean.setName("小亮");
        bean.getDepartment().setName("研发部");

        System.out.println("==== sourceBean修改后，copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());
    }
~~~
>false
==== copyBean的属性 ====
小明
行政部
==== sourceBean修改后，copyBean的属性 ====
小明
行政部

修改bean的department  也没有影响到copyBean 的department，达到了深拷贝的目的！


2、JSON序列化、反序列化也是可以的。使用ObjectMapper

先引入jackson
~~~
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-core</artifactId>
      <version>2.9.6</version>
    </dependency>

    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.9.6</version>
    </dependency>

    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.9.6</version>
    </dependency>
  </dependencies>
~~~

使用
~~~
    public static void main(String[] args) throws IOException {
        Person bean = list.get(0);
        ObjectMapper objectMapper = new ObjectMapper();
        String copyBeanStr = objectMapper.writeValueAsString(bean);
        Person copyBean = objectMapper.readValue(copyBeanStr, new TypeReference<Person>() {});
        System.out.println(bean == copyBean);

        System.out.println("==== copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());

        bean.setName("小亮");
        bean.getDepartment().setName("研发部");

        System.out.println("==== sourceBean修改后，copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());
    }
~~~

>false
==== copyBean的属性 ====
小明
行政部
==== sourceBean修改后，copyBean的属性 ====
小明
行政部

3、使用二方库 MapStruct

~~~
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Mappings;
import org.mapstruct.factory.Mappers;
@Mapper
public interface PersonConverter {
    PersonConverter INSTANCE = Mappers.getMapper(PersonConverter.class);
    @Mappings({
        @Mapping(source = "name", target = "name"),
        @Mapping(source = "age", target = "age"),
        @Mapping(source = "department.name", target = "department.name"),
    })
    Person domain2dto(Person person);

    List<Person> domain2dto(List<Person> people);

}
~~~


~~~
    public static void main(String[] args) throws IOException {
        Person bean = list.get(0);
        Person copyBean = PersonConverter.INSTANCE.domain2dto(bean);
        System.out.println(bean == copyBean);
        System.out.println("==== copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());
        bean.setName("小亮");
        bean.getDepartment().setName("研发部");
        System.out.println("==== sourceBean修改后，copyBean的属性 ====");
        System.out.println(copyBean.getName());
        System.out.println(copyBean.getDepartment().getName());
    }
}
~~~
>false
==== copyBean的属性 ====
小明
行政部
==== sourceBean修改后，copyBean的属性 ====
小明
行政部
