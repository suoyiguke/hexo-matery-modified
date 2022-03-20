---
title: java-小技巧1，多表join时。提出类型、部门等在程序中兑换成名字.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
list转map。使用id做key，name做value
~~~
    private Map<String, String> getChannel() {
        List<MgbChannel> list = channelService.list(new LambdaQueryWrapper<MgbChannel>().eq(MgbChannel::getDelStatus, DelFlag.EFFECTIVE.getIndex()));

        return list.stream().collect(Collectors.toMap(MgbChannel::getChannelKey, MgbChannel::getChannelName, (k1, k2) -> k1));
    }


    private Map<String,String> getProductCategory() {

        List<ProductCategory> list = productCategoryService.list();
        return list.stream().collect(Collectors.toMap(ProductCategory::getCatNo, ProductCategory::getCatName, (k1, k2) -> k1));
    }


~~~


使用如下：
~~~
    @Override
    public GbmResult selectMgbGoodsPage(Page<MgbGoods> page, MgbGoodsDto dto) {
        Page<MgbGoodsVo> mgbGoodsVoPage = mgbGoodsMapper.selectMgbGoodsPage(page, dto);
        //品类
        Map<String, String> productCategoryMap = getProductCategory();
        //渠道
        Map<String, String> channelMap = getChannel();
        List<MgbGoodsVo> records = mgbGoodsVoPage.getRecords();
        for (MgbGoodsVo vo:records) {
            //获取品类名称
            //一级
            vo.setCatRootName(productCategoryMap.get(vo.getCatRootNo()));
            //二级
            vo.setCatParentName(productCategoryMap.get(vo.getCatParentNo()));
            //三级
            vo.setCatChildName(productCategoryMap.get(vo.getCatChildNo()));
            //上架渠道
            vo.setChannelName(channelMap.get(vo.getChannelKey()));
            //销量

            //商品状态
            vo.setStateName(MgbGoodsStateEnum.getMsgByIndex(vo.getState()));
            //获取0扣点采集价和代发价
//            getZeroPointsPrice(vo);
        }
        return GbmResult.success(new PageBean(mgbGoodsVoPage));
    }

~~~


这样就能代替大表的subquery了！！！


###value为实体类对象

~~~
    /**
     * 获取所有供应商名、售后地址，  supplierNo==>supplierName,refundAddress
     * @return
     */
    @Cacheable(value = "getSupplierBySupplierNoMap")
    @Override
       public Map<String, Supplier> getSupplierBySupplierNoMap() {
        List<Supplier> list = list(new LambdaQueryWrapper<Supplier>().select(Supplier::getSupplierNo, Supplier::getSupplierName,Supplier::getRefundAddress));
        return list.stream().collect(Collectors.toMap(Supplier::getSupplierNo, a -> a, (k1, k2) -> k1));
    }
~~~

