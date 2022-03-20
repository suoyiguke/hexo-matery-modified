---
title: java小技巧2，使用枚举而不是if-else或者Switch来做数据字典兑换.md
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
定义枚举
~~~
package com.gbm.cloud.treasure.enums;

/**
 * @Author: hjh
 * @Date: 2021/7/7 17:54
 * @Description: 商品状态枚举
 */
public enum MgbGoodsStateEnum {
//
    ALL(0,"全部"),
    UP(1,"已上架"),
    DOWN(2,"已下架"),
    ;


    private Integer index;
    private String msg;

    MgbGoodsStateEnum(int index, String msg) {
        this.index = index;
        this.msg = msg;
    }


    public Integer getIndex() {
        return index;
    }

    public void setIndex(Integer code) {
        this.index = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }


    public static String getMsgByIndex(int index) {
        for (MgbGoodsStateEnum mgbGoodsStateEnum : values()) {
            if (mgbGoodsStateEnum.getIndex().equals(index)) {
                return mgbGoodsStateEnum.getMsg();
            }
        }
        return null;
    }



}

~~~

使用            vo.setStateName(MgbGoodsStateEnum.getMsgByIndex(vo.getState()));

~~~
        List<MgbGoodsVo> records = mgbGoodsVoPage.getRecords();
        for (MgbGoodsVo vo:records) {
            //获取品类名称
            //一级
            vo.setCatRootName(productCategoryMap.get(vo.getCatRootNo()));
            //二级
            vo.setCatParentName(productCategoryMap.get(vo.getCatParentNo()));
            //三级
            vo.setCatChildName(productCategoryMap.get(vo.getCatChildNo()));
            //上架渠道
            vo.setChannelName(channelMap.get(vo.getChannelKey()));
            //销量

            //商品状态
            vo.setStateName(MgbGoodsStateEnum.getMsgByIndex(vo.getState()));
            //获取0扣点采集价和代发价
//            getZeroPointsPrice(vo);
        }
~~~


>注意，这样使用枚举一定要从0开始。ordinal总是从0开始匹配的！从1开始的话会导致错开一位
