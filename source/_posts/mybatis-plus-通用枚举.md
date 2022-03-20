---
title: mybatis-plus-通用枚举.md
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
title: mybatis-plus-通用枚举.md
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
# 通用枚举

解决了繁琐的配置，让 mybatis 优雅的使用枚举属性！

> 自`3.1.0`开始，如果你无需使用原生枚举，可配置默认枚举来省略扫描通用枚举配置 [默认枚举配置](https://mp.baomidou.com/config/#defaultEnumTypeHandler)
> 
> *   升级说明:
>     
>     
>     
>     `3.1.0` 以下版本改变了原生默认行为,升级时请将默认枚举设置为`EnumOrdinalTypeHandler`
>     
>     
> *   影响用户:
>     
>     
>     
>     实体中使用原生枚举
>     
>     
> *   其他说明:
>     
>     
>     
>     配置枚举包扫描的时候能提前注册使用注解枚举的缓存

# [#](https://mp.baomidou.com/guide/enum.html#_1%E3%80%81%E5%A3%B0%E6%98%8E%E9%80%9A%E7%94%A8%E6%9E%9A%E4%B8%BE%E5%B1%9E%E6%80%A7)1、声明通用枚举属性

> 方式一： 使用 @EnumValue 注解枚举属性 [完整示例(opens new window)](https://gitee.com/baomidou/mybatis-plus-samples/blob/master/mybatis-plus-sample-enum/src/main/java/com/baomidou/mybatisplus/samples/enums/enums/GradeEnum.java)

```
public enum GradeEnum {

    PRIMARY(1, "小学"),  SECONDORY(2, "中学"),  HIGH(3, "高中");

    GradeEnum(int code, String descp) {
        this.code = code;
        this.descp = descp;
    }

    @EnumValue//标记数据库存的值是code
    private final int code;
    //。。。
}

```

> 方式二： 枚举属性，实现 IEnum 接口如下：

```
public enum AgeEnum implements IEnum<Integer> {
    ONE(1, "一岁"),
    TWO(2, "二岁"),
    THREE(3, "三岁");

    private int value;
    private String desc;

    @Override
    public Integer getValue() {
        return this.value;
    }
}

```

> 实体属性使用枚举类型

```
public class User {
    /**
     * 名字
     * 数据库字段: name varchar(20)
     */
    private String name;

    /**
     * 年龄，IEnum接口的枚举处理
     * 数据库字段：age INT(3)
     */
    private AgeEnum age;

    /**
     * 年级，原生枚举（带{@link com.baomidou.mybatisplus.annotation.EnumValue}):
     * 数据库字段：grade INT(2)
     */
    private GradeEnum grade;
}

```

#2、配置扫描通用枚举

*   注意!! spring mvc 配置参考，安装集成 MybatisSqlSessionFactoryBean 枚举包扫描，spring boot 例子配置如下：

>typeEnumsPackage: com.baomidou.springboot.entity.enums 的这个包要是自己枚举类所在的包！

```
mybatis-plus:
    # 支持统配符 * 或者 ; 分割
    typeEnumsPackage: com.baomidou.springboot.entity.enums
  ....

```

#如何序列化枚举值为数据库存储值？

## Jackson

### 一、重写toString方法

#### springboot中全局配置

```
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer customizer(){
        return builder -> builder.featuresToEnable(SerializationFeature.WRITE_ENUMS_USING_TO_STRING);
    }

```

####jackson 局部配置

```
    ObjectMapper objectMapper = new ObjectMapper();
    objectMapper.configure(SerializationFeature.WRITE_ENUMS_USING_TO_STRING, true);

```

以上两种方式任选其一,然后在枚举中复写toString方法即可.

###二、jackson 注解处理

```
public enum GradeEnum {

    PRIMARY(1, "小学"),  SECONDORY(2, "中学"),  HIGH(3, "高中");

    GradeEnum(int code, String descp) {
        this.code = code;
        this.descp = descp;
    }

    @EnumValue
  	@JsonValue	//标记响应json值
    private final int code;
}

```

## Fastjson


#### Fastjson全局处理方式

```
		FastJsonConfig config = new FastJsonConfig();
		config.setSerializerFeatures(SerializerFeature.WriteEnumUsingToString);

```

#### Fastjson局部处理方式

```
		@JSONField(serialzeFeatures= SerializerFeature.WriteEnumUsingToString)
		private UserStatus status;

```

以上两种方式任选其一,然后在枚举中复写toString方法即可.




###效果

![image.png](https://upload-images.jianshu.io/upload_images/13965490-39b2a3db6511cea5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
















###使用示例
从数据库中查出来的数据直接是枚举类型的。这样不用自己再进行额外的处理。很方便


枚举类
- toSting 重写为直接返回想要翻译的字段
- @EnumValue//标记数据库存的值是code

~~~
package com.gbm.cloud.treasure.entity.myUser.vo;

import com.baomidou.mybatisplus.annotation.EnumValue;
import lombok.NoArgsConstructor;

@NoArgsConstructor
public enum GradeEnum {

    PRIMARY(1, "小学"),  SECONDORY(2, "中学"),  HIGH(3, "高中");


    GradeEnum(int code, String descp) {
        this.code = code;
        this.descp = descp;
    }

    @EnumValue//标记数据库存的值是code
    private  int code;

    private  String descp;


    @Override
    public String toString() {
        return descp;
    }
}
~~~

DTO实体
- 在FastJson下。使用@JSONField(serialzeFeatures= SerializerFeature.WriteEnumUsingToString) 注解，在转json时将枚举翻译
~~~
package com.gbm.cloud.treasure.entity.myUser.vo;

import com.alibaba.fastjson.annotation.JSONField;
import com.alibaba.fastjson.serializer.SerializerFeature;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.springframework.format.annotation.DateTimeFormat;

import java.util.Date;

/**
 * @Description: 用户
 * @Author: jeecg-boot
 * @Date:   2021-10-28
 * @Version: V1.0
 */
@Data
@TableName("my_user")
@EqualsAndHashCode(callSuper = false)
@Accessors(chain = true)
public class TbMyUserDto {
    
	/**id*/
	@TableId(type = IdType.ASSIGN_ID)
	private Integer id;
	/**userName*/
	private String userName;
	/**passWord*/
	private String passWord;
	/**age*/
	private Integer age;
	/**createDate*/
	@JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd HH:mm:ss")
    @DateTimeFormat(pattern="yyyy-MM-dd HH:mm:ss")
	private Date createDate;


	/**
	 * 年级，原生枚举（带{@link com.baomidou.mybatisplus.annotation.EnumValue}):
	 * 数据库字段：grade INT(2)
	 */
	@JSONField(serialzeFeatures= SerializerFeature.WriteEnumUsingToString)
	private GradeEnum type;
}

~~~

fastjson使用
~~~
        List<TbMyUserDto> list = userServie.list(new LambdaQueryWrapper<TbMyUserDto>());
        System.out.println(list);
        System.out.println(JSON.toJSONString(list));

~~~
