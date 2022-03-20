---
title: java-反射.md
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
1、调用所有包含get的方法名，参数数目为0的
~~~
      Class<?> herosClass = Certificate.class;
        Method[] methods = herosClass.getMethods();
        for (Method method : methods) {
            if(method.getName().contains("get") &&   method.getParameterCount()  == 0){
                System.out.println(method.getName());
                Object invoke = method.invoke(x509Certificate);
                System.out.println(invoke);
            }
        }
~~~

2、使用字符串方法名调用方法
~~~
@Test
    public void test7() throws ClassNotFoundException, InstantiationException, IllegalAccessException, NoSuchMethodException, SecurityException, IllegalArgumentException, InvocationTargetException{

        Class<?> Person = Class.forName("com.Person");
        Object newInstance = Person.newInstance();
        for (int i = 1; i < 4; i++) {
            Method method = Person.getMethod("getPerson"+i, String.class);
            String str2= (String) method.invoke(newInstance, new Object[]{i+""});
            System.out.println(str2);
        }
    }
~~~

3、调用set
~~~
    /***
     * 初始化时加载所有set方法
     */
    static {
        Class cs = null;
        try {
            cs = Class.forName(JgOriginalOrder.class.getName());
        } catch (ClassNotFoundException e) {
            log.error("初始化JgOriginalOrder set 失败",e);
        }
        Field[] fileds = cs.getDeclaredFields();
        try {
            for (Field field : fileds) {
                PropertyDescriptor pd = new PropertyDescriptor(field.getName(), cs);
                //获取所有set方法
                Method method = pd.getWriteMethod();
                methodMap.put(field.getName(),method);
            }
        } catch (Exception e) {
            log.error("初始化JgOriginalOrder set 失败",e);
        }
    }

    private static void setObjOnOrder(JgOriginalOrder order, String fieldName ,Object setObj) {
        final Method method = methodMap.get(fieldName);
        try {
            method.invoke(order,setObj);
        } catch (IllegalAccessException e) {
           log.error("set 方法调用失败",e);
        } catch (InvocationTargetException e) {
            log.error("set 方法调用失败",e);
        }
    }
~~~


4、pojo 各种属性都为null判断

~~~
    private static Method[] methods = MgbsupplierBatchDto.class.getMethods();

    private static boolean isAllNull(MgbsupplierBatchDto t) {
        for (Method method : methods) {
            if (method.getName().contains("get") && method.getParameterCount() == 0) {
                if(!StringUtils.contains(method.getName(),"getCellStyleMap")&&!StringUtils.contains(method.getName(),"getClass") ){
                    Object invoke = null;
                    try {
                        invoke = method.invoke(t);
                    } catch (IllegalAccessException e) {
                        log.error(e.toString(),e);
                    } catch (InvocationTargetException e) {
                        log.error(e.toString(),e);
                    }
                    if (ToolUtil.isNotEmpty(invoke)) {
                        return false;
                    }
                }

            }
        }
        return true;
    }
~~~
