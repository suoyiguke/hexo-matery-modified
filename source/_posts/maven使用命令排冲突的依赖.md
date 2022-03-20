---
title: maven使用命令排冲突的依赖.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: maven
categories: maven
---
---
title: maven使用命令排冲突的依赖.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: maven
categories: maven
---


SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/C:/Users/yinkai/.m2/repository/ch/qos/logback/logback-classic/1.2.3/logback-classic-1.2.3.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/C:/Users/yinkai/.m2/repository/org/slf4j/slf4j-simple/1.7.30/slf4j-simple-1.7.30.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [ch.qos.logback.classic.util.ContextSelectorStaticBinder]
Disconnected from the target VM, address: '127.0.0.1:51413', transport: 'socket'

命令：
~~~
mvn dependency:tree
~~~

~~~


B at 95 kB/s)
[INFO] com.gbm.cloud:mgb_treasure_system:jar:0.0.1-SNAPSHOT
[INFO] +- org.springframework.boot:spring-boot-starter:jar:2.3.0.RELEASE:compile
[INFO] |  +- org.springframework.boot:spring-boot:jar:2.3.0.RELEASE:compile
[INFO] |  |  \- org.springframework:spring-context:jar:5.2.6.RELEASE:compile
[INFO] |  +- org.springframework.boot:spring-boot-autoconfigure:jar:2.3.0.RELEASE:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-logging:jar:2.3.0.RELEASE:compile
[INFO] |  |  +- ch.qos.logback:logback-classic:jar:1.2.3:compile
[INFO] |  |  |  \- ch.qos.logback:logback-core:jar:1.2.3:compile
[INFO] |  |  +- org.apache.logging.log4j:log4j-to-slf4j:jar:2.13.2:compile
[INFO] |  |  \- org.slf4j:jul-to-slf4j:jar:1.7.30:compile
[INFO] |  +- jakarta.annotation:jakarta.annotation-api:jar:1.3.5:compile
[INFO] |  +- org.springframework:spring-core:jar:5.2.6.RELEASE:compile
[INFO] |  |  \- org.springframework:spring-jcl:jar:5.2.6.RELEASE:compile
[INFO] |  \- org.yaml:snakeyaml:jar:1.26:compile
[INFO] +- org.springframework.boot:spring-boot-starter-test:jar:2.3.0.RELEASE:test
[INFO] |  +- org.springframework.boot:spring-boot-test:jar:2.3.0.RELEASE:test
[INFO] |  +- org.springframework.boot:spring-boot-test-autoconfigure:jar:2.3.0.RELEASE:test
[INFO] |  +- com.jayway.jsonpath:json-path:jar:2.4.0:test
[INFO] |  |  \- net.minidev:json-smart:jar:2.3:test
[INFO] |  |     \- net.minidev:accessors-smart:jar:1.2:test
[INFO] |  +- jakarta.xml.bind:jakarta.xml.bind-api:jar:2.3.3:compile
[INFO] |  |  \- jakarta.activation:jakarta.activation-api:jar:1.2.2:compile
[INFO] |  +- org.assertj:assertj-core:jar:3.16.1:test
[INFO] |  +- org.hamcrest:hamcrest:jar:2.2:test
[INFO] |  +- org.junit.jupiter:junit-jupiter:jar:5.6.2:test
[INFO] |  |  +- org.junit.jupiter:junit-jupiter-api:jar:5.6.2:test
[INFO] |  |  |  +- org.apiguardian:apiguardian-api:jar:1.1.0:test
[INFO] |  |  |  +- org.opentest4j:opentest4j:jar:1.2.0:test
[INFO] |  |  |  \- org.junit.platform:junit-platform-commons:jar:1.6.2:test
[INFO] |  |  +- org.junit.jupiter:junit-jupiter-params:jar:5.6.2:test
[INFO] |  |  \- org.junit.jupiter:junit-jupiter-engine:jar:5.6.2:test
[INFO] |  |     \- org.junit.platform:junit-platform-engine:jar:1.6.2:test
[INFO] |  +- org.mockito:mockito-core:jar:3.3.3:test
[INFO] |  |  +- net.bytebuddy:byte-buddy:jar:1.10.10:test
[INFO] |  |  +- net.bytebuddy:byte-buddy-agent:jar:1.10.10:test
[INFO] |  |  \- org.objenesis:objenesis:jar:2.6:test
[INFO] |  +- org.mockito:mockito-junit-jupiter:jar:3.3.3:test
[INFO] |  +- org.skyscreamer:jsonassert:jar:1.5.0:test
[INFO] |  |  \- com.vaadin.external.google:android-json:jar:0.0.20131108.vaadin1:test
[INFO] |  +- org.springframework:spring-test:jar:5.2.6.RELEASE:test
[INFO] |  \- org.xmlunit:xmlunit-core:jar:2.7.0:test
[INFO] +- org.springframework.boot:spring-boot-starter-web:jar:2.3.0.RELEASE:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-json:jar:2.3.0.RELEASE:compile
[INFO] |  |  +- com.fasterxml.jackson.core:jackson-databind:jar:2.11.0:compile
[INFO] |  |  +- com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.11.0:compile
[INFO] |  |  +- com.fasterxml.jackson.datatype:jackson-datatype-jsr310:jar:2.11.0:compile
[INFO] |  |  \- com.fasterxml.jackson.module:jackson-module-parameter-names:jar:2.11.0:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-tomcat:jar:2.3.0.RELEASE:compile
[INFO] |  |  +- org.apache.tomcat.embed:tomcat-embed-core:jar:9.0.35:compile
[INFO] |  |  \- org.apache.tomcat.embed:tomcat-embed-websocket:jar:9.0.35:compile
[INFO] |  +- org.springframework:spring-web:jar:5.2.6.RELEASE:compile
[INFO] |  |  \- org.springframework:spring-beans:jar:5.2.6.RELEASE:compile
[INFO] |  \- org.springframework:spring-webmvc:jar:5.2.6.RELEASE:compile
[INFO] |     +- org.springframework:spring-aop:jar:5.2.6.RELEASE:compile
[INFO] |     \- org.springframework:spring-expression:jar:5.2.6.RELEASE:compile
[INFO] +- org.mybatis.spring.boot:mybatis-spring-boot-starter:jar:2.1.2:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-jdbc:jar:2.3.0.RELEASE:compile
[INFO] |  |  +- com.zaxxer:HikariCP:jar:3.4.5:compile
[INFO] |  |  \- org.springframework:spring-jdbc:jar:5.2.6.RELEASE:compile
[INFO] |  +- org.mybatis.spring.boot:mybatis-spring-boot-autoconfigure:jar:2.1.2:compile
[INFO] |  +- org.mybatis:mybatis:jar:3.5.4:compile
[INFO] |  \- org.mybatis:mybatis-spring:jar:2.0.4:compile
[INFO] +- org.springframework.cloud:spring-cloud-starter-netflix-eureka-client:jar:2.2.2.RELEASE:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-starter:jar:2.2.2.RELEASE:compile
[INFO] |  |  +- org.springframework.cloud:spring-cloud-context:jar:2.2.2.RELEASE:compile
[INFO] |  |  \- org.springframework.security:spring-security-rsa:jar:1.0.9.RELEASE:compile
[INFO] |  |     \- org.bouncycastle:bcpkix-jdk15on:jar:1.64:compile
[INFO] |  |        \- org.bouncycastle:bcprov-jdk15on:jar:1.64:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-netflix-hystrix:jar:2.2.2.RELEASE:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-netflix-eureka-client:jar:2.2.2.RELEASE:compile
[INFO] |  +- com.netflix.eureka:eureka-client:jar:1.9.17:compile
[INFO] |  |  +- org.codehaus.jettison:jettison:jar:1.3.7:runtime
[INFO] |  |  |  \- stax:stax-api:jar:1.0.1:compile
[INFO] |  |  +- com.netflix.netflix-commons:netflix-eventbus:jar:0.3.0:runtime
[INFO] |  |  |  +- com.netflix.netflix-commons:netflix-infix:jar:0.3.0:runtime
[INFO] |  |  |  |  +- commons-jxpath:commons-jxpath:jar:1.3:runtime
[INFO] |  |  |  |  +- org.antlr:antlr-runtime:jar:3.4:runtime
[INFO] |  |  |  |  |  +- org.antlr:stringtemplate:jar:3.2.1:runtime
[INFO] |  |  |  |  |  \- antlr:antlr:jar:2.7.7:runtime
[INFO] |  |  |  |  \- com.google.code.gson:gson:jar:2.8.6:runtime
[INFO] |  |  |  \- org.apache.commons:commons-math:jar:2.2:runtime
[INFO] |  |  +- com.netflix.archaius:archaius-core:jar:0.7.6:compile
[INFO] |  |  +- javax.ws.rs:jsr311-api:jar:1.1.1:runtime
[INFO] |  |  +- com.netflix.servo:servo-core:jar:0.12.21:runtime
[INFO] |  |  +- com.sun.jersey:jersey-core:jar:1.19.1:runtime
[INFO] |  |  +- com.sun.jersey:jersey-client:jar:1.19.1:runtime
[INFO] |  |  +- com.sun.jersey.contribs:jersey-apache-client4:jar:1.19.1:runtime
[INFO] |  |  +- com.google.inject:guice:jar:4.1.0:runtime
[INFO] |  |  |  +- javax.inject:javax.inject:jar:1:runtime
[INFO] |  |  |  \- aopalliance:aopalliance:jar:1.0:compile
[INFO] |  |  +- com.fasterxml.jackson.core:jackson-annotations:jar:2.11.0:compile
[INFO] |  |  \- com.fasterxml.jackson.core:jackson-core:jar:2.11.0:compile
[INFO] |  +- com.netflix.eureka:eureka-core:jar:1.9.17:compile
[INFO] |  |  \- com.fasterxml.woodstox:woodstox-core:jar:5.2.1:runtime
[INFO] |  |     \- org.codehaus.woodstox:stax2-api:jar:4.2:runtime
[INFO] |  +- org.springframework.cloud:spring-cloud-starter-netflix-archaius:jar:2.2.2.RELEASE:compile
[INFO] |  |  +- org.springframework.cloud:spring-cloud-netflix-ribbon:jar:2.2.2.RELEASE:compile
[INFO] |  |  +- org.springframework.cloud:spring-cloud-netflix-archaius:jar:2.2.2.RELEASE:compile
[INFO] |  |  \- commons-configuration:commons-configuration:jar:1.8:compile
[INFO] |  |     \- commons-lang:commons-lang:jar:2.6:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-starter-netflix-ribbon:jar:2.2.2.RELEASE:compile
[INFO] |  |  +- com.netflix.ribbon:ribbon:jar:2.3.0:compile
[INFO] |  |  |  +- com.netflix.ribbon:ribbon-transport:jar:2.3.0:runtime
[INFO] |  |  |  |  +- io.reactivex:rxnetty-contexts:jar:0.4.9:runtime
[INFO] |  |  |  |  \- io.reactivex:rxnetty-servo:jar:0.4.9:runtime
[INFO] |  |  |  \- io.reactivex:rxnetty:jar:0.4.9:runtime
[INFO] |  |  +- com.netflix.ribbon:ribbon-core:jar:2.3.0:compile
[INFO] |  |  +- com.netflix.ribbon:ribbon-httpclient:jar:2.3.0:compile
[INFO] |  |  |  +- commons-collections:commons-collections:jar:3.2.2:runtime
[INFO] |  |  |  \- com.netflix.netflix-commons:netflix-commons-util:jar:0.3.0:runtime
[INFO] |  |  +- com.netflix.ribbon:ribbon-loadbalancer:jar:2.3.0:compile
[INFO] |  |  |  \- com.netflix.netflix-commons:netflix-statistics:jar:0.1.1:runtime
[INFO] |  |  \- io.reactivex:rxjava:jar:1.3.8:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-starter-loadbalancer:jar:2.2.2.RELEASE:compile
[INFO] |  |  +- org.springframework.cloud:spring-cloud-loadbalancer:jar:2.2.2.RELEASE:compile
[INFO] |  |  |  \- io.projectreactor.addons:reactor-extra:jar:3.3.3.RELEASE:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-starter-cache:jar:2.3.0.RELEASE:compile
[INFO] |  |  \- com.stoyanr:evictor:jar:1.0.0:compile
[INFO] |  +- com.netflix.ribbon:ribbon-eureka:jar:2.3.0:compile
[INFO] |  \- com.thoughtworks.xstream:xstream:jar:1.4.11.1:compile
[INFO] |     +- xmlpull:xmlpull:jar:1.1.3.1:compile
[INFO] |     \- xpp3:xpp3_min:jar:1.1.4c:compile
[INFO] +- org.springframework.cloud:spring-cloud-starter-oauth2:jar:2.2.1.RELEASE:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-starter-security:jar:2.2.1.RELEASE:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-starter-actuator:jar:2.3.0.RELEASE:compile
[INFO] |  |  |  +- org.springframework.boot:spring-boot-actuator-autoconfigure:jar:2.3.0.RELEASE:compile
[INFO] |  |  |  |  \- org.springframework.boot:spring-boot-actuator:jar:2.3.0.RELEASE:compile
[INFO] |  |  |  \- io.micrometer:micrometer-core:jar:1.5.1:compile
[INFO] |  |  |     \- org.latencyutils:LatencyUtils:jar:2.0.3:runtime
[INFO] |  |  \- org.springframework.cloud:spring-cloud-security:jar:2.2.1.RELEASE:compile
[INFO] |  |     \- org.springframework.boot:spring-boot-starter-security:jar:2.3.0.RELEASE:compile
[INFO] |  \- org.springframework.security.oauth.boot:spring-security-oauth2-autoconfigure:jar:2.1.2.RELEASE:compile
[INFO] |     +- com.sun.xml.bind:jaxb-core:jar:2.3.0.1:compile
[INFO] |     +- com.sun.xml.bind:jaxb-impl:jar:2.3.0.1:compile
[INFO] |     +- javax.xml.bind:jaxb-api:jar:2.3.1:compile
[INFO] |     |  \- javax.activation:javax.activation-api:jar:1.2.0:compile
[INFO] |     +- org.springframework.security.oauth:spring-security-oauth2:jar:2.3.4.RELEASE:compile
[INFO] |     |  +- org.springframework.security:spring-security-core:jar:5.3.2.RELEASE:compile
[INFO] |     |  +- org.springframework.security:spring-security-config:jar:5.3.2.RELEASE:compile
[INFO] |     |  +- org.springframework.security:spring-security-web:jar:5.3.2.RELEASE:compile
[INFO] |     |  \- org.codehaus.jackson:jackson-mapper-asl:jar:1.9.13:compile
[INFO] |     |     \- org.codehaus.jackson:jackson-core-asl:jar:1.9.13:compile
[INFO] |     \- org.springframework.security:spring-security-jwt:jar:1.0.9.RELEASE:compile
[INFO] +- mysql:mysql-connector-java:jar:8.0.20:runtime
[INFO] +- com.baomidou:mybatis-plus-boot-starter:jar:3.3.2:compile
[INFO] |  \- com.baomidou:mybatis-plus:jar:3.3.2:compile
[INFO] |     \- com.baomidou:mybatis-plus-extension:jar:3.3.2:compile
[INFO] |        \- com.baomidou:mybatis-plus-core:jar:3.3.2:compile
[INFO] |           \- com.baomidou:mybatis-plus-annotation:jar:3.3.2:compile
[INFO] +- org.projectlombok:lombok:jar:1.18.12:compile (optional)
[INFO] +- com.alibaba:fastjson:jar:1.2.75:compile
[INFO] +- com.github.pagehelper:pagehelper-spring-boot-starter:jar:1.2.12:compile
[INFO] |  +- com.github.pagehelper:pagehelper-spring-boot-autoconfigure:jar:1.2.12:compile
[INFO] |  \- com.github.pagehelper:pagehelper:jar:5.1.10:compile
[INFO] |     \- com.github.jsqlparser:jsqlparser:jar:2.0:compile
[INFO] +- org.springframework.boot:spring-boot-starter-validation:jar:2.3.0.RELEASE:compile
[INFO] |  +- org.glassfish:jakarta.el:jar:3.0.3:compile
[INFO] |  \- org.hibernate.validator:hibernate-validator:jar:6.1.5.Final:compile
[INFO] |     +- jakarta.validation:jakarta.validation-api:jar:2.0.2:compile
[INFO] |     +- org.jboss.logging:jboss-logging:jar:3.4.1.Final:compile
[INFO] |     \- com.fasterxml:classmate:jar:1.5.1:compile
[INFO] +- com.alibaba:druid-spring-boot-starter:jar:1.1.18:compile
[INFO] |  +- com.alibaba:druid:jar:1.1.18:compile
[INFO] |  \- org.slf4j:slf4j-api:jar:1.7.30:compile
[INFO] +- org.springframework.boot:spring-boot-starter-data-redis:jar:2.3.0.RELEASE:compile
[INFO] |  +- org.springframework.data:spring-data-redis:jar:2.3.0.RELEASE:compile
[INFO] |  |  +- org.springframework.data:spring-data-keyvalue:jar:2.3.0.RELEASE:compile
[INFO] |  |  +- org.springframework:spring-tx:jar:5.2.6.RELEASE:compile
[INFO] |  |  +- org.springframework:spring-oxm:jar:5.2.6.RELEASE:compile
[INFO] |  |  \- org.springframework:spring-context-support:jar:5.2.6.RELEASE:compile
[INFO] |  \- io.lettuce:lettuce-core:jar:5.3.0.RELEASE:compile
[INFO] |     +- io.netty:netty-common:jar:4.1.49.Final:compile
[INFO] |     +- io.netty:netty-handler:jar:4.1.49.Final:compile
[INFO] |     |  +- io.netty:netty-resolver:jar:4.1.49.Final:compile
[INFO] |     |  +- io.netty:netty-buffer:jar:4.1.49.Final:compile
[INFO] |     |  \- io.netty:netty-codec:jar:4.1.49.Final:compile
[INFO] |     +- io.netty:netty-transport:jar:4.1.49.Final:compile
[INFO] |     \- io.projectreactor:reactor-core:jar:3.3.5.RELEASE:compile
[INFO] |        \- org.reactivestreams:reactive-streams:jar:1.0.3:compile
[INFO] +- com.squareup.okhttp3:okhttp:jar:3.3.0:compile
[INFO] |  \- com.squareup.okio:okio:jar:1.8.0:compile
[INFO] +- com.alibaba:easyexcel:jar:2.2.3:compile
[INFO] |  +- org.apache.poi:poi:jar:3.17:compile
[INFO] |  |  \- org.apache.commons:commons-collections4:jar:4.1:compile
[INFO] |  +- org.apache.poi:poi-ooxml:jar:3.17:compile
[INFO] |  |  \- com.github.virtuald:curvesapi:jar:1.04:compile
[INFO] |  +- org.apache.poi:poi-ooxml-schemas:jar:3.17:compile
[INFO] |  |  \- org.apache.xmlbeans:xmlbeans:jar:2.6.0:compile
[INFO] |  +- cglib:cglib:jar:3.1:compile
[INFO] |  |  \- org.ow2.asm:asm:jar:4.2:compile
[INFO] |  \- org.ehcache:ehcache:jar:3.8.1:compile
[INFO] |     \- org.glassfish.jaxb:jaxb-runtime:jar:2.3.3:compile
[INFO] |        +- org.glassfish.jaxb:txw2:jar:2.3.3:compile
[INFO] |        +- com.sun.istack:istack-commons-runtime:jar:3.0.11:compile
[INFO] |        \- com.sun.activation:jakarta.activation:jar:1.2.2:runtime
[INFO] +- org.springframework.boot:spring-boot-configuration-processor:jar:2.3.0.RELEASE:compile (optional)
[INFO] +- org.springframework.cloud:spring-cloud-starter-openfeign:jar:2.2.2.RELEASE:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-openfeign-core:jar:2.2.2.RELEASE:compile
[INFO] |  |  \- io.github.openfeign.form:feign-form-spring:jar:3.8.0:compile
[INFO] |  |     +- io.github.openfeign.form:feign-form:jar:3.8.0:compile
[INFO] |  |     \- commons-fileupload:commons-fileupload:jar:1.4:compile
[INFO] |  |        \- commons-io:commons-io:jar:2.2:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-commons:jar:2.2.2.RELEASE:compile
[INFO] |  |  \- org.springframework.security:spring-security-crypto:jar:5.3.2.RELEASE:compile
[INFO] |  +- io.github.openfeign:feign-core:jar:10.7.4:compile
[INFO] |  +- io.github.openfeign:feign-slf4j:jar:10.7.4:compile
[INFO] |  \- io.github.openfeign:feign-hystrix:jar:10.7.4:compile
[INFO] |     \- com.netflix.hystrix:hystrix-core:jar:1.5.18:compile
[INFO] +- org.springframework.cloud:spring-cloud-starter-zipkin:jar:2.2.2.RELEASE:compile
[INFO] |  +- org.springframework.cloud:spring-cloud-starter-sleuth:jar:2.2.2.RELEASE:compile
[INFO] |  |  \- org.springframework.cloud:spring-cloud-sleuth-core:jar:2.2.2.RELEASE:compile
[INFO] |  |     +- org.aspectj:aspectjrt:jar:1.9.5:compile
[INFO] |  |     +- io.zipkin.brave:brave:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-context-log4j2:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-messaging:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-rpc:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-spring-web:jar:5.10.1:compile
[INFO] |  |     |  \- io.zipkin.brave:brave-instrumentation-http:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-spring-rabbit:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-kafka-clients:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-kafka-streams:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-httpclient:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-httpasyncclient:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-spring-webmvc:jar:5.10.1:compile
[INFO] |  |     |  \- io.zipkin.brave:brave-instrumentation-servlet:jar:5.10.1:compile
[INFO] |  |     +- io.zipkin.brave:brave-instrumentation-jms:jar:5.10.1:compile
[INFO] |  |     \- io.zipkin.reporter2:zipkin-reporter-metrics-micrometer:jar:2.12.1:compile
[INFO] |  \- org.springframework.cloud:spring-cloud-sleuth-zipkin:jar:2.2.2.RELEASE:compile
[INFO] |     +- io.zipkin.zipkin2:zipkin:jar:2.19.3:compile
[INFO] |     +- io.zipkin.reporter2:zipkin-reporter:jar:2.12.1:compile
[INFO] |     +- io.zipkin.reporter2:zipkin-sender-kafka:jar:2.12.1:compile
[INFO] |     +- io.zipkin.reporter2:zipkin-sender-activemq-client:jar:2.12.1:compile
[INFO] |     \- io.zipkin.reporter2:zipkin-sender-amqp-client:jar:2.12.1:compile
[INFO] +- com.belerweb:pinyin4j:jar:2.5.1:compile
[INFO] +- com.aliyun:alibaba-dingtalk-service-sdk:jar:1.0.1:compile
[INFO] |  \- commons-logging:commons-logging:jar:1.1.1:compile
[INFO] +- com.alibaba.cloud:spring-cloud-starter-alibaba-seata:jar:2.2.3.RELEASE:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-aop:jar:2.3.0.RELEASE:compile
[INFO] |  |  \- org.aspectj:aspectjweaver:jar:1.9.5:compile
[INFO] |  \- io.seata:seata-spring-boot-starter:jar:1.3.0:compile
[INFO] |     \- io.seata:seata-all:jar:1.3.0:compile
[INFO] |        +- io.netty:netty-all:jar:4.1.49.Final:compile
[INFO] |        +- com.typesafe:config:jar:1.2.1:compile
[INFO] |        +- org.apache.commons:commons-pool2:jar:2.8.0:compile
[INFO] |        +- commons-pool:commons-pool:jar:1.6:compile
[INFO] |        +- com.google.protobuf:protobuf-java:jar:3.11.4:compile
[INFO] |        \- com.github.ben-manes.caffeine:caffeine:jar:2.8.2:compile
[INFO] |           \- org.checkerframework:checker-qual:jar:3.3.0:compile
[INFO] +- cn.hutool:hutool-core:jar:4.6.13:compile
[INFO] +- org.apache.httpcomponents:httpcore:jar:4.4:compile
[INFO] +- org.apache.httpcomponents:httpclient:jar:4.4:compile
[INFO] |  \- commons-codec:commons-codec:jar:1.14:compile
[INFO] +- commons-httpclient:commons-httpclient:jar:3.1:compile
[INFO] +- org.springframework.boot:spring-boot-starter-data-elasticsearch:jar:2.3.0.RELEASE:compile
[INFO] |  \- org.springframework.data:spring-data-elasticsearch:jar:4.0.0.RELEASE:compile
[INFO] |     +- org.springframework.data:spring-data-commons:jar:2.3.0.RELEASE:compile
[INFO] |     \- org.elasticsearch.plugin:transport-netty4-client:jar:7.6.2:compile
[INFO] |        \- io.netty:netty-codec-http:jar:4.1.49.Final:compile
[INFO] +- org.elasticsearch.client:elasticsearch-rest-high-level-client:jar:7.6.1:compile
[INFO] |  +- org.elasticsearch:elasticsearch:jar:7.6.2:compile
[INFO] |  |  +- org.elasticsearch:elasticsearch-core:jar:7.6.2:compile
[INFO] |  |  +- org.elasticsearch:elasticsearch-secure-sm:jar:7.6.2:compile
[INFO] |  |  +- org.elasticsearch:elasticsearch-x-content:jar:7.6.2:compile
[INFO] |  |  |  +- com.fasterxml.jackson.dataformat:jackson-dataformat-smile:jar:2.11.0:compile
[INFO] |  |  |  +- com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:jar:2.11.0:compile
[INFO] |  |  |  \- com.fasterxml.jackson.dataformat:jackson-dataformat-cbor:jar:2.11.0:compile
[INFO] |  |  +- org.elasticsearch:elasticsearch-geo:jar:7.6.2:compile
[INFO] |  |  +- org.apache.lucene:lucene-core:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-analyzers-common:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-backward-codecs:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-grouping:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-highlighter:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-join:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-memory:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-misc:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-queries:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-queryparser:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-sandbox:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-spatial:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-spatial-extras:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-spatial3d:jar:8.4.0:compile
[INFO] |  |  +- org.apache.lucene:lucene-suggest:jar:8.4.0:compile
[INFO] |  |  +- org.elasticsearch:elasticsearch-cli:jar:7.6.2:compile
[INFO] |  |  |  \- net.sf.jopt-simple:jopt-simple:jar:5.0.2:compile
[INFO] |  |  +- com.carrotsearch:hppc:jar:0.8.1:compile
[INFO] |  |  +- joda-time:joda-time:jar:2.10.4:compile
[INFO] |  |  +- com.tdunning:t-digest:jar:3.2:compile
[INFO] |  |  +- org.hdrhistogram:HdrHistogram:jar:2.1.9:compile
[INFO] |  |  +- org.apache.logging.log4j:log4j-api:jar:2.13.2:compile
[INFO] |  |  \- org.elasticsearch:jna:jar:4.5.1:compile
[INFO] |  +- org.elasticsearch.client:elasticsearch-rest-client:jar:7.6.2:compile
[INFO] |  |  +- org.apache.httpcomponents:httpasyncclient:jar:4.1.4:compile
[INFO] |  |  \- org.apache.httpcomponents:httpcore-nio:jar:4.4.13:compile
[INFO] |  +- org.elasticsearch.plugin:mapper-extras-client:jar:7.6.1:compile
[INFO] |  +- org.elasticsearch.plugin:parent-join-client:jar:7.6.1:compile
[INFO] |  +- org.elasticsearch.plugin:aggs-matrix-stats-client:jar:7.6.1:compile
[INFO] |  +- org.elasticsearch.plugin:rank-eval-client:jar:7.6.1:compile
[INFO] |  \- org.elasticsearch.plugin:lang-mustache-client:jar:7.6.1:compile
[INFO] |     \- com.github.spullara.mustache.java:compiler:jar:0.9.6:compile
[INFO] +- org.springframework.boot:spring-boot-starter-amqp:jar:2.3.0.RELEASE:compile
[INFO] |  +- org.springframework:spring-messaging:jar:5.2.6.RELEASE:compile
[INFO] |  \- org.springframework.amqp:spring-rabbit:jar:2.2.6.RELEASE:compile
[INFO] |     +- com.rabbitmq:amqp-client:jar:5.9.0:compile
[INFO] |     \- org.springframework.amqp:spring-amqp:jar:2.2.6.RELEASE:compile
[INFO] |        \- org.springframework.retry:spring-retry:jar:1.2.5.RELEASE:compile
[INFO] +- org.apache.commons:commons-compress:jar:1.8.1:compile
[INFO] +- org.mybatis.spring.boot:mybatis-spring-boot-starter-test:jar:1.3.2:test
[INFO] |  \- org.mybatis.spring.boot:mybatis-spring-boot-test-autoconfigure:jar:1.3.2:test
[INFO] +- junit:junit:jar:4.13:test
[INFO] |  \- org.hamcrest:hamcrest-core:jar:2.2:test
[INFO] \- com.baidu.aip:java-sdk:jar:4.16.2:compile
[INFO]    +- org.json:json:jar:20160810:compile
[INFO]    +- org.slf4j:slf4j-simple:jar:1.7.30:compile
[INFO]    \- com.google.guava:guava:jar:28.2-android:compile
[INFO]       +- com.google.guava:failureaccess:jar:1.0.1:compile
[INFO]       +- com.google.guava:listenablefuture:jar:9999.0-empty-to-avoid-conflict-with-guava:compile
[INFO]       +- com.google.code.findbugs:jsr305:jar:3.0.2:compile
[INFO]       +- org.checkerframework:checker-compat-qual:jar:2.5.5:compile
[INFO]       +- com.google.errorprone:error_prone_annotations:jar:2.3.4:compile
[INFO]       \- com.google.j2objc:j2objc-annotations:jar:1.3:compile
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  01:44 min
[INFO] Finished at: 2021-12-03T18:10:31+08:00
[INFO] ------------------------------------------------------------------------



~~~
