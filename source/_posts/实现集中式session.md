---
title: 实现集中式session.md
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
title: 实现集中式session.md
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
>墙角数枝梅，凌寒独自开

###需求：
使用redis实现session用户会话功能，同时只允许一个用户登录。新登录的会话会让旧的会话失效；会话保持30分钟，如果30分种内会话有活跃请求，则刷新失效时间


###设计：
使用redis的string类型即可完成。但是需要两个k-v键值对来保存会话信息。当然使用redis有个优势就是 `集中式的`； 如果应用水平扩展，工程部署为多个镜像，进行负载均衡。那么就不用考虑单点登录问题和实现session会话共享了。

######第一个k-v：
key ===> USERID_`UserId ` 

value  ===>  存入一个uuid，使用这个做 "token"。它会被返回给前端
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1210681065a64afd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
######第二个k-v：
key ===>  即第一个k-v的value。就是上面生成的uuid

value ===>  md5 (uuid+userId+username)  使用上面的uuid加盐，和userId、username一起进行生成md5摘要，保证每一次调用登录接口生成的value都不同
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9844a82869e591ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


> - token字符串由于是uuid实现，则每次访问登录接口都会生成一个新的字符串返回
> - 登录逻辑里需要判断，根据userId去redis拿数据如果存在则删除掉旧的会话信息，从而达到`同时只允许一个用户登录`的需求; 如果不存在直接生成会话信息即可
> - 设置redis中保存的会话信息30分钟后失效，并且每次正常返回需要带token的接口都需要刷新一下redis

###实现代码

> 基于springboot、mybatis_plus、redis 实现。关于mybatis_plus 可以看看我这篇文章https://www.jianshu.com/p/434bd76cef7e
redis集成看这篇 https://www.jianshu.com/p/ed4b3af12f25



mysql导入用户数据
~~~

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `age` int(11) NULL DEFAULT NULL COMMENT '年龄',
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '密码',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'yinkai', 24, 'yinkai@qq.com', 'e10adc3949ba59abbe56e057f20f883e');

SET FOREIGN_KEY_CHECKS = 1;

~~~

User实体类
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
    private String password;
}
~~~

编写一个拦截器

~~~
package com.springboot.study.demo1.Interceptor;

import com.alibaba.fastjson.JSON;
import com.baomidou.mybatisplus.extension.api.R;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.service.UserService;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.util.DigestUtils;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.concurrent.TimeUnit;

/**
 *@description: LoginInterceptor
 *@author: yinkai
 *@create: 2020/3/14 14:05
 */
public class LoginInterceptor implements HandlerInterceptor {

    @Autowired
    private ValueOperations valueOperations;
    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    @Autowired
    private UserService userService;
    /**
     * 进入controller层之前拦截请求
     * @param o
     * @return
     * @throws Exception
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object o) throws Exception {


        //跨域请求，*代表允许全部类型
        response.setHeader("Access-Control-Allow-Origin", "*");
        //允许请求方式
        response.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE");
        //用来指定本次预检请求的有效期，单位为秒，在此期间不用发出另一条预检请求
        response.setHeader("Access-Control-Max-Age", "3600");
        //请求包含的字段内容，如有多个可用哪个逗号分隔如下
        response.setHeader("Access-Control-Allow-Headers", "content-type,x-requested-with,Authorization, x-ui-request,lang,token");
        //访问控制允许凭据，true为允许
        response.setHeader("Access-Control-Allow-Credentials", "true");
        // 浏览器是会先发一次options请求，如果请求通过，则继续发送正式的post请求
        // 配置options的请求返回


        String token = request.getParameter("token");
        String userId = request.getParameter("userId");

        //参数非空判断，若为空则拦截
        if(StringUtils.isBlank(token)|| StringUtils.isBlank(userId)){
            response.setContentType("application/json;charset=UTF-8");
            R<Object> r = R.failed("没有带上token或其他参数");
            response.getWriter().print(JSON.toJSONString(r));
            return  false;
        }

        //按userId查询user信息
        //user为空则说明对应id的用户不存在，拦截
        User user = userService.getById(userId);
        if(user == null){
            response.setContentType("application/json;charset=UTF-8");
            R<Object> r = R.failed("用户不存在");
            response.getWriter().print(JSON.toJSONString(r));
            return  false;
        }

        //redis中无token信息
        String concat = "USERID_".concat(userId.toString());
        if(!stringRedisTemplate.hasKey(concat)){
            response.setContentType("application/json;charset=UTF-8");
            R<Object> r = R.failed("账号未登录，或者账号长时间未操作已过期");
            response.getWriter().print(JSON.toJSONString(r));
            return false;
        }

        //用户会话当前token 与 前端传过来的token进行比较，不相等则token失效或错误
        String uuidToken = (String)valueOperations.get(concat);
        if(!token.equals(uuidToken)){
            response.setContentType("application/json;charset=UTF-8");
            R<Object> r = R.failed("会话出错 或者 账号在其他地方登录，你被强制下线");
            response.getWriter().print(JSON.toJSONString(r));
            return false;
        }

        //得到以token为key的value值 即是 之前生成的md5
        String md5ValueRedis = (String) valueOperations.get(uuidToken);

        //用户id和name，使用uuidToken加盐获得md5摘要作为redis的 value
        //能够完成一个用户在另一台设备登录，则之前的登录token失效。需要重新登录的功能
        String md5Value = DigestUtils.md5DigestAsHex(user.getId().toString().concat(user.getName()).concat(uuidToken).getBytes());

        if(!md5Value.equals(md5ValueRedis)){
            response.setContentType("application/json;charset=UTF-8");
            R<Object> r = R.failed("用户信息生成的md5与redis中不一致");
            response.getWriter().print(JSON.toJSONString(r));
            return false;
        }


        //将token存入redis; userId做为key，uuidToken作为value  并设置过期时间---30分钟
        valueOperations.set("USERID_".concat(user.getId().toString()),uuidToken,30, TimeUnit.MINUTES);
        //将uuidToken 作为key md5Value作为value，
        valueOperations.set(uuidToken,md5Value,30, TimeUnit.MINUTES);

        return true;

    }

    @Override
    public void postHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, ModelAndView modelAndView) throws Exception {

    }

    @Override
    public void afterCompletion(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, Exception e) throws Exception {

    }

}
~~~


注册拦截器
> 拦截器不能拦截登录接口，排除掉登录接口的url
~~~
package com.springboot.study.demo1.config;

import com.springboot.study.demo1.Interceptor.LoginInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 *@description: WebAppConfig
 *@author: yinkai
 *@create: 2020/3/14 14:05
 */
@Configuration
public class WebAppConfig implements WebMvcConfigurer {


    @Bean(name="LoginInterceptor")
    public HandlerInterceptor getLoginInterceptor(){
        return new LoginInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {

        // 多个拦截器组成一个拦截器链
        // addPathPatterns 用于添加拦截规则
        // excludePathPatterns 用户排除拦截
        /**
         * 拦截所有请求,除了/user/checkUser 这个用户登录并返回token信息的接口
         */
        registry.addInterceptor(getLoginInterceptor()).excludePathPatterns("/user/checkUser");
    }



}
~~~

编写登录接口

>- checkUser接口在用户名密码正确后，返回一个token字符串给到前端
>- list接口表示需要被拦截的接口，请求需要带上token和userId才能被执行
~~~
package com.springboot.study.demo1.controller;

import com.baomidou.mybatisplus.extension.api.R;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.service.UserService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import javax.annotation.Resource;

/**
 * @description: UserController
 * @author: yinkai
 * @create: 2020/2/25 9:51
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Resource
    private UserService userService;


    /**
     * 测试接口
     * @return
     */
    @RequestMapping(value = "/list")
    public R list() {
        return R.ok(userService.list(null));
    }

    /**
     * 登录，返回token
     * @param user
     * @return
     */
    @RequestMapping(value = "/checkUser", method = RequestMethod.POST, produces = "application/json;charset=UTF-8")
    public R checkUser(User user) {
        return userService.checkUser(user.getName(), user.getPassword());
    }


}

~~~

编写登录service
~~~
package com.springboot.study.demo1.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.api.R;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.springboot.study.demo1.datasources.annotation.DataSource;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.mapper.UserMapper;
import com.springboot.study.demo1.service.UserService;
import javafx.scene.shape.VLineTo;
import lombok.SneakyThrows;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.SetOperations;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.DigestUtils;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

/**
 *@description: UserServiceImpl
 *@author: yinkai
 *@create: 2020/2/25 9:22
 */

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    @Autowired
    private ValueOperations<String, String> valueOperations;


    @Transactional(rollbackFor = Exception.class,isolation = Isolation.REPEATABLE_READ,propagation = Propagation.REQUIRED)
    @Override
    public R checkUser(String name, String password) {
        if(StringUtils.isBlank(name)||StringUtils.isBlank(password)){
            return  R.failed("参数异常");
        }

        password = DigestUtils.md5DigestAsHex(password.getBytes());
        User user = this.getBaseMapper().selectUserByNameAndPassword(name,password);
        if(user == null){
            return  R.failed("没有这个用户");
        }
        if(!user.getPassword().equals(password)) {
            return  R.failed("密码错误");
        }

        //存在性判断,存在则删除
        String concat = "USERID_".concat(user.getId().toString());

        if(stringRedisTemplate.hasKey(concat)){
            String s = valueOperations.get(concat);
            //删除旧token数据
            stringRedisTemplate.delete(s);
            stringRedisTemplate.delete(concat);
        }


        //使用uuid做key，这个key需要返回给前端。即所谓的 "token"
        String uuidToken = UUID.randomUUID().toString().replaceAll("-", "");

        //md5
        //使用用户id和name，加盐获得md5摘要作为redis的 value,再使用生成的uuid加盐！
        //让每次checkUser接口被调用，都会生成一个新的value
        // 能够完成一个用户在另一台设备登录，则之前的登录token失效。需要重新登录的功能
        String md5Value = DigestUtils.md5DigestAsHex(user.getId().toString().concat(user.getName()).concat(uuidToken).getBytes());



        //将token存入redis; userId做为key，uuidToken作为value  并设置过期时间---30分钟
        valueOperations.set("USERID_".concat(user.getId().toString()),uuidToken,30, TimeUnit.MINUTES);
        //将uuidToken 作为key md5Value作为value，
        valueOperations.set(uuidToken,md5Value,30, TimeUnit.MINUTES);

        //置空密码
        user.setPassword("");


        //将token和用户信息返回
        return R.ok(new HashMap<String,Object>(){{
            put("token",uuidToken);
            put("user",user);
        }});
    }



}

~~~

UserMapper 编写
~~~
package com.springboot.study.demo1.mapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.springboot.study.demo1.entity.User;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.springframework.transaction.annotation.Transactional;

/**
 *@description: UserMapper
 *@author: yinkai
 *@create: 2020/2/25 9:22
 */
@Mapper
public interface UserMapper extends BaseMapper<User> {



    @Select("select * from user where name = #{name} and password = #{password}")
    User selectUserByNameAndPassword(String name,String password);
}

~~~

###测试会话功能
调用一次 登录接口
http://192.168.10.106:8080/test/user/checkUser?name=yinkai&password=123456

返回了 token=e3aa65dbd0024e95ab1df3a007f8396a   和用户信息
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6cbcc1724c9af0df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

拿到这个token去访问一个需要token的接口
http://192.168.10.106:8080/test/user/list?token=e3aa65dbd0024e95ab1df3a007f8396a&userId=1
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e743e2d4715fcc11.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

返回信息没问题

如果将token参数改掉，则请求被拦截
[http://192.168.10.106:8080/test/user/list?token=e3aa65dbd0024e95ab1df3a007f8396a123&userId=1](http://192.168.10.106:8080/test/user/list?token=e3aa65dbd0024e95ab1df3a007f8396a&userId=1)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3c6760315e621eba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


再次调用登录接口，返回了最新的token
http://192.168.10.106:8080/test/user/checkUser?name=yinkai&password=123456
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e187e17fddbfe153.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么再次使用之前的旧token访问
[http://192.168.10.106:8080/test/user/list?token=e3aa65dbd0024e95ab1df3a007f8396a&userId=1](http://192.168.10.106:8080/test/user/list?token=e3aa65dbd0024e95ab1df3a007f8396a&userId=1)

功能没问题~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aa20afba46f5afa5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
