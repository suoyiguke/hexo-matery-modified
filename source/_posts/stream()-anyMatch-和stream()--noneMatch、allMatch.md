---
title: stream()-anyMatch-和stream()--noneMatch、allMatch.md
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
anyMatch 对应Predicate方法， 返回布尔值

anyMatch 与fitter类似。fitter过滤，anyMatch 匹配；
如果不使用anyMatch ，那么只能写 一个for循环加一个if。
这样几乎既可以消除for循环了
~~~
        Student stu1 = new Student(01, 19, "张三");
        Student stu2 = new Student(02, 23, "李四");
        Student stu3 = new Student(01, 28, "王五");
        List<Student> list = new ArrayList<>();
        list.add(stu1);
        list.add(stu2);
        list.add(stu3);
        boolean isOk=false;
        // 判断学生年龄是否有大于27岁的
        for (Student student : list) {
            Integer age = student.getAge();
            if(age>27){
                isOk = true;
                break;
            }
        }
~~~

>在一个集合里判断里面的元素是否达成某个条件

~~~
  @Data
    @AllArgsConstructor
    static
    class Student{
        private Integer id;
        private Integer age;
        private String name;
    }

    public static void main(String[] args) {

        Student stu1 = new Student(01, 19, "张三");
        Student stu2 = new Student(02, 23, "李四");
        Student stu3 = new Student(01, 28, "王五");
        List<Student> list = new ArrayList<>();
        list.add(stu1);
        list.add(stu2);
        list.add(stu3);
        // 判断学生年龄是否有大于27岁的
        boolean anyMatchFlag = list.stream().anyMatch(student -> student.getAge() > 27);
        System.out.println(anyMatchFlag);
    }


~~~


用的好的：

~~~
    request.getFieldValues().stream()
      .map(oneFieldValues -> readOneFieldValues(oneFieldValues, request.getKey()))
      .peek(map -> checkRequest(map.values().stream().anyMatch(StringUtils::isNotBlank), MSG_NO_EMPTY_VALUE))
      .flatMap(map -> map.entrySet().stream())
      .peek(entry -> valuesByFieldKeys.put(entry.getKey(), entry.getValue()))
      .forEach(entry -> checkRequest(fieldKeys.contains(entry.getKey()), "Unknown field key '%s' for setting '%s'", entry.getKey(), request.getKey()));

~~~
