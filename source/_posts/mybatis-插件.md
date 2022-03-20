---
title: mybatis-插件.md
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
title: mybatis-插件.md
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
###打印完整sql
~~~
package org.szwj.ca.identityauthsrv;

import org.apache.commons.lang3.StringUtils;
import org.apache.ibatis.cache.CacheKey;
import org.apache.ibatis.executor.Executor;
import org.apache.ibatis.mapping.BoundSql;
import org.apache.ibatis.mapping.MappedStatement;
import org.apache.ibatis.mapping.ParameterMapping;
import org.apache.ibatis.mapping.ParameterMode;
import org.apache.ibatis.plugin.*;
import org.apache.ibatis.reflection.MetaObject;
import org.apache.ibatis.session.Configuration;
import org.apache.ibatis.session.ResultHandler;
import org.apache.ibatis.session.RowBounds;
import org.apache.ibatis.type.TypeHandlerRegistry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Properties;

/**
 * 打印sql
 *
 * @date 2019/1/14 20:13
 */
@Component
@Profile({"dev", "test"})
@Intercepts({
        @Signature(type = Executor.class, method = "query", args = {MappedStatement.class, Object.class, RowBounds.class, ResultHandler.class}),
        @Signature(type = Executor.class, method = "query", args = {MappedStatement.class, Object.class, RowBounds.class, ResultHandler.class, CacheKey.class, BoundSql.class}),
        @Signature(type = Executor.class, method = "update", args = {MappedStatement.class, Object.class})}
)
public class SqlInterceptor implements Interceptor {
    private static ThreadLocal<SimpleDateFormat> dateTimeFormatter = new ThreadLocal<SimpleDateFormat>() {
        @Override
        protected SimpleDateFormat initialValue() {
            return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        }
    };

    @Override
    public Object intercept(Invocation invocation) throws Throwable {

        Object result = null;
        //捕获掉异常，不要影响业务
        try {
            MappedStatement mappedStatement = (MappedStatement) invocation.getArgs()[0];
            Object parameter = null;
            if (invocation.getArgs().length > 1) {
                parameter = invocation.getArgs()[1];
            }
            String sqlId = mappedStatement.getId();
            BoundSql boundSql = mappedStatement.getBoundSql(parameter);
            Configuration configuration = mappedStatement.getConfiguration();

            long startTime = System.currentTimeMillis();

            try {
                result = invocation.proceed();
            } finally {
                long endTime = System.currentTimeMillis();
                long sqlCostTime = endTime - startTime;
                String sql = this.getSql(configuration, boundSql);
                this.formatSqlLog(sqlId, sql, sqlCostTime, result);
            }
            return result;

        } catch (Exception e) {
            return result;
        }
    }

    @Override
    public Object plugin(Object target) {
        if (target instanceof Executor) {
            return Plugin.wrap(target, this);
        }
        return target;
    }

    @Override
    public void setProperties(Properties properties) {
    }

    /**
     * 获取完整的sql语句
     *
     * @param configuration
     * @param boundSql
     * @return
     */
    private String getSql(Configuration configuration, BoundSql boundSql) {
        // 输入sql字符串空判断
        String sql = boundSql.getSql();
        if (StringUtils.isEmpty(sql)) {
            return "";
        }
        return formatSql(sql, configuration, boundSql);
    }

    /**
     * 将占位符替换成参数值
     *
     * @param sql
     * @param configuration
     * @param boundSql
     * @return
     */
    private String formatSql(String sql, Configuration configuration, BoundSql boundSql) {

        //美化sql
        sql = beautifySql(sql);

        //填充占位符, 目前基本不用mybatis存储过程调用,故此处不做考虑
        Object parameterObject = boundSql.getParameterObject();
        List<ParameterMapping> parameterMappings = boundSql.getParameterMappings();
        TypeHandlerRegistry typeHandlerRegistry = configuration.getTypeHandlerRegistry();

        List<String> parameters = new ArrayList<>();
        if (parameterMappings != null) {
            MetaObject metaObject = parameterObject == null ? null : configuration.newMetaObject(parameterObject);
            for (int i = 0; i < parameterMappings.size(); i++) {
                ParameterMapping parameterMapping = parameterMappings.get(i);
                if (parameterMapping.getMode() != ParameterMode.OUT) {
                    //  参数值
                    Object value;
                    String propertyName = parameterMapping.getProperty();
                    //  获取参数名称
                    if (boundSql.hasAdditionalParameter(propertyName)) {
                        // 获取参数值
                        value = boundSql.getAdditionalParameter(propertyName);
                    } else if (parameterObject == null) {
                        value = null;
                    } else if (typeHandlerRegistry.hasTypeHandler(parameterObject.getClass())) {
                        // 如果是单个值则直接赋值
                        value = parameterObject;
                    } else {
                        value = metaObject == null ? null : metaObject.getValue(propertyName);
                    }

                    if (value instanceof Number) {
                        parameters.add(String.valueOf(value));
                    } else {
                        StringBuilder builder = new StringBuilder();
                        builder.append("'");
                        if (value instanceof Date) {
                            builder.append(dateTimeFormatter.get().format((Date) value));
                        } else if (value instanceof String) {
                            builder.append(value);
                        }
                        builder.append("'");
                        parameters.add(builder.toString());
                    }
                }
            }
        }

        for (String value : parameters) {
            sql = sql.replaceFirst("\\?", value);
        }
        return sql;
    }


    /**
     * 格式化sql日志
     *
     * @param sqlId
     * @param sql
     * @param costTime
     * @return
     */
    private void formatSqlLog(String sqlId, String sql, long costTime, Object obj) {
        String sqlLog = "==> " + sql;
        StringBuffer result = new StringBuffer();
        if (obj instanceof List) {
            List list = (List) obj;
            int count = list.size();
            result.append("<==      Total: " + count);
        } else if (obj instanceof Integer) {
            result.append("<==      Total: " + obj);
        }

        result.append("      Spend Time ==> " + costTime + " ms");
        Logger log = LoggerFactory.getLogger(sqlId);
        log.info(sqlLog);
        log.info(result.toString());
    }


    public static String beautifySql(String sql) {
        sql = sql.replaceAll("[\\s\n ]+", " ");
        return sql;
    }
}


~~~

注册

~~~
package org.szwj.ca.identityauthsrv;

import java.io.File;

import java.util.ArrayList;
import java.util.List;
import org.springframework.http.MediaType;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
import org.szwj.ca.identityauthsrv.config.Config;

import com.alibaba.fastjson.serializer.SerializerFeature;
import com.alibaba.fastjson.support.config.FastJsonConfig;
import com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter;
import org.apache.catalina.connector.Connector;
import org.apache.coyote.http11.Http11NioProtocol;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.web.HttpMessageConverters;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.embedded.EmbeddedServletContainerFactory;
import org.springframework.boot.context.embedded.tomcat.TomcatEmbeddedServletContainerFactory;
import org.springframework.boot.web.servlet.ServletComponentScan;
import org.springframework.context.annotation.Bean;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
@MapperScan(basePackages = "org.szwj.ca.identityauthsrv.dao")
@ServletComponentScan
public class IdentityauthsrvApplication extends WebMvcConfigurerAdapter {

    @Value("${https.enable}")
    private Boolean enable;

    @Value("${https.port}")
    private Integer port;

    @Value("${https.ssl.key-store}")
    private String keyStore;

    @Value("${https.ssl.key-store-password}")
    private String keyStorePassword;

    @Value("${https.ssl.key-password}")
    private String keyPassword;

    @Bean
    public EmbeddedServletContainerFactory servletContainer() {
        TomcatEmbeddedServletContainerFactory tomcat = new TomcatEmbeddedServletContainerFactory();
        if (enable) {
            tomcat.addAdditionalTomcatConnectors(createStandardConnector());
        }
        return tomcat;
    }

    private Connector createStandardConnector() {
        Connector connector = new Connector("org.apache.coyote.http11.Http11NioProtocol");
        Http11NioProtocol protocol = (Http11NioProtocol) connector.getProtocolHandler();
        File keystore = new File(System.getProperty("user.dir") + keyStore);
        connector.setScheme("https");
        connector.setSecure(true);
        connector.setPort(port);
        protocol.setSSLEnabled(true);
        protocol.setKeystoreFile(keystore.getAbsolutePath());
        protocol.setKeystorePass(keyStorePassword);
        protocol.setKeyPass(keyPassword);
        return connector;
    }

//    @Bean
//    public HttpMessageConverters fastJsonHttpMessageConverters() {
//        FastJsonHttpMessageConverter fastJsonHttpMessageConverter = new FastJsonHttpMessageConverter();
//        FastJsonConfig fastJsonConfig = new FastJsonConfig();
//        fastJsonConfig.setSerializerFeatures(SerializerFeature.WriteMapNullValue,
//            SerializerFeature.WriteNullListAsEmpty);
//        fastJsonHttpMessageConverter.setFastJsonConfig(fastJsonConfig);
//
//        // 处理中文乱码问题
//        List<MediaType> fastMediaTypes = new ArrayList<>();
//        fastMediaTypes.add(MediaType.APPLICATION_JSON_UTF8);
//        fastJsonHttpMessageConverter.setSupportedMediaTypes(fastMediaTypes);
//
//        HttpMessageConverter<?> converter = fastJsonHttpMessageConverter;
//        return new HttpMessageConverters(converter);
//    }


    //注册插件
    @Bean
    public SqlInterceptor myPlugin() {
        SqlInterceptor myPlugin = new SqlInterceptor();
        return myPlugin;
    }

    public static void main(String[] args) throws Exception {
        SpringApplication.run(IdentityauthsrvApplication.class, args);
        if (Config.GetInstance().getWebSocketEnabled()) {
            new NettyServer(Config.GetInstance().getWebSocketPort()).start();
        }
    }
}

~~~


###mybatis cache plugin

~~~
谢邀，确实至少在mybatis 3上存在一级缓存脏数据的问题，不知题主用的是不是这个版本。

可以认为原生的mybatis不是为多线程环境准备的，包括它二级缓存的一些特性都像是为开发桌面软件而存在。但这个脏数据问题通过插件可以解决。可以在网上找找mybatis cache plugin。

我自己也有这样的插件，不过和其他插件一起整合了，代码都放在 [limeng32/mybatisPlugin](https://link.zhihu.com/?target=https%3A//github.com/limeng32/mybatisPlugin) 上，但没有文档，之后有时间再说。

对了一般在多线程环境下mybatis的配置文件中这几项要这样配：
~~~
<setting name="lazyLoadingEnabled" value="false" />
<setting name="aggressiveLazyLoading" value="false" />
<setting name="localCacheScope" value="SESSION" />
~~~
~~~
