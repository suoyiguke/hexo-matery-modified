---
title: stream-集合操作提升.md
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
###对比二者 list转map
1、两个都是list转map

第一个Collectors.toMap有去重含义
~~~
 Map<Integer, JgOrderStateMate> mateMap = mateList.stream().collect(Collectors.toMap(JgOrderStateMate::getOrderState, m -> m, (v1, v2) -> v2));
~~~
第二个Collectors.groupingBy有分组含义
~~~
  Map<String, List<CertInfoPO>> collect = certSet.stream().collect(Collectors.groupingBy(CertInfoPO::getIdentityNumber));
~~~

2、Collectors.groupingBy 和mysql的 groupby的区别
mysql的 groupby无法直接得到Map<String, List<CertInfoPO>> 这种形式



3、案例：逗号分割字符串转Map
~~~
 List<String> strings = Arrays.asList("aaaa,bbbb,cccc", "ddddd,eeeee");

        Map<String, List<String>> collect = strings.stream().collect(Collectors.toMap(key -> key, key -> Arrays.asList(key.split(",")), (v1, v2) -> v1));
        System.out.println(collect);

~~~

4、转TreeMap
~~~
 TreeMap<Long, String> treeMap = new TreeMap<>();
     TreeMap<Long, String> map = treeMap.entrySet().stream()   		
     									.collect(Collectors.toMap(entry -> entry.getKey(), entry -> entry.getValue(), (oldValue, newValue) -> newValue, TreeMap::new));

~~~

5、转hutu的 TableMap
~~~
            TableMap<String[], String> collect = commodityRegion.stream().collect(Collectors.toMap(entry -> StringUtils.split(entry.getCommoditySku(), Constant.COMMA), m -> new StringBuilder(m.getProvinceName()).append(m.getCityName()).append(m.getAreaName()).toString(), (v1, v2) -> v2, new Supplier<TableMap<String[], String>>() {
                @Override
                public TableMap<String[], String> get() {
                    return new TableMap(commodityRegion.size());
                }
            }));
~~~

6、 t -> t => Function.identity()




7、转List
~~~
     // Accumulate names into a List
     List<String> list = people.stream().map(Person::getName).collect(Collectors.toList());
~~~
8、转TreeSet
~~~
     // Accumulate names into a TreeSet
     Set<String> set = people.stream().map(Person::getName).collect(Collectors.toCollection(TreeSet::new));
~~~
9、集合字符串拼接 join
~~~
     // Convert elements to strings and concatenate them, separated by commas
     String joined = things.stream()
                           .map(Object::toString)
                           .collect(Collectors.joining(", "));
~~~
10、sum 
~~~
     // Compute sum of salaries of employee
     int total = employees.stream()
                          .collect(Collectors.summingInt(Employee::getSalary)));
~~~
11、分组
~~~     
// Group employees by department
     Map<Department, List<Employee>> byDept
         = employees.stream()
                    .collect(Collectors.groupingBy(Employee::getDepartment));
~~~
12、分组统计
~~~     
// Compute sum of salaries by department
     Map<Department, Integer> totalByDept
         = employees.stream()
                    .collect(Collectors.groupingBy(Employee::getDepartment,
                                                   Collectors.summingInt(Employee::getSalary)));
~~~
13、分两组
~~~
     // Partition students into passing and failing
     Map<Boolean, List<Student>> passingFailing =
         students.stream()
                 .collect(Collectors.partitioningBy(s -> s.getGrade() >= PASS_THRESHOLD));
~~~

14、得到数组
~~~
        //用法1，得到Object数组
        Object[] objects = Stream.generate(ThreadLocalRandom.current()::nextLong)
            .skip(900).limit(1000).toArray();
        System.out.println(objects);
        //用法2,指定数组类型
        Long[] integers = new Long[1000];
        Stream.generate(ThreadLocalRandom.current()::nextLong)
            .skip(900).limit(1000).toArray(value ->integers);
        System.out.println(integers);
~~~

15、Stream.generate 快捷生成数据列表
这里是使用ThreadLocalRandom随机整形生成数据
~~~
    public static void main(String[] args) {
        List<Integer> collect = Stream.generate(Main::getAnInt)
            .limit(1000)
            .collect(Collectors.toList());
        //[) 前闭后开
        System.out.println(collect);

    }

    private static int getAnInt() {
        // 1~10
        return ThreadLocalRandom.current().nextInt(1,11);
    }
~~~

16、Stream.generate 可以构造自己的对象列表
~~~
    public static void main(String[] args) {
        List<User> collect = Stream.generate(Main::getNewUser)
            .limit(1000)
            .collect(Collectors.toList());
        //[) 前闭后开
        System.out.println(collect);

    }

    private static User getNewUser() {
        return new User(StrUtil.genGetter(RandomUtil.randomString( 10)),ThreadLocalRandom.current().nextInt(0,101));
    }
~~~



17、mapping和map现在来看是差不多的
~~~
        List<String[]> collect = Stream.of("name,111:age,20", "name,222:age,21").collect(mapping(m -> m.split(","), Collectors.toList()));
        System.out.println(collect);

        List<String[]> collect1 = Stream.of("name,111:age,20", "name,222:age,21").map(m -> m.split(",")).collect(Collectors.toList());
        System.out.println(collect1);;

~~~


用string list 构造 实体 list
~~~
 List<JgWarehouseOrder> collect = updateMap.keySet().stream().collect(mapping(m -> getOrder(m), toList()));
 
   private static JgWarehouseOrder getOrder(String platformOrderNo) {
        return  new JgWarehouseOrder().setPlatformOrderNo(platformOrderNo);
    }

~~~


18、reduce 归约合并

//两两合并
Optional<T> reduce(BinaryOperator<T> accumulator)
//两两合并，带初始值的
T reduce(T identity, BinaryOperator<T> accumulator)
//先转化元素类型再两两合并，带初始值的
<U> U reduce(U identity, BiFunction<U, ? super T, U> accumulator, BinaryOperator<U> combiner)

示例
~~~
List<Integer> demo = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8);
//数字转化为字符串，然后使用“-”拼接起来
String data = demo.stream().reduce("0", (u, t) -> u + "-" + t, (s1, s2) -> s1 + "-" + s2);
System.out.println(data);
~~~
-------result--------
0-1-2-3-4-5-6-7-8


19、flatMap扁平化的应用：分割多个地址集合成，单个地址集合
~~~
        //按地区
        Set<JgRulaEmbargo> towSet = setMap.get(Constant.NUMBER_ONE);
        if (ToolUtil.isNotEmpty(towSet)) {
            //将多个地址分割
            Set<String> addressSet = towSet.stream().filter(m -> ToolUtil.isNotEmptyAll(m.getDetailedAddress()))
                    .flatMap(m -> Arrays.stream(org.apache.commons.lang.StringUtils.split(m.getDetailedAddress(), Constant.SEMICOLON))).collect(toSet());
            region.addAll(addressSet);
        }

~~~


20、一个List转另一个List

~~~
    List<ZskAccessoriesListDtoError> errorList = dataMap.values().stream()
                .filter(ToolUtil::isNotEmpty)
                .filter(m -> ToolUtil.isNotEmpty(m.getErrMsg())).collect(Collectors.mapping(e -> ZskAccessoriesListDtoError.builder().errMsg(e.getErrMsg())
                        .accessoryName(e.getAccessoryName())
                        .spu(e.getSpu())
                        .price(e.getPrice())
                        .reissuedFreight(e.getReissuedFreight())
                        .specifications(e.getSpecifications())
                        .specifications(e.getDefectsLiabilityPeriod()).build(), Collectors.toList()));
~~~

21、分组排序
对组内元素再进行排序。
一时想不到什么一步到位得好方法。

1、先排序后分组可以实现一样得效果。
按分组字段1级排序，按排序字段2级排序即可
~~~
       List<MgbDictData> list = ((MgbDictDataRepository) mgbDictDataService.getBaseMapper()).getGdDict();
        DATAGROUPS = list.stream()
                .sorted(Comparator.nullsFirst(Comparator.comparing(MgbDictData::getDictType)
                .thenComparing(MgbDictData::getDictSort)
                .thenComparing(MgbDictData::getDictValue)))
                .collect(Collectors.groupingBy(MgbDictData::getDictType));

~~~

22、groupingBy 和toMap同时使用，得到HashMap<String, Map<String, String>>

>List-> List groupingBy -> Map<List>-->List toMap-->Map<Map>

~~~
        List<MgbDictData> list = ((MgbDictDataRepository) mgbDictDataService.getBaseMapper()).getGdDict();

  HashMap<String, Map<String, String>> collect = list.stream()
                .sorted(Comparator.nullsFirst(Comparator.comparing(MgbDictData::getDictType)
                        .thenComparing(MgbDictData::getDictSort)
                        .thenComparing(MgbDictData::getDictValue)))
                .collect(Collectors.groupingBy(MgbDictData::getDictType, HashMap::new, Collectors.toMap(MgbDictData::getDictValue, MgbDictData::getDictLabel, (v1, v2) -> v2)));
~~~

再进一步：使用treeMap实现设置顺序
~~~
  List<MgbDictData> list = ((MgbDictDataRepository) mgbDictDataService.getBaseMapper()).getGdDict();
        DATAGROUPS = list.stream()
                .collect(Collectors.groupingBy(MgbDictData::getDictType, HashMap::new, Collectors.toMap(MgbDictData::getDictValue, MgbDictData::getDictLabel, (v1, v2) -> v2,
                        () -> new TreeMap<>(Comparator.comparingInt(value -> {
                            if (NumberUtil.isNumber(value)) {
                                return Integer.valueOf(value);
                            } else {
                                return 0;
                            }
                        })))
                ));
~~~

23、其他的
1、Map<String, DictTypeEnum>转  Map<Integer, List<DictTypeEnum>>
~~~
 private static Map<String, DictTypeEnum> enumDataMap;
        Map<Integer, List<DictTypeEnum>> collect = enumDataMap.entrySet().stream().map(Map.Entry::getValue).collect(Collectors.groupingBy(DictTypeEnum::getIndex));

~~~

2、Map<String, DictTypeEnum> 转  Map<Integer, Map<String, DictTypeEnum>>
~~~
      enumDataMapMap = enumMap.values().stream()
                .filter(m -> !ToolUtil.isAllEmpty(m.getParentDictType(), m.getIndex())).collect(Collectors.groupingBy(DictTypeEnum::getIndex, HashMap::new, Collectors.toMap(DictTypeEnum::getDictType, Function.identity(), (v1, v2) -> v2)));
~~~

3、Map<String, List<MgbDictData>>  转 Map<String, Map<String, MgbDictData>>  
~~~
    private static Map<String, Map<String, MgbDictData>> dictTypeMap;

   dictTypeMap = dataGroups.values().stream().flatMap(List::stream)
                .collect(Collectors.groupingBy(MgbDictData::getDictType, HashMap::new, Collectors.toMap(MgbDictData::getDictValue, Function.identity(), (v1, v2) -> v2)));
~~~

4、Map<String, List<MgbDictData>>  转  Map<String, MgbDictData>
~~~
 private static Map<String, List<MgbDictData>> dataGroups;
        uuidDictMap = dataGroups.values().stream().flatMap(List::stream).collect(Collectors.toMap(MgbDictData::getUuid, Function.identity(), (v1, v2) -> v2));
~~~




