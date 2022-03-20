---
title: 反射set、get工具类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 工具类
categories: 工具类
---
---
title: 反射set、get工具类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 工具类
categories: 工具类
---
~~~
package com.gbm.cloud.treasure.util;

import com.google.common.collect.Maps;
import lombok.extern.slf4j.Slf4j;

import java.lang.reflect.Field;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * @author cbw
 * @date 2021/12/6 14:30
 */
@Slf4j
public class ReflectObjectUtil {
    /**
     * 获取单个对象指定键的值
     *
     * @param t
     * @param key
     * @param <T>
     * @return
     */
    public static <T> Object getValueByKey(T t, String key) {
        Object obj = null;
        try {
            Class clazz = t.getClass();
            Field[] fields = clazz.getDeclaredFields();
            Field resultField = Arrays.stream(fields)
                    .filter(field -> field.getName().equals(key))
                    .findFirst()
                    .get();
            resultField.setAccessible(true);
            if (resultField.getGenericType().toString().equals(
                    "class java.util.Date")) {
                //时间需要额外处理
                SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                obj = simpleDateFormat.format(resultField.get(t));
            }else {
                obj = resultField.get(t);
            }
        } catch (IllegalArgumentException e) {
            log.error("出现异常"+e.getClass().toString());
            return null;
        } catch (Exception e) {
            log.error("出现异常"+e.getClass().toString());
            return null;
        }
        return obj;
    }

    /**
     * 获取单个对象指定键的值
     *
     * @param t
     * @param key
     * @param <T>
     * @return
     */
    public static <T> Object setValueByKey(T t, String key, Object value) {
        Object obj = null;
        try {
            Class clazz = t.getClass();
            Field[] fields = clazz.getDeclaredFields();
            Field resultField = Arrays.stream(fields)
                    .filter(field -> field.getName().equals(key))
                    .findFirst()
                    .get();

            resultField.setAccessible(true);

            resultField.set(t, value);
        } catch (IllegalArgumentException e) {
            log.error("出现异常"+e.getClass().toString());
            return null;
        } catch (Exception e) {
            log.error("出现异常"+e.getClass().toString());
            return null;
        }
        return obj;
    }

    /**
     * 获取单个对象的所有键值对
     *
     * @param t
     * @param <T>
     * @return
     */
    public static <T> Map<String, Object> getKeyAndValue(T t) {
        Map<String, Object> map = Maps.newHashMap();
        Class clazz = (Class) t.getClass();
        Field[] fields = clazz.getDeclaredFields();
        map = Arrays.stream(fields).collect(Collectors.toMap(Field::getName, field -> {
            Object resultObj = null;
            field.setAccessible(true);
            try {
                resultObj = field.get(t);
            } catch (IllegalArgumentException e) {
                log.error("出现异常"+e.getClass().toString());
                return null;
            } catch (Exception e) {
                log.error("出现异常"+e.getClass().toString());
                return null;
            }
            return Optional.ofNullable(resultObj).orElse(0);
        }, (k1, k2) -> k2));
        return map;
    }
}

~~~
