---
title: webflux与spring集成方案1-平滑替换springmvc.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: webflux与spring集成方案1-平滑替换springmvc.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
~~~
 <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <!-- https://mvnrepository.com/artifact/io.projectreactor/reactor-core -->
        <dependency>
            <groupId>io.projectreactor</groupId>
            <artifactId>reactor-core</artifactId>
            <version>3.4.8</version>
        </dependency>
    </dependencies>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webflux</artifactId>
            <version>2.5.6</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.fangdada</groupId>
            <artifactId>demoReactor8</artifactId>
            <version>0.0.1-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>RELEASE</version>
            <scope>compile</scope>
        </dependency>
    </dependencies>
~~~


~~~
package com.fangdada.demowebfulx.controller;

import com.fangdada.demowebfulx.entity.User;
import com.fangdada.demowebfulx.service.UserService;
import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import javax.websocket.server.PathParam;
import java.awt.print.Book;
import java.time.Duration;
import java.util.Date;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;

/**
 * @Author: fd
 * @Date 2021/11/30 10:12
 * @Description: 注解编程模型实现SpringWebflux
 */
@RestController
public class UserController {

    @Value("#{'${test1:}'.empty ? '${test2:}' : '${test1:}'}")
    private String test;

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    //id 查询
    @GetMapping("/user/{id}")
    public Mono<User> getUserId(@PathVariable int id) {
        System.out.println(test);
        return userService.getUserById(id);
    }

    //查询所有
    @GetMapping(value = "/user", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<User> getUsers() {
        return userService.getAllUser();
    }

    //添加
    @PostMapping("/saveUser")
    public Mono<Void> saveUser(@RequestBody User user) {
        Mono<User> userMono = Mono.just(user);
        return userService.saveUserInfo(userMono);
    }



    @GetMapping(value = "/test", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<Book> sseBook(@RequestParam("num") Integer num) {
        if(num == null){
            throw new NullPointerException("num为空");
        }
        return Flux.interval(Duration.ofSeconds(1))
                .map(
                        second ->
                                new Book()
                                        .setId(String.valueOf(second))
                                        .setName("深入浅出Flux响应式Web编程" + second)
                                        .setPrice("12")
                ).take(num);
    }


    @Data
    @Accessors(chain = true)
    class Book {
        private String id;
        private String name;
        private String price;
        private Date createTime = new Date();
    }


}


~~~

service

~~~
public interface UserService {

	//根据id查询用户
	Mono<User> getUserById(int id);//Mono返回单个或零个元素

	//查询所有用户
	Flux<User> getAllUser();//Flux返回多个元素

	//添加用户
	Mono<Void> saveUserInfo(Mono<User> user);

}

~~~

impl

~~~
@Service
public class UserServiceImpl implements UserService {

	//创建map集合存储数据
	private final Map<Integer, User> users = new HashMap<>();

	public UserServiceImpl() {
		users.put(1,new User("lucy","nan",20));
		users.put(2,new User("mary","nv",30));
		users.put(3,new User("jack","nv",50));
	}

	//根据id查询
	@Override
	public Mono<User> getUserById(int id) {
		return Mono.justOrEmpty(users.get(id));
	}

	//查询多个用户
	@Override
	public Flux<User> getAllUser() {
		return Flux.fromIterable(users.values());
	}

	//添加用户 Mono.empty() 终止信号
	@Override
	public Mono<Void> saveUserInfo(Mono<User> userMono) {
		return userMono.doOnNext(person -> {
			//向map集合里面放值
			int id = users.size()+1;
			users.put(id,person);
		}).thenEmpty(Mono.empty());
	}
}

~~~

modul
~~~
@Data
@AllArgsConstructor
public class User {

	private String name;
	private String gender;
	private Integer age;

}

~~~
