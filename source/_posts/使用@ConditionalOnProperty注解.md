---
title: 使用@ConditionalOnProperty注解.md
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
title: 使用@ConditionalOnProperty注解.md
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
###1. spring boot ConditionalOnProperty 使用讲解

@Retention(RetentionPolicy.RUNTIME)  
@Target({ElementType.TYPE, ElementType.METHOD})  
@Documented  
@Conditional({OnPropertyCondition.class})  
public @interface ConditionalOnProperty {  
    String[] value() default {}; //数组，获取对应property名称的值，与name不可同时使用  

    String prefix() default "";//property名称的前缀，可有可无  

    String[] name() default {};//数组，property完整名称或部分名称（可与prefix组合使用，组成完整的property名称），与value不可同时使用  

    String havingValue() default "";//可与name组合使用，比较获取到的属性值与havingValue给定的值是否相同，相同才加载配置  

    boolean matchIfMissing() default false;//缺少该property时是否可以加载。如果为true，没有该property也会正常加载；反之报错  

    boolean relaxedNames() default true;//是否可以松散匹配
}  

###操作案例
**案例1： 值必须匹配为123 才会有效**
注意 ： prefix 可以不用， 但是要写全部在name 上
@ConditionalOnProperty(prefix = "parentName",name = "sonName",havingValue = "123")  
.yml配置如下：  
parentName:  
      sonName: 123      //正常    
parentName:  
      sonName: 1234     //失败，与havingValue给定的值不一致  



**案例2： 值必须匹配为123 才会有效， 并且可以yml 或者 properties 文件中不设置这个属性， 因为matchIfMissing 为true**
@ConditionalOnProperty(prefix = "parentName",name = "sonName",havingValue = "123",matchIfMissing = true)  
// .yml配置如下：     
//不配置相关参数       //正常，当matchIfMissing = true时，即使没有该parentName.sonName属性也会加载正常 

**案例3： 配置多个属性值， 并且属性值都是一样的情况下才有效**
注意： 可以使用在判断两个配置属性都为为某个值的情况下使用， 比较方便,
parentName.sonName和parentName.flag的值都要与havingValue的一致才行
@ConditionalOnProperty(prefix = "parentName", name = {"sonName", "flag"}, havingValue = "123")
parentName:  
      sonName: 123  
      flag: 1234       //失败     
parentName:  
    sonName: 123  
    flag: 123        //正常  
parentName:  
    sonName: 123     //失败，缺少parentName.flag  



**案例4： 配置多个属性值， 并且属性值都是一样的情况下才有效, 其中设置 matchIfMissing = true， 允许不在配置文件中出现**
@ConditionalOnProperty(prefix = "parentName", name = {"sonName", "flag"}, havingValue = "123",matchIfMissing = true)
parentName:  
    sonName: 123     //正常     

// .yml配置如下：      




@ConditionalOnProperty(name = "spring.datasource.druid.statViewServlet.enabled", havingValue = "true")



