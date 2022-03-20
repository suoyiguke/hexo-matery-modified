---
title: 使用@ConditionalOnExpression注解按yml配置选择实例化Bean.md
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
title: 使用@ConditionalOnExpression注解按yml配置选择实例化Bean.md
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
@ConditionalOnExpression是springboot提供的非常好用的注解。
@ConditionalOnExpression("'true") 当括号中的内容为true时 ，使用该注解的类被实例化。

它可以和@Service、@Component、@Controller、@Repository 、@Bean 、@Configuration 等注解一起使用。可以通过`SPEL 表达式`、读取配置文件属性来让IOC容器选择性的扫描加入指定的某个Bean。而不是将所有实现类Bean都加入到IOC，这样会造成一定的资源浪费。简单来说就是`按需加载`,而不是`全部加载`。


###按yml配置来确定是否声明Bean
**加到Bean上**
~~~
    @Bean
    @ConditionalOnExpression("#{'true'.equals(environment['print.sql.log.enable'])}")
    public SqlInterceptor myPlugin() {
        return new SqlInterceptor();
    }
~~~

**直接加在@Configuration配置类，这样配置类下所有声明的bean都会受控制**
~~~
@Configuration
@ConditionalOnExpression("#{'true'.equals(environment['ias.prodxy.enabled'])}")
public class ProxyConfig {

~~~



###按yml配置选择实例化哪个Bean

比如我在一个serviceImpl类上加上如下注解,那么该类就会根据business.idCartOcr.choice的值是否等于“BAIDU”来决定是否进行创建Bean并加入IOC容器：
>@Service("BaiduUtilsServiceImpl")
@ConditionalOnExpression("'${business.idCartOcr.choice}'.equalsIgnoreCase('BAIDU')")


实现1
~~~
@Service("BaiduUtilsServiceImpl")
@ConditionalOnExpression("'${business.idCartOcr.choice}'.equalsIgnoreCase('BAIDU')")
public class BaiduUtilsServiceImpl implements AiService {
~~~

实现2
~~~
@Service("GdcaUtilsServiceImpl")
@ConditionalOnExpression("'${business.idCartOcr.choice}'.equalsIgnoreCase('GDCA')")
public class GdcaUtilsServiceImpl  implements AiService {

    @Override
    public void facePost(String image, String name, String idNo) {

    }

    @Override
    public IdCart ocrPost(String photoFront, String photoBack) {
        return null;
    }
}
~~~

因为AiService 只有一个实现类Bean是加入IOC的，所以 使用@Autowired按类型注入就行了。若有多个实现类Bean。那么使用@Resource 并填上BeanName参数来选择注入具体某个Bean。
~~~
    @Autowired
    private AiService aiService;
~~~


配置business.idCartOcr.choice=GDCA 时就只会自动实例化GdcaUtilsServiceImpl，反之配置business.idCartOcr.choice=BAIDU时就只实例化BaiduUtilsServiceImpl。


###@ConditionalOnExpression使用多个配置属性值

&&的关系
~~~
@ConditionalOnExpression("${properties.first.property.enable:true} && ${properties.second.property.startServer:false}")
~~~

还可以使用+连接
~~~
@ConditionalOnExpression("${properties.first.property.enable:true} " +
        "&& ${properties.second.property.enable:true} " +
        "&& ${properties.third.property.enable:true}")
~~~


equals的关系
~~~
@ConditionalOnExpression("'${com.property1}'.equals('${com.property2}')")
~~~

