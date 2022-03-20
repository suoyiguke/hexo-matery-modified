---
title: java中continue-外层循环.md
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
~~~   
     List<Product> allProducts = new ArrayList<>(treeSet);
        List<Product> addProducts = new ArrayList<>();
        a:for (Product product : allProducts) {
            for (Product existProduct : existProductList) {
                if (comparator.compare(existProduct,product)==0){
                    product.setSpu(existProduct.getSpu());
                    continue a;
                }
            }
            product.setSpu(codeGenerator.getSpu(brandIdMap.get(product.getBrandNo()),catIdMap.get(product.getCatNo())));
            product.setReplaceSendTag(supplierMap.get(product.getSupplierNo()).getReplaceSendTag());
            product.setReplaceSendEmail(supplierMap.get(product.getSupplierNo()).getReplaceSendEmail());
            product.setReplaceSendTimes(supplierMap.get(product.getSupplierNo()).getReplaceSendTimes());
            product.setReplaceSendFrequency(supplierMap.get(product.getSupplierNo()).getReplaceSendFrequency());
            product.setRemark(supplierMap.get(product.getSupplierNo()).getReplaceSendRemark());
            product.setTermsNoArray(String.join(",", terms.stream().map(AfterSaleTermsDto::getTermsNo).collect(Collectors.toList())));
            addProducts.add(product);
        }
~~~
