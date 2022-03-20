---
title: java-内部类应用之剥离配置到静态内部类让配置信息初始化不依赖于类的本身初始化.md
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
现在有这么一种情况

A 类和B类都实现了接口C，接口C中有两个方法，方法1和方法2。A类实现了方法1和方法2，而B类只实现了方法1，B类的方法2没有实现，只能去调用A类的方法2，但是这样调用会报空指针，因为A类使用了@ConditionalOnExpression注解且配置文件中声明使用的实现是B类，故初始化类A所需必要配置信息没办法得到有效的初始化。

那么我们可以这样处理：

1、将方法2声明为static方法并从接口C中移除；
2、将初始化A类的配置信息放到A类的静态内部类当中,然后加上@Component注解将此类纳入到spring容器的管理，这样A类初始化所需的配置就可以得到初始化了！



1、接口C
~~~
public interface AiService {

    //人脸
    void facePost(String image, String name, String idNo);

}

~~~

2、A类
~~~
@Service("BaiduUtilsServiceImpl")
@ConditionalOnExpression("'${business.idCartOcr.choice}'.equalsIgnoreCase('BAIDU')")
public class BaiduUtilsServiceImpl implements AiService {

  void facePost(String image, String name, String idNo){
       //实现接口1
      //访问内部类Conifg中的属性
 
   }

   //接口2 实现 改为静态；
    public static IdCart ocrPost(String photoFront, String photoBack) {
    //访问内部类Conifg中的属性
    }




    /**
     * 内部类
     */
    @Component
    public static class Config {

        private static String accessToken;
        private static String thirdEndpoint;
        private static String thirdClientId;
        private static String thirdClientSecret;
        //接口URL
        private static String thirdEndpointIdCart;
        private static String thirdEndpointFace;

        @NacosValue(value = "${business.idCartOcr.baidu.thirdClientId}", autoRefreshed = true)
        public void setThirdClientId(String thirdClientId) {
            Config.thirdClientId = thirdClientId;
        }

        @NacosValue(value = "${business.idCartOcr.baidu.thirdClientSecret}", autoRefreshed = true)
        public void setThirdClientSecret(String thirdClientSecret) {
            Config.thirdClientSecret = thirdClientSecret;
        }

        @NacosValue(value = "${business.idCartOcr.baidu.thirdEndpoint}", autoRefreshed = true)
        public void setThirdEndpoint(String thirdEndpoint) {
            Config.thirdEndpoint = thirdEndpoint;

            Config.thirdEndpointIdCart = String
                .format("%s/rest/2.0/ocr/v1/idcard", thirdEndpoint);
            Config.thirdEndpointFace = String
                .format("%s/rest/2.0/face/v3/person/verify", thirdEndpoint);
        }
    }

}


~~~

3、B类
~~~
@Service("GdcaUtilsServiceImpl")
@ConditionalOnExpression("'${business.idCartOcr.choice}'.equalsIgnoreCase('GDCA')")
public class GdcaUtilsServiceImpl implements AiService {

    @Override
    public void facePost(String image, String name, String idNo) {
    //实现
  }
}
~~~
