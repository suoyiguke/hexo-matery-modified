---
title: 通用点赞设计（一）使用redis的set类型.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 业务
categories: 业务
---
---
title: 通用点赞设计（一）使用redis的set类型.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 业务
categories: 业务
---
> 严于律己

可以使用redis来实现点赞，这比使用mysql这样的关系型数据库性能要强。redis数据存在内存中，读取迅速。能够支持更大的并发量，而且redis也可以持久化保证点赞数据不丢失。如果redis存入大量点赞数据而导致服务器内存负荷大这时就可以将redis和mysql一起配合使用

###需求

- 用户对`文章、视频、文章评论、视频评论` 等主体的 点赞和取消点赞

- 查询某个主体的特定对象的获赞总数
- 查询某个主体的特定对象的点赞用户集合
- 查询某个主体的各个对象的点赞总数，并做好按点赞数降序排列

###redis设计
######提出一些概念：
>点赞主体类型: 使用java中的枚举类型实现，类名为BType。需求中提到了有4种点赞主体类型`文章、视频、文章评论、视频评论` 

>点赞主体id: 四种主体的id均是由mysql表的自动增长主键设置的。使用Object subjectId

> 点赞用户id  即 Object postId

######实现方式
我们使用redis的 Set 类型来存储点赞数据

- key设计

点赞主体类型:点赞主体id
- value设计
将点赞用户id 即postId存入set


###具体实现

定义点赞主体的枚举类
~~~
package com.springboot.study.demo1.like.model;

/**
 *@description: BType 点赞主体的枚举类型
 *@author: yinkai
 *@create: 2020/3/11 15:31
 */
public enum BType {
    LIKED_ARTICLE("文章点赞"),
    LIKED_ARTICLECOMMENT("文章评论点赞"),
    LIKED_VIDEO("视频点赞"),
    LIKED_VIDEOCOMMENT("视频评论点赞");
    private String bType;

    BType(String bType) {
        this.bType = bType;
    }
}
~~~


定义生成redis key的工具类
~~~
package com.springboot.study.demo1.like.utils;
import com.springboot.study.demo1.like.model.BType;

/**
 *@description: LikedUtil 生成redis key的工具类
 *@author: yinkai
 *@create: 2020/3/11 16:43
 */
public class LikedUtil {
    public static String getKey(BType bType, Object bId) {
        return bType + ":" + bId;
    }

}
~~~

创建点赞的业务接口
~~~
package com.springboot.study.demo1.like.service;
import com.springboot.study.demo1.like.model.BType;

import java.util.Map;
import java.util.Set;

/**
 *@description: ILikedService 点赞接口
 *@author: yinkai
 *@create: 2020/3/11 16:39
 */
public interface ILikedService {

    /**
     * 点赞/取消点赞
     *
     * @param bType     业务类型
     * @param subjectId 被点赞主体ID
     * @param postId    点赞主体ID
     */
    void liked(BType bType, Object subjectId, Object postId);

    /**
     * 查询单个主体（如文章）的获赞个数，如 id为 1的文章被点赞的数量
     *
     * @param bType     业务类型
     * @param subjectId 被点赞主体ID
     * @return 点赞数量
     */
    Long count(BType bType, Object subjectId);

    /**
     * 查询单个主体（如文章）的点赞用户集合
     * @param bType
     * @param subjectId
     * @return
     */
    Set<Object> getPostUserSet(BType bType, Object subjectId);

    /**
     *  获取每个被点赞主体（如文章）的id和对应的点赞数量
     * @param bType
     * @return
     */
    Map<String, Long> getSubjectLikedCount(BType bType);

}
~~~

创建点赞接口实现类
~~~package com.springboot.study.demo1.like.service.impl;
import com.springboot.study.demo1.like.model.BType;
import com.springboot.study.demo1.like.service.ILikedService;
import com.springboot.study.demo1.like.utils.LikedUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.SetOperations;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class ILikedServiceImpl implements ILikedService {
    @Autowired
    private SetOperations setOperations;

    @Autowired
    private RedisTemplate redisTemplate;


    /**
     * 点赞/取消点赞
     *
     * @param bType     业务类型
     * @param subjectId 被点赞主体ID
     * @param postId    点赞主体ID
     */
    @Override
    public void liked(BType bType, Object subjectId, Object postId) {
        //生成key
        String key = LikedUtil.getKey(bType, subjectId);

        //判断key对应的set中是否存在subjectId
        //存在则取消点赞
        if (setOperations.isMember(key, postId)) {
            setOperations.remove(key, postId);
        } else {
            //不存在则点赞
            setOperations.add(key, postId);
        }

    }

    /**
     * 查询单个主体（如文章）的获赞个数，如 id为 1的文章被点赞的数量
     *
     * @param bType     业务类型
     * @param subjectId 被点赞主体ID
     * @return 点赞数量
     */
    @Override
    public Long count(BType bType, Object subjectId) {
        //生成key
        String key = LikedUtil.getKey(bType, subjectId);
        //获得点赞数量
        Long size = setOperations.size(key);
        return size;
    }

    /**
     * 查询单个主体（如文章）的点赞用户集合
     * @param bType
     * @param subjectId
     * @return
     */
    @Override
    public Set<Object> getPostUserSet(BType bType, Object subjectId) {
        //生成key
        String key = LikedUtil.getKey(bType, subjectId);
        Set members = setOperations.members(key);
        return members;
    }


    /**
     *  获取每个被点赞主体（如文章）的id和对应的点赞数量
     * @param bType
     * @return
     */
    @Override
    public Map<String, Long> getSubjectLikedCount(BType bType) {

        Map<String, Long> map = new HashMap<>();
        //得到以bType开头的所有key组成的集合
        Set<String> keys = redisTemplate.keys(bType + ":*");
        //遍历这些key
        for (String key : keys) {
            //获得key对应的set中元素的数量（点赞总数）
            Long total = setOperations.size(key);
            //将key截取，只取冒号之后的id作为map的key
            //将点赞总数作为map的value
            map.put(key.substring(key.lastIndexOf(":") + 1), total);
        }


        //按value升序排列
        map = sortByValue(map,true);

        return map;
    }





    /**
     * 实现map的value排序
     *
     * @param map
     * @param reverse
     * @return
     */

    public static Map sortByValue(Map map, final boolean reverse) {
        //将Map转为 List<Map.Entry>
        List list = new ArrayList(map.entrySet());
        //在 List<Map.Entry> 内部按元素getValue大小排序
        Collections.sort(list, new Comparator() {

            @Override
            public int compare(Object o1, Object o2) {
                if (reverse) {
                    return -((Comparable) ((Map.Entry) (o1)).getValue())
                            .compareTo(((Map.Entry) (o2)).getValue());
                }
                return ((Comparable) ((Map.Entry) (o1)).getValue())
                        .compareTo(((Map.Entry) (o2)).getValue());
            }
        });

        //将有序的List转为 LinkedHashMap，使用LinkedHashMap做插入顺序排序
        Map result = new LinkedHashMap(map.size());
        for (Iterator it = list.iterator(); it.hasNext(); ) {
            Map.Entry entry = (Map.Entry) it.next();
            result.put(entry.getKey(), entry.getValue());
        }

        list = null;
        return result;
    }





}




~~~

###点赞接口测试

~~~
package com.springboot.study.demo1;
import com.springboot.study.demo1.like.model.BType;
import com.springboot.study.demo1.like.service.ILikedService;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.Set;


/**
 * @author ceshi
 * @Title:
 * @Package
 * @Description:
 * @date 2020/3/1115:49
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class ILikedServiceImplTest {
    @Autowired
    ILikedService iLikedService;



    @org.junit.Test
    public void liked() {

        // 文章、文章评论、视频、视频评论四个主体 id为 1000、1001、1002 。被500个用户点赞
        for (int i = 0; i <500 ; i++) {
            iLikedService.liked(BType.LIKED_ARTICLE,1000,i);
            iLikedService.liked(BType.LIKED_ARTICLE,1001,i);
            iLikedService.liked(BType.LIKED_ARTICLE,1002,i);

            iLikedService.liked(BType.LIKED_ARTICLECOMMENT,1000,i);
            iLikedService.liked(BType.LIKED_ARTICLECOMMENT,1001,i);
            iLikedService.liked(BType.LIKED_ARTICLECOMMENT,1002,i);

            iLikedService.liked(BType.LIKED_VIDEO,1000,i);
            iLikedService.liked(BType.LIKED_VIDEO,1001,i);
            iLikedService.liked(BType.LIKED_VIDEO,1002,i);


            iLikedService.liked(BType.LIKED_VIDEOCOMMENT,1000,i);
            iLikedService.liked(BType.LIKED_VIDEOCOMMENT,1001,i);
            iLikedService.liked(BType.LIKED_VIDEOCOMMENT,1002,i);


        }
    }


    @org.junit.Test
    public void count() {

        Long count = iLikedService.count(BType.LIKED_ARTICLE, 1000);
        System.out.println(count);

    }

    @org.junit.Test
    public void getPostUserSet() {

        Set<Object> postUserSet = iLikedService.getPostUserSet(BType.LIKED_ARTICLE, 1000);

        for (Object obj : postUserSet) {
            System.out.println(obj);
        }

    }
}
~~~

运行测试liked()方法，插入数据如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e6573fb95166e82d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

运行测试getSubjectLikedCount()方法，查询视频类主体下所有视频的id对应点赞次数，并按点赞次数降序排列
![image.png](https://upload-images.jianshu.io/upload_images/13965490-57545feb00a24443.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###实现缺陷
1、按点赞数降序排列是在java程序中实现的，没有用到redis的排序功能

2、该实现方案只是保存了点赞用户的id，如果要查询用户的其它信息比如 头像、昵称等字段就必须到mysql中进行查询。这会对mysql造成一定的压力
