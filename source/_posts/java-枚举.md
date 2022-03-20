---
title: java-枚举.md
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
1、根据name获得value，非常方便，不要去写switch了！
~~~
package com.sfpay.axg.enums;

import org.apache.commons.lang3.StringUtils;

public enum OrderPage {
    WAITPRINT("01", "待打印"),
    PRINTED("02", "已打印"),
    DELIVERGOODS("03", "已发货"),
    ALLORDER("04", "全部订单"),
    ORDERMANAGEMENT("05", "订单管理"),
    CATCHORDER("09", "抓单打印");

    private String key;

    private String value;

    OrderPage(String key, String value) {
        this.key = key;
        this.value = value;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    @Override
    public String toString() {
        return this.getKey();
    }

    /**
     * 根据key得到value
     * @param key
     * @return
     */
    public static String getValue(String key) {
        if (StringUtils.isBlank(key)) {
            return null;
        }
        for (OrderPage type : values()) {
            if (type.getKey().equals(key)) {
                return type.getValue();
            }
        }
        return null;
    }

    /**
     * 根据name 得到key
     * @param name
     * @return
     */
    public static String getKeyByName(String name) {
        OrderPage[] productEnums = values();
        for (OrderPage productEnum : productEnums) {
            if ((productEnum.name()).equals(name)) {
                return productEnum.key;
            }
        }
        return null;
    }


    public static void main(String[] args) {

        System.out.println(getKeyByName("1"));

    }

}

~~~

2、一个枚举类里还可以使用其它枚举对象作为成员属性

利用好这个写法可以维护一个关系 
~~~
package com.gbm.cloud.treasure.entity.mgbUndertakesOrder.Enum.option;

import com.gbm.cloud.common.util.Constant;
import com.gbm.cloud.treasure.entity.mgbUndertakesOrder.Enum.vo.UserEnum;

import java.util.Arrays;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
/**
 * @author 尹凯
 * @time 2021/8/9 17:02
 * @Description: 售后流程-已发货退货
 */
public enum ShippedReturnOption {
    /**
     * 已发货退货
     */
    ONE(0, "已发货退货", UserEnum.PLATFORMOOPERATION),
    TWO(1, "确认退货",UserEnum.SUPPLIER),
    THREE(2, "确认退款",UserEnum.PLATFORMOOPERATION);

    public static final String NO = "C";

    ShippedReturnOption(Integer code, String desc, UserEnum userEnum) {
        this.code = code;
        this.desc = desc;
        this.userEnum = userEnum;
    }

    public int code;
    public String desc;
    public UserEnum userEnum;



    private static Map<Integer, ShippedReturnOption> collect = Arrays.stream(ShippedReturnOption.values()).collect(Collectors.toMap(s -> s.code, section -> section,(v1,v2)->v2));

    public static Map<Integer, ShippedReturnOption> getAll() {
        return collect;
    }

    public static String getDescByCode(Integer code,UserEnum userEnum) {

        final Map<Integer, ShippedReturnOption> all = getAll();
        if (all.keySet().contains(code)) {
            final ShippedReturnOption shippedReturnOption = all.get(code);
            return Optional.ofNullable(shippedReturnOption).map(m -> m.userEnum.equals(userEnum) ? shippedReturnOption.desc : Constant.NOT_ME).orElse(null);

        }
        return null;
    }
}
~~~
~~~
public enum UserEnum {
    SUPPLIER(1, "供应商"),
    PLATFORMOOPERATION(2, "平台运营");

    UserEnum(int code, String desc) {
        this.code = code;
        this.desc = desc;
    }

    private int code;
    private String desc;


}

~~~
