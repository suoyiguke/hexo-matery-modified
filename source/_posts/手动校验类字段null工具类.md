---
title: 手动校验类字段null工具类.md
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
title: 手动校验类字段null工具类.md
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
IsNullUtil 

~~~
package com.gbm.cloud.common.util;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang.StringUtils;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.FatalBeanException;

import java.beans.PropertyDescriptor;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.List;

/**
 * @author linmuyu
 * @time 2021/3/24 16:51
 * @Description:
 */
@Slf4j
public class IsNullUtil {
    //整个类都校验
    public static String validateProperty(Object validateObj) {
        return validateProperty(validateObj,(String[])null);
    }
    //类中的某些字段不校验
    public static String validateProperty(Object validateObj,String... ignoreProperties) {
        PropertyDescriptor[] targetPds = BeanUtils.getPropertyDescriptors(validateObj.getClass());
        List<String> ignoreList = (ignoreProperties != null ? Arrays.asList(ignoreProperties) : null);
        for (PropertyDescriptor targetPd : targetPds) {
            Method readMethod = targetPd.getReadMethod();
            if (readMethod != null && (ignoreList == null || !ignoreList.contains(targetPd.getName()))) {
                try {
                    if (!Modifier.isPublic(readMethod.getDeclaringClass().getModifiers())) {
                        readMethod.setAccessible(true);
                    }
                    Object value = readMethod.invoke(validateObj);
                    if (value instanceof String) {
                        if (StringUtils.isEmpty((String) value)) {
                            log.error("存在"+targetPd.getName()+"不合法");
                            return targetPd.getName();
                        }
                    }
                    if (value instanceof Float || value instanceof Integer) {
                        if (StringUtils.isEmpty(value.toString())) {
                            log.error("存在"+targetPd.getName()+"不合法");
                            return targetPd.getName();
                        }
                    }
                    if (value == null) {
                        log.error("存在"+targetPd.getName()+"不合法");
                        return targetPd.getName();
                    }
                } catch (Throwable ex) {
                    throw new FatalBeanException(
                            "Could not copy property '" + targetPd.getName() + "' from source to target", ex);
                }
            }
        }
        return null;
    }




    /**
     * @Des 类中的指定字段需要校验
     * @Author yinkai
     * @Date 2021/11/30 16:16
     */
    public static String validatePropertyNeed(Object validateObj,String... properties) {
        PropertyDescriptor[] targetPds = BeanUtils.getPropertyDescriptors(validateObj.getClass());
        List<String> propertiesList = (properties != null ? Arrays.asList(properties) : null);
        for (PropertyDescriptor targetPd : targetPds) {
            Method readMethod = targetPd.getReadMethod();
            if (readMethod != null && (propertiesList == null || propertiesList.contains(targetPd.getName()))) {
                try {
                    if (!Modifier.isPublic(readMethod.getDeclaringClass().getModifiers())) {
                        readMethod.setAccessible(true);
                    }
                    Object value = readMethod.invoke(validateObj);
                    if (value instanceof String) {
                        if (StringUtils.isEmpty((String) value)) {
                            log.error("存在"+targetPd.getName()+"不合法");
                            return targetPd.getName();
                        }
                    }
                    if (value instanceof Float || value instanceof Integer) {
                        if (StringUtils.isEmpty(value.toString())) {
                            log.error("存在"+targetPd.getName()+"不合法");
                            return targetPd.getName();
                        }
                    }
                    if (value == null) {
                        log.error("存在"+targetPd.getName()+"不合法");
                        return targetPd.getName();
                    }
                } catch (Throwable ex) {
                    throw new FatalBeanException(
                            "Could not copy property '" + targetPd.getName() + "' from source to target", ex);
                }
            }
        }
        return null;
    }
}

~~~
