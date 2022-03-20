---
title: springboot-操作redis的string和hash类型(二).md
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
title: springboot-操作redis的string和hash类型(二).md
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
###string类型
操作redis的string类型的核心类是org.springframework.data.redis.core.ValueOperations
它给我们提供了以下方法

好多重载啊，干的漂亮（sxbk）
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7387ca834fb1e420.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######下面一一对这些方法进行实践
毕竟文档没有写清楚，只是有参数和返回值。具体的作用根本没有提到，只有自己一个个去实践才能得出用法~
~~~
package com.springboot.study.demo1;

import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.*;
import org.springframework.test.context.junit4.SpringRunner;

import java.time.Duration;
import java.util.*;
import java.util.concurrent.TimeUnit;

/**
 *@description: Test1
 *@author: yinkai
 *@create: 2020/3/7 21:15
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test {
    @Autowired
    private ValueOperations<String, String> valueOperations;

    @org.junit.Test
    public void set() {

        /**========================= 写 ==========================**/
        //1、设置指定key的value值,若存在则直接覆盖
        valueOperations.set("name","yinkai hello");
        //设置指定key的value值，并10秒失效,若存在则直接覆盖
        valueOperations.set("des","hello world",10, TimeUnit.SECONDS);
        //覆盖指定key的value字符串，设置失效时间。使用jdk1.8的Duration类
        valueOperations.set("des","hello world",Duration.ofSeconds(2));
        //覆盖指定key的value字符串，从位置(offset) 8开始
        valueOperations.set("name","redis", 7);



        //2、尝试插入key-value。若存在指定key，忽略此次插入，返回false；不存在指定key，则写入，返回true
          //false
        System.out.println(valueOperations.setIfAbsent("name","yinxuan"));
          //true
        System.out.println(valueOperations.setIfAbsent("age","24"));
        //这个可设置超时时间 使用JUC的TimeUnit类
        valueOperations.setIfAbsent("jj.cale","24",10,TimeUnit.SECONDS);
        //这个可设置超时时间 使用java8的java.time.Duration类
        valueOperations.setIfAbsent("jj.cale", "24",  Duration.ofSeconds(10));


        //3、尝试插入key-value。不存在不插入，存在则覆盖
           //false
        System.out.println(valueOperations.setIfPresent("alen", "24"));
           //true
        System.out.println(valueOperations.setIfPresent("name", "24"));
        //这个可设置超时时间 使用JUC的TimeUnit类
        valueOperations.setIfAbsent("name", "24",10,TimeUnit.SECONDS);
        //这个可设置超时时间 使用java8的java.time.Duration类
        valueOperations.setIfAbsent("name", "24",Duration.ofSeconds(2));


        //4、将key-value 键值对列表 批量插入redis,若存在则直接覆盖
        valueOperations.multiSet(new HashMap<String, String>(){{
             put("key1","value1");
             put("key2","value2");
             put("key3","value3");
        }});


        //5、尝试插入key-value键值对列表。若存在指定key，忽略此次插入，返回false；不存在指定key，则写入，返回true
        Boolean b1 = valueOperations.multiSetIfAbsent(new HashMap<String, String>() {{
            put("key1", "value1+");
            put("key2", "value2+");
            put("key3", "value3+");
        }});
           //false
        System.out.println(b1);

        Boolean b2 = valueOperations.multiSetIfAbsent(new HashMap<String, String>() {{
            put("key111", "value1+");
            put("key2222", "value2+");
            put("key3333", "value3+");
        }});
            //true
        System.out.println(b2);


        //6、覆盖指定key的value，返回之前的旧值
        System.out.println(valueOperations.getAndSet("name","yinxuang"));


        //7、给指定的key的value值后面拼接字符串
        //key不存在则直接写入
        valueOperations.append("wowo","Hello");
        System.out.println(valueOperations.get("wowo"));
        //key存在则在尾巴后面拼接
        valueOperations.append("wowo"," world!");
        System.out.println(valueOperations.get("wowo"));


        //8、给指定key的value加 整数 1
        System.out.println(valueOperations.increment("age"));
        //指定具体整数
        System.out.println(valueOperations.increment("age", 2));
        //给指定key的value加 浮点数 1.2
        valueOperations.increment("age",1.2);


        //9、给指定key的value减整数 1
        valueOperations.decrement("age");
        //指定具体整数
        valueOperations.decrement("age",2);






        //10、对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit)
        //key键对应的值value对应的ascii码,在offset的位置(从左向右数)变为value
        valueOperations.set("bitTest","a");
        // 'a' 的ASCII码是 97。转换为二进制是：01100001
        // 'b' 的ASCII码是 98  转换为二进制是：01100010
        // 'c' 的ASCII码是 99  转换为二进制是：01100011
        //因为二进制只有0和1，在setbit中true为1，false为0，因此我要变为'b'的话第六位设置为1，第七位设置为0
        valueOperations.setBit("bitTest",6, true);
        valueOperations.setBit("bitTest",7, false);
        System.out.println(valueOperations.get("bitTest"));


        /**========================= 读 ==========================**/



        //11、从0到5截取指定key为wowo的value字符串，它并不会影响redis里的值。只是将value取出来然后截取而已
        System.out.println(valueOperations.get("wowo",0,5));


        //12、根据key 获得 value
        System.out.println(valueOperations.get("name"));

        //13、获得key列表对应的value列表
        System.out.println(valueOperations.multiGet(Arrays.asList("key1", "key2", "key3")));


        //14、获取指定key对应的value字符串长度
        System.out.println(valueOperations.size("name"));

        //15、获取key对应value的ascii码的在offset处位值
        System.out.println(valueOperations.getBit("bitTest",7));


        //16、bitField
        //valueOperations.bitField();

        //17、获得RedisOperations对象
        RedisOperations<String, String> operations = valueOperations.getOperations();

    }
}
~~~


###hash类型
springboot中操作redis的hash类型的核心类是org.springframework.data.redis.core.HashOperations

它为我们提供了16个方法如下，hash类型的方法比string类型就少了更多了啊
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9c269bd15edf06d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######对这些方法进行一些使用测试
~~~
package com.springboot.study.demo1;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.*;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.*;

/**
 *@description: Test
 *@author: yinkai
 *@create: 2020/3/7 21:15
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test {
    @Autowired
    private HashOperations<String, String, Object> hashOperations;

    @Test
    public void set() {

        /**========================= 写 ==========================**/

        //1、存入整个hash对象
        Map<String,Object> map = new HashMap();
        map.put("name","yinkai");
        map.put("age",24);
        map.put("sex","男");
        hashOperations.putAll("key",map);

        //2、存入hash对象的指定hashkey和value
        hashOperations.put("key","desc","hello world");

        //3、仅当hashKey不存在时才设置散列hashKey的value。
        //age存在，返回 false 设置失败
        System.out.println(hashOperations.putIfAbsent("key","age",30));
        //tel不存在，返回 true 设置成功
        System.out.println(hashOperations.putIfAbsent("key","tel","110"));


        //4、根据key和hashkey删除一个value
        System.out.println(hashOperations.delete("key","desc"));


        //5、给指定的key、hashkey的value 叠加 整数1
        System.out.println(hashOperations.increment("key","age",1));

        //6、给指定的key、hashkey的value 叠加浮点数
        System.out.println(hashOperations.increment("key","age",1.1));




        /**========================= 读 ==========================**/


        //7、根据key，得到整个hash对象
        Map<String, Object> redisHash1 = hashOperations.entries("key");
        System.out.println(redisHash1);

        //8、通过根据key，得到hash对象的key列表
        Set<String> set = hashOperations.keys("key");
        System.out.println(set);

        //9、根据key，得到hash对象的value列表
        List<Object> list = hashOperations.values("key");
        System.out.println(list);


        //10、根据key和hashkey列表获得对应的value列表
        List<String> list2 = new ArrayList<>();
        list2.add("name");
        list2.add("age");
        List<Object> key = hashOperations.multiGet("key", list2);
        System.out.println(key);

        //11、根据key 和 hashkey 得到一个value
        System.out.println(hashOperations.get("key", "name"));



        //12、根据key和hashkey 判断对应的value是不是存在
        // 不存在返回false
        System.out.println(hashOperations.hasKey("key","haha"));
        // 存在返回true
        System.out.println(hashOperations.hasKey("key","age"));


        //13、获取key对应的hash对象的属性个数
        System.out.println(hashOperations.size("key"));

        //14、使用Cursor在key的hash中迭代遍历
        Cursor<Map.Entry<String, Object>> curosr = hashOperations.scan("key", ScanOptions.NONE);
        while(curosr.hasNext()){
            Map.Entry<String, Object> entry = curosr.next();
            System.out.println(entry.getKey()+"===>"+entry.getValue());
        }

        //15、根据key和hashkey 获得对应的value的长度。不存则在返回0
        System.out.println(hashOperations.lengthOfValue("key", "age"));

        //16、获得RedisOperations 对象
        RedisOperations<String, ?> operations = hashOperations.getOperations();


    }
}
~~~
