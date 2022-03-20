---
title: 枚举类虽然可以直接在post请求中使用，但是存在一个问题.md
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
title: 枚举类虽然可以直接在post请求中使用，但是存在一个问题.md
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
body
~~~
{
    "gender": 1
}
~~~


枚举类
~~~
package com.softdev.system.demo;


import java.util.HashMap;
import java.util.Map;

public enum Gender   implements BaseEnum {
    MALE(1), FEMALE(2);

    private int value;
    private static Map<Integer, Gender> valueMap = new HashMap<>();

    static {
        for(Gender gender : Gender.values()) {
            valueMap.put(gender.value, gender);
        }
    }

    Gender(int value) {
        this.value = value;
    }

    public static Gender getByValue(int value) {
        Gender result = valueMap.get(value);
        if(result == null) {
            throw new IllegalArgumentException("No element matches " + value);
        }
        return result;
    }

    @Override
    public int getValue() {
        return value;
    }
}
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-54f9ab8777eb808f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
而且传字符串形式就对应不上
~~~
{
    "gender": "1"
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b93b0a3a93cc4779.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


传1，却映射到了value=2的枚举对象。因为定义的Gender 是从1开始而不是从0开始。
其实框架自定义是对应枚举的 ordinal 属性。
所以，我们定义枚举时一定要从0开始递增。中间也不能间断，否则业务就错乱了。




###有办法解决这个问题吗？当然有呀


1、定义JsonDeserializer
~~~
package com.softdev.system.demo;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonStreamContext;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class IdCodeToEnumDeserializer extends JsonDeserializer<BaseEnum> {
    @SneakyThrows
    @Override
    public BaseEnum deserialize(JsonParser jsonParser, DeserializationContext deserializationContext)
        throws IOException {
        final String param = jsonParser.getText();// 1
        final JsonStreamContext parsingContext = jsonParser.getParsingContext();// 2
        final String currentName = parsingContext.getCurrentName();// 3
        final Object currentValue = parsingContext.getCurrentValue();// 4
        try {
            final Field declaredField = currentValue.getClass().getDeclaredField(currentName);// 5
            final Class<?> targetType = declaredField.getType();// 6
            final Method createMethod = targetType.getDeclaredMethod("create", Object.class);// 7
            return (BaseEnum) createMethod.invoke(null, param);// 8
        } catch (NoSuchMethodException | InvocationTargetException | IllegalAccessException | NoSuchFieldException e) {

            throw e;
        }
    }
}

~~~

2、给枚举类增加create方法
~~~
package com.softdev.system.demo;


import cn.hutool.core.date.Season;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public enum Gender implements BaseEnum {
    MALE(1), FEMALE(2);

    private int value;
    private static Map<Integer, Gender> valueMap = new HashMap<>();

    static {
        for (Gender gender : Gender.values()) {
            valueMap.put(gender.value, gender);
        }
    }

    Gender(int value) {
        this.value = value;
    }

    public static Gender getByValue(int value) {
        Gender result = valueMap.get(value);
        if (result == null) {
            throw new IllegalArgumentException("No element matches " + value);
        }
        return result;
    }

    @Override
    public int getValue() {
        return value;
    }


    public static Gender create(Object code) {
        for (Gender item : values()) {
            if (Objects.equals(code, item.name())) {
                return item;
            }
            int value = item.getValue();
            if (Objects.equals(code,String.valueOf(value))) {
                return item;
            }
        }
        return null;
    }



    public static Gender valueOf(int ordinal) {
        if (ordinal < 0 || ordinal >= values().length) {
            throw new IndexOutOfBoundsException("Invalid ordinal");
        }
        return values()[ordinal];
    }

    public static void main(String[] args) {
        Gender gender = valueOf(0);
        System.out.println(gender);
    }

}
~~~


3、使用枚举类作为成员属性的地方加上@JsonDeserialize注解，并且指定Deserializer
~~~
package com.softdev.system.demo;


import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import lombok.Data;

@Data
public class User {

    @com.fasterxml.jackson.databind.annotation.JsonDeserialize(using = IdCodeToEnumDeserializer.class)
    private Gender gender;
}

~~~

>注意：工程中不能使用Fastjson的HttpMessageConverters，如果有则不生效。请先注释掉


请求测试
~~~
{
    "gender": 1
}
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ec029ec5d353ff68.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这回对了





4、我们可以继续完善下create方法，让枚举类里的各种属性都能匹配到！
~~~

    public static Gender create(Object code) {
        for (Gender item : values()) {
            if (Objects.equals(code, item.name())) {
                return item;
            }
            int value = item.getValue();
            if (Objects.equals(code,String.valueOf(value))) {
                return item;
            }
        }
        return null;
    }


~~~
