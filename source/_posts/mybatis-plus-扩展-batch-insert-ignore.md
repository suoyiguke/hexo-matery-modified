---
title: mybatis-plus-扩展-batch-insert-ignore.md
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
title: mybatis-plus-扩展-batch-insert-ignore.md
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
mybatis-plus为了兼容多个数据库，因此并没有提供对mysql 特性功能 insert ignore的支持。但是我们可以自己来实现！

###定义

定义一个mapper继承直接继承BaseMapper
~~~
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;
public interface CommonMapper<T> extends BaseMapper<T> {

    int insertIgnoreBatchAllColumn(@Param("list") List<T> list);

}
~~~

定义一个service接口继承之前的IService
~~~
import com.baomidou.mybatisplus.core.toolkit.CollectionUtils;
import com.baomidou.mybatisplus.extension.service.IService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.gbm.cloud.treasure.entity.jg.CustomsData;
import com.gbm.cloud.treasure.listener.handler.CommonMapper;
import org.apache.poi.ss.formula.functions.T;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

public interface CommonService<M extends CommonMapper<T>, T> extends IService<T> {
     Boolean  fastSaveIgnoreBatch(List<T> list, int batchSize) ;

    Boolean fastSaveIgnoreBatch(List<T> list) ;
}

~~~

定义一个serviceImpl继承之前的ServiceImpl，并实现CommonService接口

~~~
import com.baomidou.mybatisplus.core.toolkit.CollectionUtils;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.gbm.cloud.treasure.dao.CommonMapper;
import java.util.List;
public class CommonServiceImpl<M extends CommonMapper<T>, T> extends ServiceImpl<M, T> implements CommonService<CommonMapper<T>, T> {
    private static final Integer BATCH_SIZE = 100;

    @Override
    public Boolean fastSaveIgnoreBatch(List list, int batchSize) {
        if (CollectionUtils.isEmpty(list)) {
            return true;
        }

        batchSize = batchSize < 1 ? BATCH_SIZE : batchSize;

        if (list.size() <= batchSize) {
            return retBool(baseMapper.insertIgnoreBatchAllColumn(list));
        }

        for (int fromIdx = 0, endIdx = batchSize; ; fromIdx += batchSize, endIdx += batchSize) {
            if (endIdx > list.size()) {
                endIdx = list.size();
            }
            baseMapper.insertIgnoreBatchAllColumn(list.subList(fromIdx, endIdx));
            if (endIdx == list.size()) {
                return true;
            }
        }
    }
    @Override
    public Boolean fastSaveIgnoreBatch(List list) {
        return fastSaveIgnoreBatch(list, BATCH_SIZE);
    }
}


~~~




insert ignore真正实现的地方
~~~

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.core.enums.SqlMethod;
import com.baomidou.mybatisplus.core.injector.AbstractMethod;
import com.baomidou.mybatisplus.core.metadata.TableFieldInfo;
import com.baomidou.mybatisplus.core.metadata.TableInfo;
import com.baomidou.mybatisplus.core.metadata.TableInfoHelper;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.baomidou.mybatisplus.core.toolkit.sql.SqlScriptUtils;
import lombok.Setter;
import lombok.experimental.Accessors;
import org.apache.ibatis.executor.keygen.Jdbc3KeyGenerator;
import org.apache.ibatis.executor.keygen.KeyGenerator;
import org.apache.ibatis.executor.keygen.NoKeyGenerator;
import org.apache.ibatis.mapping.MappedStatement;
import org.apache.ibatis.mapping.SqlSource;

import java.util.List;
import java.util.function.Predicate;

public class InsertIgnoreBatchAllColumn extends AbstractMethod {

    private static final String MAPPER_METHOD = "insertIgnoreBatchAllColumn";

    @Setter
    @Accessors(chain = true)
    private Predicate<TableFieldInfo> predicate;

    @SuppressWarnings("Duplicates")
    @Override
    public MappedStatement injectMappedStatement(Class<?> mapperClass, Class<?> modelClass, TableInfo tableInfo) {
        KeyGenerator keyGenerator = new NoKeyGenerator();
        SqlMethod sqlMethod = SqlMethod.INSERT_ONE;
        String sqlTemplate = "<script>\nINSERT IGNORE INTO %s %s VALUES %s\n</script>";

        List<TableFieldInfo> fieldList = tableInfo.getFieldList();
        String insertSqlColumn = tableInfo.getKeyInsertSqlColumn(false) +
                this.filterTableFieldInfo(fieldList, predicate, TableFieldInfo::getInsertSqlColumn, EMPTY);
        String columnScript = LEFT_BRACKET + insertSqlColumn.substring(0, insertSqlColumn.length() - 1) + RIGHT_BRACKET;
        String insertSqlProperty = tableInfo.getKeyInsertSqlProperty(ENTITY_DOT, false) +
                this.filterTableFieldInfo(fieldList, predicate, i -> i.getInsertSqlProperty(ENTITY_DOT), EMPTY);
        insertSqlProperty = LEFT_BRACKET + insertSqlProperty.substring(0, insertSqlProperty.length() - 1) + RIGHT_BRACKET;
        String valuesScript = SqlScriptUtils.convertForeach(insertSqlProperty, "list", null, ENTITY, COMMA);
        String keyProperty = null;
        String keyColumn = null;
        // 表包含主键处理逻辑,如果不包含主键当普通字段处理
        if (StringUtils.isNotEmpty(tableInfo.getKeyProperty())) {
            if (tableInfo.getIdType() == IdType.AUTO) {
                /* 自增主键 */
                keyGenerator = new Jdbc3KeyGenerator();
                keyProperty = tableInfo.getKeyProperty();
                keyColumn = tableInfo.getKeyColumn();
            } else {
                if (null != tableInfo.getKeySequence()) {
                    keyGenerator = TableInfoHelper.genKeyGenerator(getMethod(sqlMethod),tableInfo, builderAssistant);
                    keyProperty = tableInfo.getKeyProperty();
                    keyColumn = tableInfo.getKeyColumn();
                }
            }
        }
        String sql = String.format(sqlTemplate, tableInfo.getTableName(), columnScript, valuesScript);
        SqlSource sqlSource = languageDriver.createSqlSource(configuration, sql, modelClass);
        return this.addInsertMappedStatement(mapperClass, modelClass, MAPPER_METHOD, sqlSource, keyGenerator, keyProperty, keyColumn);
    }
}

~~~


sql注入器
~~~

import com.baomidou.mybatisplus.core.injector.AbstractMethod;
import com.baomidou.mybatisplus.core.injector.DefaultSqlInjector;

import java.util.List;

public class CustomerSqlInjector extends DefaultSqlInjector {

    @Override
    public List<AbstractMethod> getMethodList(Class<?> mapperClass) {
        List<AbstractMethod> methodList = super.getMethodList(mapperClass);
        methodList.add(new InsertIgnoreBatchAllColumn());
        return methodList;
    }

}
~~~

mybatis 配置类添加声明好ISqlInjector ，不配置不生效
~~~

import com.baomidou.mybatisplus.core.config.GlobalConfig;
import com.baomidou.mybatisplus.core.injector.ISqlInjector;
import com.baomidou.mybatisplus.extension.plugins.PaginationInterceptor;
import com.baomidou.mybatisplus.extension.plugins.pagination.optimize.JsqlParserCountOptimize;
import com.gbm.cloud.treasure.listener.handler.CustomerSqlInjector;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MybatisPlusConfig {

。。。。。。

    @Bean
    public ISqlInjector iSqlInjector() {
        return new CustomerSqlInjector();
    }
}

~~~




###使用

1、普通的service
IJgOriginalOrderService 中继承 CommonService 而不是之前的 IService

~~~
import com.gbm.cloud.treasure.entity.jg.JgOrderExcelField;
import com.gbm.cloud.treasure.entity.jg.JgOriginalOrder;
import com.gbm.cloud.treasure.listener.handler.CommonMapper;
import com.gbm.cloud.treasure.dao.CommonService;

import java.util.List;
import java.util.Map;

public interface IJgOriginalOrderService extends CommonService<CommonMapper<JgOriginalOrder>,JgOriginalOrder>  {

     String saveDbAndExcel(List<JgOriginalOrder> dataList, List<Map<Integer, String>> errObjList, List<JgOrderExcelField> fieldList);

}

~~~

2、对应的serviceImpl，同样使用CommonServiceImpl代替之前的ServiceImpl
~~~
public class JgOriginalOrderServiceImpl extends CommonServiceImpl<CommonMapper<JgOriginalOrder>, JgOriginalOrder> implements IJgOriginalOrderService {
}
~~~


3、使用
~~~
originalOrderService.fastSaveIgnoreBatch(dataList,10);
~~~



定义业务mapper继承CommonMapper
 extends CommonMapper<MbUndertakesOrderDto>
