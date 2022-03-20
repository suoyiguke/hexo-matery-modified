---
title: java持久化-mybatis-中如何防止${}带来的sql注入问题？（二）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: java持久化-mybatis-中如何防止${}带来的sql注入问题？（二）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
>大成若缺

在上篇文章 https://www.jianshu.com/p/8549841d24da ，我们知道有时候不得不使用${}。如like模糊查询和order by 动态传参这两种情况；

但\${}越会带来sql注入的风险，那么应该如何解决\${}带来的sql注入问题呢？

下面依次来讨论这两种情况

###order by 动态传参带来的注入问题

我们知道order by 动态传入排序字段，必须使用${}才行，但是会引发sql注入。如下所示


编写mappe接口
~~~
   @Select("select * from user order by ${column}")
    List<User> sqltest3(String column);
~~~

测试，传入 `id,(select 1 from (select sleep(10))a)` 

~~~
  @Test
    public void testInsert(){

        List<User> users = mapper.sqltest3("id,(select 1 from (select sleep(10))a)");
        for (User user : users) {
            System.out.println(user);
        }

    }
~~~

最终发出的sql是这样的
 >select * from user order by id,(select 1 from (select sleep(1000))a)

可以发现程序会阻塞10秒，如果把sleep时间改成1000000呢？再一直请求该接口，则足矣让系统瘫痪！而且只是orderby注入的一种手段。精通漏洞的黑客可不会讲情面


######解决\${}带来的orderby注入问题
我们可以在自定义排序的实体类User里定义一个静态的map，存入的key为前端传过来的值，value则是参与自定义排序的字段名。真正进行自定义排序的时候使用这个map即可。这样排序的${column}的值是由我们程序员自己定的，对邪恶的用户是不可见的

以下是思路demo
~~~
package com.springboot.study.demo1.entity;
import com.baomidou.mybatisplus.annotation.TableField;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import sun.plugin2.message.Serializer;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

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

    // key为前端传的值，value为数据库对应的列值
    public static Map<String,String> orderByKeyMap = new HashMap<String,String>(){
        {
            put("userId","id");
            put("name","name");
        }
    };
}
~~~
使用如下
~~~
    @Test
    public void testInsert(){

        //List<User> users = mapper.sqltest3(User.orderByKeyMap.get("userId"));
        List<User> users = mapper.sqltest3(User.orderByKeyMap.get("name"));
        for (User user : users) {
            System.out.println(user);
        }
    }

~~~


当然在springboot中可以使用aop实现
~~~
package com.jiazhi.aspect;

import java.lang.reflect.ParameterizedType;
import java.util.Map;
import java.util.regex.Pattern;

import org.apache.commons.lang3.StringUtils;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.stereotype.Component;

import com.jiazhi.util.ReflectUtils;

@Aspect
@Component
public class SortAspect {
	
	@SuppressWarnings({ "unchecked", "rawtypes" })
	@Before("execution(com.jiazhi.model.easyui.Grid com.jiazhi.service..*Impl.*(..)) or execution(* com.jiazhi.service.business..*Impl.*(..))")
    public void before(JoinPoint point) {
		Object[] args = point.getArgs();
		if (args != null && args.length > 0 && args[0] != null && args[0].getClass() != null) {
			if (args[0].getClass().toString().indexOf("java.util.LinkedHashMap") != -1) {
				Map<String, Object> params = (Map<String, Object>) args[0];
				if (params.get("sort") != null && params.get("isSortChange") == null) {
					String pattern = "[a-zA-Z\\.\\,_]+";
					 
					Class entityClass = (Class) ((ParameterizedType) point.getTarget().getClass().getGenericSuperclass()).getActualTypeArguments()[0]; 
					String columnName = ReflectUtils.getColumnName(entityClass, (String) params.get("sort"));
					if (StringUtils.isNotEmpty(columnName) && !columnName.equals((String) params.get("sort"))) {
						params.put("sort", columnName);
						params.put("isSortChange", true);
					}  else if (StringUtils.isNotEmpty(columnName) && columnName.equals((String) params.get("sort")) || Pattern.matches(pattern, (String) params.get("sort"))) {
						
					} else {
						params.remove("sort");
						params.remove("order");
					}
					if (params.get("order") == null || params.get("order") != null && !"asc".equals(params.get("order").toString().toLowerCase()) && !"desc".equals(params.get("order").toString().toLowerCase())) {
						params.put("order", "asc");
					}
				}
			}
		}
    }
}

~~~

###like查询带来的注入问题


编写mapper接口
~~~
 @Select("select * from user where name like '%${name}%'")
    List<User> sqltest2(String name);
~~~

我们传入`yin%' OR '1%'='1` 做like字段
~~~
    @Test
    public void test(){
        List<User> users = mapper.sqltest2("yin%' OR '1%'='1");
        for (User user : users) {
            System.out.println(user);
        }
    }
~~~
最终发出的sql如下，user表中的所有数据都会被查出来
> select * from user where name like '%yin%' OR '1%'='1%';


######解决like查询带来的注入问题
其实可以使用#{}的方式来进行like查询，只是需要使用mysql的concat()字符串拼接函数

如下
~~~
 @Select("select * from user where name like concat('%',#{name},'%')")
    List<User> sqltest2(String name);
~~~

最终的发出的sql
>select * from user where name like concat('%','yin','%');

我有一个疑惑，这样使用concat()会不会导致索引失效呢？
我们可以进行一个试验

首先，新建一个联合索引 `index_name_age_email`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-035ed85f1c650b65.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

进行查询计划分析，对比一下两条sql。一个使用 like '%y%' ；一个使用like concat('%','y','%')
~~~
  EXPLAIN select id,name,age,email from user WHERE name like concat('%','y','%')
  EXPLAIN select id,name,age,email from user WHERE name like '%y%'
~~~
分析的结果是一致的，说明这样使用concat()函数不会导致索引失效~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4b0c90da500b8ae8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

所以这种方式是可行的！
