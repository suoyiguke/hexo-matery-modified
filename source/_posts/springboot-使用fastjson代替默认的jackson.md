---
title: springboot-使用fastjson代替默认的jackson.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: springboot-使用fastjson代替默认的jackson.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
fastjson是国产的json解析工具，毫无疑问应该支持
文档地址  https://www.w3cschool.cn/fastjson/
github https://github.com/alibaba/fastjson

###springboot 集成fastjson
添加fastjson的依赖
~~~
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.62</version>
        </dependency>
~~~
在spring-boot-starter-web模块中排除掉默认的jackson依赖
~~~
     <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-json</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
~~~


添加一个类，继承WebMvcConfigurer 接口，重写configureMessageConverters()方法
~~~
package com.springboot.study.demo1.config;

import com.alibaba.fastjson.serializer.SerializerFeature;
import com.alibaba.fastjson.support.config.FastJsonConfig;
import com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.ArrayList;
import java.util.List;

@Configuration
public class ImageWebAppConfig implements WebMvcConfigurer {


    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        //创建fastJson消息转换器
        FastJsonHttpMessageConverter fastConverter = new FastJsonHttpMessageConverter();
        List<MediaType> supportedMediaTypes = new ArrayList<>();
        supportedMediaTypes.add(MediaType.APPLICATION_JSON);
        supportedMediaTypes.add(MediaType.APPLICATION_JSON_UTF8);
        supportedMediaTypes.add(MediaType.APPLICATION_ATOM_XML);
        supportedMediaTypes.add(MediaType.APPLICATION_FORM_URLENCODED);
        supportedMediaTypes.add(MediaType.APPLICATION_OCTET_STREAM);
        supportedMediaTypes.add(MediaType.APPLICATION_PDF);
        supportedMediaTypes.add(MediaType.APPLICATION_RSS_XML);
        supportedMediaTypes.add(MediaType.APPLICATION_XHTML_XML);
        supportedMediaTypes.add(MediaType.APPLICATION_XML);
        supportedMediaTypes.add(MediaType.IMAGE_GIF);
        supportedMediaTypes.add(MediaType.IMAGE_JPEG);
        supportedMediaTypes.add(MediaType.IMAGE_PNG);
        supportedMediaTypes.add(MediaType.TEXT_EVENT_STREAM);
        supportedMediaTypes.add(MediaType.TEXT_HTML);
        supportedMediaTypes.add(MediaType.TEXT_MARKDOWN);
        supportedMediaTypes.add(MediaType.TEXT_PLAIN);
        supportedMediaTypes.add(MediaType.TEXT_XML);
        fastConverter.setSupportedMediaTypes(supportedMediaTypes);

        //创建配置类
        FastJsonConfig fastJsonConfig = new FastJsonConfig();
        //修改配置返回内容的过滤
        //WriteNullListAsEmpty  ：List字段如果为null,输出为[],而非null
        //WriteNullStringAsEmpty ： 字符类型字段如果为null,输出为"",而非null
        //DisableCircularReferenceDetect ：消除对同一对象循环引用的问题，默认为false（如果不配置有可能会进入死循环）
        //WriteNullBooleanAsFalse：Boolean字段如果为null,输出为false,而非null
        //WriteMapNullValue：是否输出值为null的字段,默认为false
        fastJsonConfig.setSerializerFeatures(
                SerializerFeature.DisableCircularReferenceDetect,
                SerializerFeature.WriteMapNullValue,
                SerializerFeature.WriteNullListAsEmpty,
                SerializerFeature.WriteNullStringAsEmpty,
                SerializerFeature.WriteNullBooleanAsFalse

        );
        fastConverter.setFastJsonConfig(fastJsonConfig);
        //将fastjson添加到视图消息转换器列表内
        converters.add(fastConverter);
    }
}
~~~

###fastjson的基本使用

######List<Map> 和 json字符串的互相转换
~~~
package com.springboot.study.demo1;
import com.alibaba.fastjson.JSON;
import java.util.*;

public class TestFastJson {


    public static void main(String[] args) {

        List<Map> list = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            list.add(new HashMap<Integer, String>() {{
                for (int i = 1; i <= 5; i++) {
                    put(1, UUID.randomUUID().toString().substring(0, 5));
                }

            }});
        }
        System.out.println(list);

        //将list<map> 转为 json字符串
        String s = JSON.toJSONString(list);
        System.out.println(s);

        //将json字符串 转为 list<map> 
        List<Map> toListmap = JSON.parseArray(s, Map.class);
        System.out.println(toListmap);

    }
}
~~~
> JSON.toJSONString()  和 JSON.parseArray() 俩个方法经常使用在`[{},{},{}...,{}] `形式的json序列化和反序列化中

######List<javabean> 和 json 字符串的互转
用法和上面的区别不大，只是JSON.parseArray() 方法的第二个参数变成相应的javabean.class即可

~~~
package com.springboot.study.demo1;

import com.alibaba.fastjson.JSON;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.*;

@NoArgsConstructor
@AllArgsConstructor
@ToString
@Data
class Person {
    private String id;
    private String name;
    private int age;

    public static void main(String[] args) {
        System.out.println("List<javabean>转化示例开始----------");

        Person person1 = new Person("1", "fastjson1", 1);
        Person person2 = new Person("2", "fastjson2", 2);
        List<Person> persons = new ArrayList<Person>();
        persons.add(person1);
        persons.add(person2);
        String jsonString = JSON.toJSONString(persons);
        System.out.println("json字符串:" + jsonString);

        //解析json字符串
        List<Person> persons2 = JSON.parseArray(jsonString, Person.class);
        //输出解析后的person对象，也可以通过调试模式查看persons2的结构
        System.out.println("person1对象：" + persons2.get(0).toString());
        System.out.println("person2对象：" + persons2.get(1).toString());

        System.out.println("List<javabean>转化示例结束----------");
    }

}

~~~

######javabean和json字符互转
~~~
package com.springboot.study.demo1;

import com.alibaba.fastjson.JSON;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@NoArgsConstructor
@AllArgsConstructor
@ToString
@Data
class Person {
    private String id;
    private String name;
    private int age;

    public static void main(String[] args) {
        System.out.println("javabean转化示例开始----------");
        Person person = new Person("1", "fastjson", 1);

        //这里将javabean转化成json字符串
        String jsonString = JSON.toJSONString(person);
        System.out.println(jsonString);
        //这里将json字符串转化成javabean对象,
        person = JSON.parseObject(jsonString, Person.class);
        System.out.println(person.toString());

        System.out.println("javabean转化示例结束----------");
    }
}
~~~
> 这里使用 JSON.parseObject() 方法单独作用于一个javabean
