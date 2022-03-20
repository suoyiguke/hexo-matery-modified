---
title: ssm-单元测试.md
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
title: ssm-单元测试.md
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
~~~
package com.sfpay.axg;

import com.sfpay.axg.dao.IOperatorInfoDao;
import com.sfpay.axg.domain.OperatorInfo;
import com.sfpay.axg.domain.criteria.OperatorInfoCriteria;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import javax.annotation.Resource;
import java.util.List;

/**
 *
 配置spring和junit整合，junit启动时加载springIOC容器
 */
@RunWith(SpringJUnit4ClassRunner.class)
//告诉junit spring配置文件
@ContextConfiguration("classpath:applicationContext-test1.xml")
public class baseTest {

    @Resource(name="operatorInfoDao")
    IOperatorInfoDao iOperatorInfoDao;

    @Test
    public void test() {
        System.out.println(iOperatorInfoDao);

        OperatorInfoCriteria operatorInfoCriteria = new OperatorInfoCriteria();
        operatorInfoCriteria.createCriteria();
        List<OperatorInfo> operatorInfos = iOperatorInfoDao.selectByCriteria(operatorInfoCriteria);

        for (OperatorInfo operatorInfo : operatorInfos) {
            System.out.println(operatorInfo);
        }

        System.out.println(12312);
    }
}

~~~


~~~
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:context="http://www.springframework.org/schema/context"
	   xmlns:tx="http://www.springframework.org/schema/tx" xmlns:aop="http://www.springframework.org/schema/aop"
	   xsi:schemaLocation="
		http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.1.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.1.xsd
		http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-3.1.xsd
		http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-3.1.xsd">

	<!-- 使用annotation 自动注册bean,并检查@Required,@Autowired的属性已被注入 -->
	<context:component-scan
			base-package="com.sfpay.axg.dao" />
	<!-- MyBatis配置 -->
	<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
		<property name="dataSource" ref="dataSource" />
		<!-- 自动扫描domain目录, 省掉Configuration.xml里的手工配置 -->
		<property name="typeAliasesPackage" value="com.sfpay.axg.domain" />
		<!-- 显式指定Mapper文件位置 -->
		<property name="mapperLocations" value="classpath:/mybatis/*Mapper.xml" />
	</bean>
	<!-- 扫描basePackage下所有以@MyBatisRepository标识的 接口 -->
	<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
		<property name="basePackage" value="com.sfpay.axg.dao" />
		<property name="annotationClass" value="org.springframework.stereotype.Repository" />
	</bean>

	<!-- 事务管理器配置, Jpa单数据源事务 -->
	<bean id="transactionManager"
		  class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource" />
		<property name="globalRollbackOnParticipationFailure" value="false" />
	</bean>
	<tx:annotation-driven transaction-manager="transactionManager" />

	<!-- 定义aspectj -->
	<aop:aspectj-autoproxy proxy-target-class="true" />

	<beans>

		<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource" destroy-method="close"  init-method="init" lazy-init="true">
			<property name="driverClassName" value="com.mysql.jdbc.Driver" />
			<property name="url" value="jdbc:mysql://192.168.0.223:3306/common_db_sd" />
			<property name="username" value="dev" />
			<property name="password" value="dev12345" />

		</bean>
	</beans>

</beans>
~~~
