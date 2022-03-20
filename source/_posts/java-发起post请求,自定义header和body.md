---
title: java-发起post请求,自定义header和body.md
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
~~~
package io.renren.modules.websocket.test;
import org.apache.http.HttpEntity;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.*;

/**
 * @date 2019/10/1017:12
 */
public class HttpUtils {


    //post请求
    /**
     * @param url
     * @param headerMap  header 参数
     * @param contentMap body 参数
     * @return
     */
    public static String postMap(String url, Map<String, String> headerMap, Map<String, String> contentMap) {
        String result = null;
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost post = new HttpPost(url);
        List<NameValuePair> content = new ArrayList<NameValuePair>();
        Iterator iterator = contentMap.entrySet().iterator();           //将content生成entity
        while (iterator.hasNext()) {
            Map.Entry<String, String> elem = (Map.Entry<String, String>) iterator.next();
            content.add(new BasicNameValuePair(elem.getKey(), elem.getValue()));
        }
        CloseableHttpResponse response = null;
        try {
            Iterator headerIterator = headerMap.entrySet().iterator();          //循环增加header
            while (headerIterator.hasNext()) {
                Map.Entry<String, String> elem = (Map.Entry<String, String>) headerIterator.next();
                post.addHeader(elem.getKey(), elem.getValue());
            }
            if (content.size() > 0) {
                UrlEncodedFormEntity entity = new UrlEncodedFormEntity(content, "UTF-8");
                post.setEntity(entity);
            }
            response = httpClient.execute(post);            //发送请求并接收返回数据
            if (response != null && response.getStatusLine().getStatusCode() == 200) {
                HttpEntity entity = response.getEntity();       //获取response的body部分
                result = EntityUtils.toString(entity);          //读取reponse的body部分并转化成字符串
            }
            return result;
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                httpClient.close();
                if (response != null) {
                    response.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
        return null;
    }


    // url格式转map
    public static Map<String, String> paramToMap(String paramStr) {
        String[] params = paramStr.split("&");
        Map<String, String> resMap = new HashMap<String, String>();
        for (int i = 0; i < params.length; i++) {
            String[] param = params[i].split("=");
            if (param.length >= 2) {
                String key = param[0];
                String value = param[1];
                for (int j = 2; j < param.length; j++) {
                    value += "=" + param[j];
                }
                resMap.put(key, value);
            }
        }
        return resMap;
    }

    //Header字符串转map
    public static Map<String, String> splid(String zz) {
        String[] stepOne = zz.split("\n");
        Map<String, String> map = new HashMap<String, String>();
        for (int i = 0; i < stepOne.length; i++) {
            String[] stepTwo = stepOne[i].split(": ");
            if (map.get(stepTwo[0]) == null)
                map.put(stepTwo[0], stepTwo[1]);
            else
                map.put(stepTwo[0], stepTwo[1] + "," + map.get(stepTwo[0]));
        }
        return map;
    }

    public static void main(String[] args) {
        String header =
                "Host: r.cnews.qq.com\n" +
                        "Accept-Encoding: gzip,deflate\n" +
                        "Referer: http://cnews.qq.com/cnews/android/\n" +
                        "User-Agent: %E5%A4%A9%E5%A4%A9%E5%BF%AB%E6%8A%A56080(android)\n" +
                        "Cookie: lskey=; luin=; skey=; uin=; logintype=0;\n" +
                        "snqn: isrlo83QeV0HUKSXBDEC2KU0i6dA6NJ+cJ6DfolV5BUaHTHKTIU0WQXRMHW9bo+0oWH2Uep5SZ6wOU2ufjuBOl9TYQKJaDModIprMcdjEIFHr32o8/mB9Da/apEitNzMj/o+zfCmWj7zQZTmMNvZaQ==\n" +
                        "svqn: 1_4\n" +
                        "qn-sig: 8da32c703ef980b76fc3343118e1a9f8\n" +
                        "qn-rid: 16e0d706-a1e4-465b-9a39-ce0caea0e03f\n" +
                        "Content-Type: application/x-www-form-urlencoded\n" +
                        "Connection: Keep-Alive";
        //"Content-Length: 2267\n";
        Map splid = splid(header);
        System.out.println(splid);
        Map<String, String> bodyMap = paramToMap("adcode=440111&last_id=20191008A046A900&lon=113.268162&cityList=%E5%B9%BF%E5%B7%9E&loc_streetNo=&forward=1&refreshType=normal&provinceId=19&last_time=1570521327&userCity=%E5%B9%BF%E5%B7%9E&bottom_id=20191007A0DZI400&loc_name=%E7%99%BD%E4%BA%91%E7%BB%BF%E5%9C%B0%E4%B8%AD%E5%BF%83&top_time=1570495721&manualRefresh=1&top_id=20191008A046A900&loc_addr=%E5%B9%BF%E4%B8%9C%E7%9C%81%E5%B9%BF%E5%B7%9E%E5%B8%82%E7%99%BD%E4%BA%91%E5%8C%BA%E4%BA%91%E5%9F%8E%E8%A5%BF%E8%B7%AF%E4%B8%8E%E9%BD%90%E5%BF%83%E8%B7%AF%E4%BA%A4%E5%8F%89%E5%8F%A3%E5%8D%97150%E7%B1%B3&page=8&cityId=198&lastRefreshTime=1570521327&loc_street=%E4%BA%91%E5%9F%8E%E8%A5%BF%E8%B7%AF&preload=1&loc_catalog=%E6%88%BF%E4%BA%A7%E5%B0%8F%E5%8C%BA%3A%E5%95%86%E5%8A%A1%E6%A5%BC%E5%AE%87&refresh_from=refresh_footer&direction=1&sessionid=undefined&chlid=kb_news_hotnews&bottom_time=1570435632&is_viola=1&loc_accuracy=40.0&lat=23.180721&REQBuildTime=1570521551393&adcode=440111&lon=113.268162&ssid=YR-TECH&omgid=f4287f3ea730a249015bd9d06a73f6dc23c00010212406&REQExecTime=1570521551412&qqnetwork=wifi&commonsid=7b7615ee4c8e412b9ba95ca7ebbca7eb&kingCardType=0&picSizeMode=0&adCookie=&commonGray=1_3%7C2_1%7C12_0%7C49_1%7C14_1%7C17_1%7C30_1%7C99_1&currentTab=kuaibao&proxy_addr=192.168.1.99%3A8888&is_wap=0&lastCheckCardType=0&omgbizid=a323e236f72cee4c10e96ec642cb73943d3a0080214908&imsi=460005292210411&commonIsFirstLaunch=0&bssid=22%3Abc%3A5a%3A74%3Aa0%3A88&taid=0101869FFED6E4A84F898262CADBA96EC2521FB86438AEE01A238B538F2A8F90BA0F96B93C4F0770FD1F0AED&activefrom=icon&unixtimesign=1570521551414&qimei=92a420ebc78a0356&Cookie=%26lskey%3D%26luin%3D%26skey%3D%26uin%3D%26logintype%3D0&qaid=0171E6660E55174412AC482013E10C8E&imsi_history=460005292210411&qn-sig=8da32c703ef980b76fc3343118e1a9f8&qn-rid=16e0d706-a1e4-465b-9a39-ce0caea0e03f&lat=23.180721&hw_fp=Coolpad%2FCool1_CN%2Fcool_c1%3A6.0.1%2FZAXCNFN5902606201S%2F0001820%3Auser%2Frelease-keys&gpu=Qualcomm%20Adreno%20%28TM%29%20510&mid=ca57d1f0e21794164956b43da41d7fea68de70fa&devid=861795038752864&mac=54%3ADC%3A1D%3A2A%3A0A%3A2A&store=9002096&screen_height=1920&apptype=android&origin_imei=861795038752864&codeclevel=5.1&rover=1&hw=Coolpad_C106&appversion=6.0.80&appver=23_areading_6.0.80&uid=92a420ebc78a0356&screen_width=1080&sceneid=&android_id=92a420ebc78a0356");

        String s = postMap("https://r.cnews.qq.com/getVerticalChannel?devid=861795038752864", splid, bodyMap);
        System.out.println(s);
    }

}


~~~
