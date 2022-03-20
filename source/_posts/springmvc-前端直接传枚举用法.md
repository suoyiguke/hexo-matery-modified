---
title: springmvc-前端直接传枚举用法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: springmvc-前端直接传枚举用法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
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

    public static void main(String[] args) {
        System.out.println(WAITPRINT.getKey());
        System.out.println(WAITPRINT.getValue());

        String value = getValue(WAITPRINT.getKey());
        System.out.println(value);
    }

}

~~~




~~~
	/**
	 * 查询订单自定义配置
	 */
	@RequestMapping(value = "/getOrderQueryConifg", method = RequestMethod.POST)
	@ResponseBody
	public JsonResult getOrderQueryConifg(@RequestParam(value = "pageName") OrderPage pageName) {

		User user = MemberUtil.getCurrentUser();
		JSONObject jsonObject = clientService.getOrderQueryConifg(user.getMemberNo(), pageName.getKey());
		return jsonResultHelper.buildSuccessJsonResult(jsonObject);
	}

~~~


postman  
>参数传枚举名字

![image.png](https://upload-images.jianshu.io/upload_images/13965490-8306e285d5cd36d3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
