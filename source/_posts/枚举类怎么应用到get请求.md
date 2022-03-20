---
title: 枚举类怎么应用到get请求.md
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
title: 枚举类怎么应用到get请求.md
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
~~~
	@GetMapping("/getMj")
	public void getMj(Gender gender){
		System.out.println(gender);
	}
~~~

post请求已经可以完全映射过去。但get请求传枚举还只能传枚举名字

http://127.0.0.1:9999/demo/getMj?gender=MALE 可以

http://127.0.0.1:9999/demo/getMj?gender=1 报错
>Caused by: org.springframework.core.convert.ConversionFailedException: Failed to convert from type [java.lang.String] to type [com.softdev.system.demo.Gender] for value '1'; nested exception is java.lang.IllegalArgumentException: No enum constant com.softdev.system.demo.Gender.1




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


###使用Converter解决
编写Converter可以支持这种形式的枚举传参：
http://127.0.0.1:9999/demo/getMj?gender=1

定义BaseEnum 
~~~
package com.softdev.system.demo;


public interface BaseEnum {
    int getValue();
}
~~~


通用Converter
~~~
package com.softdev.system.demo;
import org.springframework.core.convert.converter.Converter;
import org.springframework.core.convert.converter.ConverterFactory;

import java.util.HashMap;
import java.util.Map;
import java.util.WeakHashMap;

public class UniversalEnumConverterFactory implements ConverterFactory<String, BaseEnum> {

    private static final Map<Class, Converter> converterMap = new WeakHashMap<>();

    @Override
    public <T extends BaseEnum> Converter<String, T> getConverter(Class<T> targetType) {
        Converter result = converterMap.get(targetType);
        if(result == null) {
            result = new IntegerStrToEnum<T>(targetType);
            converterMap.put(targetType, result);
        }
        return result;
    }

    class IntegerStrToEnum<T extends BaseEnum> implements Converter<String, T> {
        private final Class<T> enumType;
        private Map<String, T> enumMap = new HashMap<>();

        public IntegerStrToEnum(Class<T> enumType) {
            this.enumType = enumType;
            T[] enums = enumType.getEnumConstants();
            for(T e : enums) {
                enumMap.put(e.getValue() + "", e);
            }
        }


        @Override
        public T convert(String source) {
            T result = enumMap.get(source);
            if(result == null) {
                throw new IllegalArgumentException("No element matches " + source);
            }
            return result;
        }
    }
}

~~~

注册
~~~
package com.softdev.system.demo.config;

import com.softdev.system.demo.UniversalEnumConverterFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.format.FormatterRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

@Configuration
public class MyWebAppConfigurer extends WebMvcConfigurerAdapter {

    @Override
    public void addFormatters(FormatterRegistry registry) {
        registry.addConverterFactory(new UniversalEnumConverterFactory());
    }
}
~~~
