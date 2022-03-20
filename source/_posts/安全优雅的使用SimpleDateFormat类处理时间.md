---
title: 安全优雅的使用SimpleDateFormat类处理时间.md
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
SimpleDateFormat是线程不安全的！所以不能因为想要公用一个实例而选择使用单例。

我们可以配合使用ThreadLocal来达到这个效果。
~~~
package org.szwj.ca.identityauthsrv.util.common;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 日期工具类
 *
 * @author yang.Liu
 * @see java.util.Map
 * @see java.text.DateFormat
 * @see java.lang.ThreadLocal
 * @see java.text.SimpleDateFormat
 */
public class DateUtils {

    private static final Logger log = LoggerFactory.getLogger(DateUtils.class);

    private DateUtils() {
    }

    /**
     * Date转为字符串日期
     *
     * @param date       日期
     * @param dateFormat 日期格式
     */
    public static String format(Date date, DateFormatEnum dateFormat) {
        return getDateFormat(dateFormat).format(date);
    }

    /**
     * Date转为默认字符串日期
     *
     * @param date 日期
     */
    public static String format(Date date) {
        return format(date, DateFormatEnum.DEFAULT_FORMAT);
    }

    /**
     * 字符串日期转为Date
     *
     * @param strDate 字符串日期
     */
    public static Date parse(String strDate) {
        return parse(strDate, DateFormatEnum.DEFAULT_FORMAT);
    }

    /**
     * 字符串日期转为Date
     *
     * @param strDate    字符串日期
     * @param dateFormat 日期格式
     */
    public static Date parse(String strDate, DateFormatEnum dateFormat) {
        try {
            return getDateFormat(dateFormat).parse(strDate);
        } catch (ParseException e) {
            log.error("字符串日期转为Date异常", e);
            return null;
        }
    }

    /**
     * Thread线程变量 + Map | 缓存 日期格式(K)，SimpleDateFormat(V)，提高效率
     *
     * @param dateFormat {@link DateFormatEnum} {@link #TL()}
     */
    private static DateFormat getDateFormat(DateFormatEnum dateFormat) {
        ThreadLocal<Map<DateFormatEnum, DateFormat>> TL = TL();
        Map<DateFormatEnum, DateFormat> map = TL.get();
        if (Objects.isNull(map)) {
            map = new HashMap<>();
            TL.set(map);
        }
        if (Objects.isNull(dateFormat)) {
            dateFormat = DateFormatEnum.DEFAULT_FORMAT;
        }
        DateFormat ret = map.get(dateFormat);
        if (Objects.isNull(ret)) {
            ret = new SimpleDateFormat(dateFormat.dateFormat);
            map.put(dateFormat, ret);
        }
        return ret;
    }

    /**
     * 时间格式化枚举，由于可读性，枚举对象声明未遵循常量大写规范～
     */
    public enum DateFormatEnum {
        DEFAULT_FORMAT("yyyy-MM-dd HH:mm:ss"),
        yyyy_MM_dd("yyyy-MM-dd"),
        yyyy("yyyy"),
        MM("MM"),
        dd("dd"),
        HH_mm_ss("HH:mm:ss"),
        HH("HH"),
        mm("mm"),
        ss("ss"),
        SSS("SSS"),
        yyyyMMddHHmmss("yyyyMMddHHmmss"),
        yyyy_MM_dd__HH_mm_ss__SSS("yyyy-MM-dd HH:mm:ss SSS"),
        yyyyMMddHHmmssSSS("yyyyMMddHHmmssSSS"),
        ;
        private final String dateFormat;

        DateFormatEnum(String dateFormat) {
            this.dateFormat = dateFormat;
        }
    }

    /**
     * 静态内部类声明单例Thread线程变量
     */
    private static class SingletonHolder {

        private static final ThreadLocal<Map<DateFormatEnum, DateFormat>> TL = new ThreadLocal<>();
    }

    /**
     * 初始化调用
     */
    private static ThreadLocal<Map<DateFormatEnum, DateFormat>> TL() {
        return SingletonHolder.TL;
    }

}
~~~
