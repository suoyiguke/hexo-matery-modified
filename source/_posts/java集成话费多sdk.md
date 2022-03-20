---
title: java集成话费多sdk.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: sdk
categories: sdk
---
---
title: java集成话费多sdk.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: sdk
categories: sdk
---
~~~
package com.cy.demo.manager.huafeiduo;

import com.modules.api.utils.FastJsonUtil;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

/**
 * @author 话费多集成
 * @date 2019/4/119:31
 */
public class Hfeiduo {

    private static String _api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
    private static String _secret_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
    private static String _notify_url = "http://yourdomain.com/callback/huafeiduo";


    /**
     * 获得签名
     *
     * @param treeMap
     * @return
     */
    public static String _getSign(TreeMap<String, String> treeMap) {
        StringBuffer sb = new StringBuffer();
        for (Map.Entry<String, String> e : treeMap.entrySet()) {
            sb.append(e.getKey() + e.getValue());
        }
        System.out.println();
        return UrlUtil.encrypt32(sb.append(_secret_key).toString());
    }


    /**
     * 检查是否可充值
     *
     * @param card_worth
     * @param phone_number
     * @return
     */
    public static Map  check(String card_worth, String phone_number) {

        TreeMap treeMap = new TreeMap();
        treeMap.put("card_worth", card_worth);
        treeMap.put("phone_number", phone_number);
        treeMap.put("api_key", _api_key);
        treeMap.put("sign", _getSign(treeMap));

        String pream = UrlUtil.buildMap(treeMap);
        String s = HttpUtils.sendGet("http://api.huafeiduo.com/?mod=order.phone.check", pream);
        Map<String, Object> map = FastJsonUtil.json2Map(s);
        return map;
    }

    /**
     * 提交订单
     *
     * @param card_worth
     * @param phone_number
     * @param sp_order_id
     */
    public static Map submit(String card_worth, String phone_number, String sp_order_id) {
        TreeMap treeMap = new TreeMap();
        treeMap.put("card_worth", card_worth);
        treeMap.put("phone_number", phone_number);
        treeMap.put("notify_url", _notify_url);
        //系统订单，自己生成
        treeMap.put("sp_order_id", sp_order_id);
        treeMap.put("api_key", _api_key);
        treeMap.put("sign", _getSign(treeMap));

        String pream = UrlUtil.buildMap(treeMap);
        String s = HttpUtils.sendGet("http://api.huafeiduo.com/gateway.cgi?mod=order.phone.submit", pream);
        Map<String, Object> map = FastJsonUtil.json2Map(s);

        if (map.get("status").equals("success")) {
            System.out.println("充值成功！");

        }
        return  map;
    }


    /**
     * 获得余额
     *
     * @return
     */
    public static String getBalance() {
        TreeMap treeMap = new TreeMap();
        treeMap.put("api_key", _api_key);
        treeMap.put("sign", _getSign(treeMap));
        String pream = UrlUtil.buildMap(treeMap);
        String s = HttpUtils.sendGet("http://api.huafeiduo.com/gateway.cgi?mod=account.balance", pream);
        Map<String, Object> map = FastJsonUtil.json2Map(s);
        BigDecimal b = (BigDecimal) ((Map) map.get("data")).get("balance");
        return b.toString();

    }


    /**
     * 订单状态
     * order_status = init(订单初始化) | recharging(充值中) | success(充值成功) | failure(充值失败)
     *
     * @param sp_order_id
     * @return
     */
    public static String getRechargeStateByOrderId(String sp_order_id) {
        TreeMap treeMap = new TreeMap();
        treeMap.put("sp_order_id", sp_order_id);
        treeMap.put("api_key", _api_key);
        treeMap.put("sign", _getSign(treeMap));
        String pream = UrlUtil.buildMap(treeMap);
        String s = HttpUtils.sendGet("http://api.huafeiduo.com/gateway.cgi?mod=order.phone.status", pream);
        Map<String, Object> map = FastJsonUtil.json2Map(s);

        if (map.get("status").equals("success")) {
            Map data = (Map) map.get("data");
            String order_status = (String) data.get("order_status");
            System.out.println("订单状态==>");
            System.out.println(order_status);
            return order_status;

        }
        return (String) map.get("message");

    }


    /**
     * 订单信息
     *
     * @param sp_order_id
     * @return
     */
    public static Map<String, Object>  getOrderDetailByOrderId(String sp_order_id) {
        TreeMap treeMap = new TreeMap();
        treeMap.put("sp_order_id", sp_order_id);
        treeMap.put("api_key", _api_key);
        treeMap.put("sign", _getSign(treeMap));
        String pream = UrlUtil.buildMap(treeMap);
        String s = HttpUtils.sendGet("http://api.huafeiduo.com/gateway.cgi?mod=order.phone.get", pream);

        String s1 = UrlUtil.unicodeToString(s);
        Map<String, Object> map = FastJsonUtil.json2Map(s1);
        Map<String, Object> data = (Map<String, Object>) map.get("data");
        if(data!=null){
            return  data;
        }else {
            data = new HashMap<>();
            data.put("message",map.get("message"));
        }

        return data;

    }

    public static Map sendSubmit(String card_worth, String phone_number, String sp_order_id){
        Map check = check(card_worth, phone_number);
        if(!check.get("status").equals("success")){
            return check;
        }

        Map submit = submit(card_worth, phone_number, sp_order_id);
        return submit;
    }


    public static void main(String[] args) {

//         if(check("100", "13725290116")){
//             submit("1","13725290116", UUIDUtils.getUUID());
//         }
//
        //  System.out.println( getBalance());
        //

        //System.out.println(getRechargeStateByOrderId("0cf64a83caa64893b2034f4b714369e8"));

        Map<String, Object> orderDetailByOrderId = getOrderDetailByOrderId("2019042414295227591");
        System.out.println(orderDetailByOrderId);


    }


}


~~~
