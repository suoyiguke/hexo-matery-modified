---
title: springboot--hession.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: PRC
categories: PRC
---
---
title: springboot--hession.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: PRC
categories: PRC
---
http://hessian.caucho.com/#Java

hessian是一个亲量级的RPC框架


https://blog.csdn.net/weixin_33671935/article/details/88685686


~~~
 <dependency>
            <groupId>com.caucho</groupId>
            <artifactId>hessian</artifactId>
            <version>4.0.60</version>
 </dependency>
~~~



###hession-server
HessionServiceConfig是hession服务端的核心类，用作配置当前的UserService等RPC接口。

~~~
@Configuration
public class HessionServiceConfig {
    @Autowired
    private UserService userService;
    //定义RPC接口的URL
    @Bean("/userService")
    public HessianServiceExporter userService() {
        HessianServiceExporter exporter = new HessianServiceExporter();
        exporter.setService(userService);
        exporter.setServiceInterface(UserService.class);
        return exporter;
    }
}
~~~

定义UserService 接口
~~~
public interface UserService {
  List<User> getUserList();
}
~~~
定义UserServiceImpl实现类
~~~
@Service("userService")
public class UserServiceImpl implements UserService {
    @Override
    public List<User> getUserList() {
        ArrayList<User> users = new ArrayList<>(4);
        users.add(new User("1", "name1"));
        users.add(new User("2", "name2"));
        users.add(new User("3", "name3"));
        users.add(new User("4", "name4"));
        return users;
    }
}
~~~

定义User类，该类要参与RPC的传输。
~~~
@NoArgsConstructor
@AllArgsConstructor
@Data
public class User implements Serializable {
    private String id;
    private String name;
}
~~~


hession-server以9000端口启动。

###hession-client
HessianClientConfig是hession客户端的核心类，用作配置刚刚创建的hession-server端发布的RPC接口。

~~~
@Configuration
public class HessianClientConfig {
    @Bean
    public HessianProxyFactoryBean userService() {
        HessianProxyFactoryBean factory = new HessianProxyFactoryBean();
        //设置hession-server端暴露的RPC接口地址；
        factory.setServiceUrl("http://localhost:9000/userService");
        //设置接口
        factory.setServiceInterface(UserService.class);
        return factory;
    }
}
~~~

然后就可以之直接注入使用：
~~~
@RestController
public class HessionClientController {
    @Autowired
    private UserService userService;
    @GetMapping("/getUserList")
    public List<User> getUserList() {
        return userService.getUserList();
    }
}
~~~

###问题

1、java.io.EOFException: readObject: unexpected end of file

用于RPC的类要实现序列化接口`Serializable`
