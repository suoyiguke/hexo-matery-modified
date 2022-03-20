---
title: mybatis_plus-自定义sql分页.md
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
title: mybatis_plus-自定义sql分页.md
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
~~~
       QueryWrapper<Object> queryWrapper = Wrappers.query()
                .eq("a.knowledge_id", knowledgeId)
                .eq("a.subject_type", subjectType)
                .orderByDesc("a.id");
        IPage<ZskOperationLogDto> ipage = ((ZskOperationLogMapper) iZskOperationLogService.getBaseMapper()).getLogList(knowledgeId, subjectType, page, queryWrapper);
~~~
~~~
    <select id="getLogList" resultType="com.gbm.cloud.treasure.entity.zsk.dto.ZskOperationLogDto">
        SELECT
            a.operation_time,
            a.operation_user,
            a.msg,
            b.id AS update_info_id
        FROM
            zsk_operation_log a
                LEFT JOIN zsk_update_info b ON a.id = b.log_id
            ${ew.customSqlSegment}
    </select>
~~~

~~~
    IPage<ZskOperationLogDto> getLogList(@Param("knowledgeId") Long knowledgeId, @Param("subjectType") SubjectTypeEnum subjectType, @Param("page") IPage<ZskOperationLogDo> iPage, @Param(Constants.WRAPPER) Wrapper wrapper);

~~~
