---
title: mybatis_plus-分页.md
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
title: mybatis_plus-分页.md
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
代码形式
~~~
        LambdaQueryWrapper<JqReturnExchange> queryWrapper = new LambdaQueryWrapper<>();
        /**
         * 过滤条件
         */
        queryWrapper
                .eq(ToolUtil.isNotEmpty(jqReturnExchangeVo.getCustomerName()), JqReturnExchange::getCustomerName, jqReturnExchangeVo.getCustomerName())
                .eq(ToolUtil.isNotEmpty(jqReturnExchangeVo.getOrderNo()), JqReturnExchange::getOrderNo, jqReturnExchangeVo.getOrderNo())
                .eq(ToolUtil.isNotEmpty(jqReturnExchangeVo.getSalesNumber()), JqReturnExchange::getSalesNumber, jqReturnExchangeVo.getSalesNumber())
                .eq(ToolUtil.isNotEmpty(jqReturnExchangeVo.getSalesType()), JqReturnExchange::getSalesType, jqReturnExchangeVo.getSalesType())
                .eq(ToolUtil.isNotEmpty(jqReturnExchangeVo.getAuditState()), JqReturnExchange::getAuditState, jqReturnExchangeVo.getAuditState())
                .eq(ToolUtil.isNotEmpty(jqReturnExchangeVo.getApplicant()), JqReturnExchange::getApplicant, jqReturnExchangeVo.getApplicant())
                .between(ToolUtil.isNotEmptyAll(jqReturnExchangeVo.getApplicationTimeStart(), jqReturnExchangeVo.getApplicationTimeEnd()), JqReturnExchange::getApplicationTime, jqReturnExchangeVo.getApplicationTimeStart(), jqReturnExchangeVo.getApplicationTimeEnd())
                .between(ToolUtil.isNotEmptyAll(jqReturnExchangeVo.getAuditTimeStart(), jqReturnExchangeVo.getAuditTimeEnd()), JqReturnExchange::getAuditTime, jqReturnExchangeVo.getAuditTimeStart(), jqReturnExchangeVo.getAuditTimeEnd());


        queryWrapper.select(JqReturnExchange::getId, JqReturnExchange::getOrderNo, JqReturnExchange::getLogisticsNo, JqReturnExchange::getCustomerName, JqReturnExchange::getPlatform,
                JqReturnExchange::getSalesType, JqReturnExchange::getApplicationTime, JqReturnExchange::getAuditTime,
                JqReturnExchange::getAuditState, JqReturnExchange::getDocumentSource, JqReturnExchange::getApplicant, JqReturnExchange::getAuditUser);

        page(page, queryWrapper);

        List<JqReturnExchange> records = page.getRecords();
        records.parallelStream().forEach(returnExchange -> {
            Integer auditStateInt = Optional.ofNullable(returnExchange)
                    .map(JqReturnExchange::getAuditState)
                    .map(AuditState::getCode).orElse(AuditState.TO_BE_APPROVED.getCode());
            returnExchange.setAuditStateInt(auditStateInt);
        });

        return GbmResultGenerator.genSuccessResult(new PageBean(page));
~~~


sql形式

~~~
    IPage<MsgjRecordVo> iPage = msgjRecordMapper.page(paraQueryParam.toPage(paraQueryParam),paraQueryParam.getParam());
        return GbmResultGenerator.genSuccessResult(new PageBean(iPage));
~~~
~~~
    IPage<MsgjRecordVo> page(Page<MsgjRecordVo> page, @Param("msgjRecordVo") MsgjRecordVo msgjRecordVo);


~~~
~~~
  
~~~
