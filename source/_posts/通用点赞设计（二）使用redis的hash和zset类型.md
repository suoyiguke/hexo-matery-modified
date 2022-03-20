---
title: 通用点赞设计（二）使用redis的hash和zset类型.md
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
title: 通用点赞设计（二）使用redis的hash和zset类型.md
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
> 靡不有初，鲜克有终

这次我们来使用hash和zset完成点赞功能

###使用hash类型设计点赞功能

我们知道redis的hash类型需要三个参数。key、hashkey 和 value。在点赞业务中，可以做如下设计

>key 设计 ==> 使用  `枚举标识符:文章的ID`作为key
hashkey 设计==> 点赞用户的id作为hashkey
value 设计 ==> 使用点赞的用户信息做为value 

这样就能完成直接展示点赞人的具体信息，而不需要到mysql中再次查询了。之前使用set类型是做不到这点的

![image.png](https://upload-images.jianshu.io/upload_images/13965490-8e59d2a5398368b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###使用zset设计获赞主体排行榜功能
要展示一个被点赞数据从大到小排序的文章列表，这个功能就可以使用redis的Zset类型来实现，因为Zset是可排序的

那么可以做如下设计

>key 设计 ==> 使用 主体类型的 `枚举标识符`作为key
value 设计 ==> 使用被点赞的主体信息做为value 

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1c0ba1d8c44a6d0b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###具体实现
主体类型枚举类
~~~
package com.springboot.study.demo1.like.model;

/**
 *@description: BType 点赞主体的枚举类型
 *@author: yinkai
 *@create: 2020/3/11 15:31
 */
public enum BType {
    //点赞
    LIKED_ARTICLE("文章点赞"),
    LIKED_ARTICLECOMMENT("文章评论点赞"),
    LIKED_VIDEO("视频点赞"),
    LIKED_VIDEOCOMMENT("视频评论点赞"),

    //点赞统计
    LIKED_ARTICLE_REPORT ("文章点赞统计"),
    LIKED_ARTICLECOMMENT_REPORT("文章评论点赞统计"),
    LIKED_VIDEO_REPORT("视频点赞统计"),
    LIKED_VIDEOCOMMENT_REPORT("视频评论点赞统计");

    private String bType;

    BType(String bType) {
        this.bType = bType;
    }

    public String getbType() {
        return bType;
    }

    public void setbType(String bType) {
        this.bType = bType;
    }
}
~~~



redis的 key生成工具类
~~~
package com.springboot.study.demo1.like.utils;

import com.springboot.study.demo1.like.model.BType;

/**
 * 生成Redis的 key
 */
public class LikedUtil {


    /**
     * 生成点赞的key
     *
     * @param bType
     * @param subjectId
     * @return
     */
    public static String getKey(BType bType, Object subjectId) {
        return bType + ":" + subjectId;
    }


    /**
     * 生成点赞数量的key
     *
     * @param bType
     * @return
     */
    public static String getReportKey(BType bType) {

        BType type = null;

        switch (bType) {
            case LIKED_ARTICLE:
                type = BType.LIKED_ARTICLE_REPORT;
                break;
            case LIKED_ARTICLECOMMENT:
                type = BType.LIKED_VIDEO_REPORT;
                break;
            case LIKED_VIDEO:
                type = BType.LIKED_VIDEO_REPORT;
                break;
            case LIKED_VIDEOCOMMENT:
                type = BType.LIKED_VIDEOCOMMENT_REPORT;
                break;
            //默认返回LIKED_ARTICLE_REPORT 文章数量key
            default:
                type = BType.LIKED_ARTICLE_REPORT;

        }
        return type.name();
    }


    public static void main(String[] args) {
        String key = LikedUtil.getReportKey(BType.LIKED_ARTICLE);
        System.out.println(key);
    }
}
~~~


创建User实体类
~~~
package com.springboot.study.demo1.entity;
import com.baomidou.mybatisplus.annotation.TableField;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import sun.plugin2.message.Serializer;

import java.io.Serializable;

/**
 *@description: User 实体类
 *@author: yinkai
 *@create: 2020/2/25 9:21
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Accessors(chain = true)
public class User implements Serializable {
    private Long id;
    private String name;
    private Integer age;
    private String email;
    @TableField(exist = false)
    private Integer count;
}
~~~





主体（文章）实体的实体类
~~~
package com.springboot.study.demo1.entity;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Accessors(chain = true)
public class Article {
    //文章id
    private Integer articleId;
    //文章标题
    private String title;
    //文章摘要
    private String summary;
    //文章图片
    private String img;

    //点赞数，该字段只用于排行版统计
    private Integer likeNum;
}
~~~


定义service接口

~~~
package com.springboot.study.demo1.like.service;
import com.springboot.study.demo1.like.model.BType;
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
     * @param user    点赞用户
     * @param subject    被点赞主体
     */
    void liked(BType bType, Object subjectId, Object postId, Object user,Object subject);

    /**
     * 查询单个主体（如文章）的获赞个数，如 id为 1的文章被点赞的数量
     *
     * @param bType     实体类型
     * @param subjectId 被点赞主体ID
     * @return 点赞数量
     */
    Long count(BType bType, Object subjectId);

    /**
     * 获得获得点赞数 前top名的bType排行版
     * @param bType  实体类型
     * @return top 排行版截取数
     */
    Set<Object> getSubjectTopN(BType bType, Long top);

}
~~~

编写实现类
> 实现了三个方法。 liked方法 实现 点赞和取消点赞、count方法查询具体主体（文章）的获赞总数、getSubjectTopN方法 获得点赞数指定前多少名的主体排行榜

>  liked方法在实现点赞逻辑以外还 插入了被点赞文章的信息。这样为之后的排行榜查询提供了数据

~~~
package com.springboot.study.demo1.like.service.impl;
import com.springboot.study.demo1.entity.Article;
import com.springboot.study.demo1.like.model.BType;
import com.springboot.study.demo1.like.service.ILikedService;
import com.springboot.study.demo1.like.utils.LikedUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.HashOperations;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ZSetOperations;
import org.springframework.stereotype.Service;
import java.util.Set;

@Service
public class ILikedServiceImpl implements ILikedService {

    @Autowired
    private RedisTemplate redisTemplate;
    @Autowired
    private HashOperations<String, Object, Object> hashOperations;
    @Autowired
    private ZSetOperations<String, Object> zSetOperations;


    /**
     * 点赞/取消点赞
     *
     * @param bType     业务类型
     * @param subjectId 被点赞主体ID
     * @param postId    点赞主体ID
     */
    @Override
    public void liked(BType bType, Object subjectId, Object postId, Object user, Object subject) {

        /**
         * 点赞实现，操作hash
         */
        //生成点赞key
        String key = LikedUtil.getKey(bType, subjectId);
        //判断key对应的set中是否存在subjectId
        //存在则取消点赞
        Boolean aBoolean = hashOperations.hasKey(key, postId);
        if (aBoolean) {
            hashOperations.delete(key, postId);
        } else {
            //不存在则点赞
            hashOperations.put(key, postId, user);
        }

        /**
         *
         *
         * 在点赞和取消点赞的同时进行 点赞统计排序实现，操作zset
         */

        //生成点赞统计key
        String reportKey = LikedUtil.getReportKey(bType);
        if (aBoolean) {
            //已经存在赞

            //需要取消点赞，设置分数为 -1 ， 最低分数
            zSetOperations.incrementScore(reportKey, subject, -1);
        } else {
            //不存在赞

            //需要点赞

            //获得分数
            Double score = zSetOperations.score(reportKey, subject);
            if (score == null) {
                //score分数不存在则设置 score为1
                zSetOperations.add(reportKey, subject, 1);
            } else {
                //score分数存在则 zset的score分数加1
                zSetOperations.incrementScore(reportKey, subject, 1);
            }
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
        Long size = hashOperations.size(key);
        return size;
    }

    @Override
    public Set<Object> getSubjectTopN(BType bType, Long top) {

        //获得点赞主体排行版
        Set<Object> set = zSetOperations.reverseRange(LikedUtil.getReportKey(bType), 0, top);

        //得到以bType开头的所有key组成的集合
        Set<String> keys = redisTemplate.keys(bType + ":*");


        //给返回结果集设置 点赞数
        for (Object obj : set) {
            for (String key : keys) {
                Integer id = Integer.valueOf(key.substring(key.lastIndexOf(":") + 1));
                if (((Article) obj).getArticleId().equals(id)) {
                    ((Article) obj).setLikeNum(hashOperations.size(key).intValue());
                }
            }
        }
        return set;
    }


}





~~~


功能测试
~~~
package com.springboot.study.demo1;

import com.springboot.study.demo1.entity.Article;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.like.model.BType;
import com.springboot.study.demo1.like.service.ILikedService;
import org.junit.runner.RunWith;
import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import reactor.core.publisher.Flux;

import java.util.Map;
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


        //文章1、文章2、文章3分被点赞

        Article article1 = new Article().setArticleId(1000).setTitle("文章1").setSummary("aaaaaaaaaaaaa").setImg("图");
        Article article2 = new Article().setArticleId(1001).setTitle("文章2").setSummary("bbbbbbbbbbbbb").setImg("图");
        Article article3 = new Article().setArticleId(1002).setTitle("文章3").setSummary("ccccccccccccc").setImg("图");

        //对id为 1000点赞
        iLikedService.liked(BType.LIKED_ARTICLE, 1000, 1, new User().setId((long) 1).setName("A").setAge(22), article1);

        //对id为 1001点赞
        iLikedService.liked(BType.LIKED_ARTICLE, 1001, 2, new User().setId((long) 2).setName("B").setAge(23),article2);
        iLikedService.liked(BType.LIKED_ARTICLE, 1001, 3, new User().setId((long) 3).setName("B").setAge(24),article2);


        //对id为 1002点赞
        iLikedService.liked(BType.LIKED_ARTICLE, 1002, 1, new User().setId((long) 1).setName("C").setAge(24),article3);
        iLikedService.liked(BType.LIKED_ARTICLE, 1002, 2, new User().setId((long) 2).setName("C").setAge(24),article3);
        iLikedService.liked(BType.LIKED_ARTICLE, 1002, 3, new User().setId((long) 3).setName("C").setAge(24),article3);

    }


    @org.junit.Test
    public void likedCancel() {

        //取消id为2的用户对LIKED_ARTICLE文章id为1000的点赞
        Article article1 = new Article().setArticleId(1000).setTitle("文章1").setSummary("aaaaaaaaaaaaa").setImg("图");
        iLikedService.liked(BType.LIKED_ARTICLE, 1000, 0, new User().setId((long) 0).setName("A").setAge(22), article1);

    }


    @org.junit.Test
    public void count() {

        Long count = iLikedService.count(BType.LIKED_ARTICLE, 1000);
        System.out.println(count);

    }

    @org.junit.Test
    public void getSubjectTopN() {

        Set<Object> subjectTopN = iLikedService.getSubjectTopN(BType.LIKED_ARTICLE, 100L);

        System.out.println(subjectTopN);

    }
}
~~~
