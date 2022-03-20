---
title: spring-如何灵活的配置bean.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: spring-如何灵活的配置bean.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
### @ConditionalOnExpression注解，按条件选择是否注入
配置文件中，print.sql.log.enable的值为true时才会去配置这个Bean。

像一些调试功能如打印mybatis的真实sql，可以使用这种方式进行开关 
~~~
    @Bean
    @ConditionalOnExpression("#{'true'.equals(environment['print.sql.log.enable'])}")
    public SqlInterceptor myPlugin() {
        return new SqlInterceptor();
    }
~~~

###直接在类上使用@Component类似的注解 和在配置类上使用 @Bean进行配置是可以相互替代的
如果要灵活的配置Bean，就使用@Bean的方式，当然使用@Component等扫描注解是最方便的！
