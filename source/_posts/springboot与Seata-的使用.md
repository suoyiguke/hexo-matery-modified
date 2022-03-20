---
title: springboot与Seata-的使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 分布式事务
categories: 分布式事务
---
---
title: springboot与Seata-的使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 分布式事务
categories: 分布式事务
---
seata自身配置 file.conf
~~~

## transaction log store, only used in seata-server
store {
  ## store mode: file、db、redis
  mode = "db"

  ## file store property
  file {
    ## store location dir
    dir = "sessionStore"
    # branch session size , if exceeded first try compress lockkey, still exceeded throws exceptions
    maxBranchSessionSize = 16384
    # globe session size , if exceeded throws exceptions
    maxGlobalSessionSize = 512
    # file buffer size , if exceeded allocate new buffer
    fileWriteBufferCacheSize = 16384
    # when recover batch read size
    sessionReloadReadSize = 100
    # async, sync
    flushDiskMode = async
  }

  ## database store property
  db {
    ## the implement of javax.sql.DataSource, such as DruidDataSource(druid)/BasicDataSource(dbcp)/HikariDataSource(hikari) etc.
    datasource = "druid"
    ## mysql/oracle/postgresql/h2/oceanbase etc.
    dbType = "mysql"
    driverClassName = "com.mysql.cj.jdbc.Driver"
    url = "jdbc:mysql://192.168.1.57:3306/gbm_cloud_seata"
    user = "root"
    password = "XUNxiao123###"
    minConn = 5
    maxConn = 30
    globalTable = "global_table"
    branchTable = "branch_table"
    lockTable = "lock_table"
    queryLimit = 100
    maxWait = 5000
  }

  ## redis store property
  redis {
    host = "127.0.0.1"
    port = "6379"
    password = ""
    database = "0"
    minConn = 1
    maxConn = 10
    queryLimit = 100
  }

}
~~~

seata相关配置

~~~
seata:
  feign:
    enabled: false
  tx-service-group: fsp_tx_group #自定义名字保持统一
  service:
    vgroupMapping:
      fsp_tx_group: seata-server #默认default，这个是seate的名字，改了之后需要改服务端registry.conf 中eureka  application = "seata-server"，保持统一
  registry:
    type: eureka
    eureka:
      service-url: http://192.168.1.54:9000/eureka/
    weight: 1
  config:
    type: file

~~~


依赖
~~~
		<dependency>
			<groupId>com.alibaba.cloud</groupId>
			<artifactId>spring-cloud-starter-alibaba-seata</artifactId>
			<version>2.2.3.RELEASE</version>
		</dependency>
~~~

AT模式下每个业务数据库需要创建undo_log表，用于seata记录分支的回滚信息

表的地址：[https://github.com/seata/seata/blob/1.3.0/script/client/at/db/mysql.sql](https://github.com/seata/seata/blob/1.3.0/script/client/at/db/mysql.sql)



```
-- 注意此处0.3.0+ 增加唯一索引 ux_undo_log
CREATE TABLE `undo_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `branch_id` bigint(20) NOT NULL,
  `xid` varchar(100) NOT NULL,
  `context` varchar(128) NOT NULL,
  `rollback_info` longblob NOT NULL,
  `log_status` int(11) NOT NULL,
  `log_created` datetime NOT NULL,
  `log_modified` datetime NOT NULL,
  `ext` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ux_undo_log` (`xid`,`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```


@GlobalTransactional 注解开启分布式事务
~~~
    @Override
    @CacheEvict(value = "getSupplierBySupplierNoMap")
    @GlobalTransactional
    public GbmResult updateSupplierAcc(SysSupplier sysSupplier) {
        GbmResultVo gbmResultVo = gbmApiClient.updateUser(sysSupplier);
        if (gbmResultVo == null || gbmResultVo.getCode() != 200) {
            return  GbmResultGenerator.genFailResult(gbmResultVo.getMessage());
        }
        return  GbmResultGenerator.genSuccessResult();
    }
~~~


配置类
~~~
package com.gbm.cloud.common.config;

import feign.RequestInterceptor;
import feign.RequestTemplate;
import io.seata.core.context.RootContext;
import io.seata.spring.annotation.GlobalTransactional;
import org.apache.commons.lang.StringUtils;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnClass({RequestInterceptor.class,GlobalTransactional.class})
public class SetSeataInterceptor implements RequestInterceptor {

    @Override
    public void apply(RequestTemplate requestTemplate) {
        String currentXid = RootContext.getXID();
        if (!StringUtils.isEmpty(currentXid)) {
            requestTemplate.header(RootContext.KEY_XID, currentXid);
        }
    }
}

~~~


启动类增加注解 
>@SpringBootApplication(exclude = {SeataFeignClientAutoConfiguration.class})




###问题
1、启动参数 -h 127.0.0.1 -p 8091 -m db -n 1 -e test 注意 -e test ，会使用registry.config-test文件。
