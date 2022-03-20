---
title: hutool---TableMap--双向查找&&重复键.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: hutool---TableMap--双向查找&&重复键.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
~~~
    public static void main(String[] args) {

        TableMap<String,Object> tableMap = new TableMap(2);
        tableMap.put("aaa", 111);
        tableMap.put("aaa", 222);

        System.out.println(tableMap);
        List<Object> aaa = tableMap.getValues("aaa");
        System.out.println(aaa);

        List<String> keys = tableMap.getKeys(222);
        System.out.println(keys);
    }

~~~



应用： 双向匹配
~~~
    public static void main(String[] args) {

        String a = "1111,2222,3333";
        String b = "aaa,bbb,ccc";
        String[] splitA = a.split(",");
        String[] splitB = b.split(",");

        TableMap<String, String> tableMapAll = new TableMap(9);
        for (String as : splitA) {
            for (String bs : splitB) {
                tableMapAll.put(as, bs);
            }
        }


        ArrayList<Zz> list = new ArrayList<>();
        list.add(new Zz("1", "1111", 12));
        list.add(new Zz("1", "aaa", 13));
        list.add(new Zz("2", "2222", 14));
        list.add(new Zz("2", "bbb", 14));
        list.add(new Zz("4", "ccc", 15));
        list.add(new Zz("4", "3333", 15));

        Map<String, List<Zz>> map = list.stream().collect(Collectors.groupingBy(Zz::getId));
        for (Map.Entry<String, List<Zz>> stringListEntry : map.entrySet()) {
            String key = stringListEntry.getKey();
            List<Zz> value = stringListEntry.getValue();
            Map<String, Zz> cMap = value.stream().collect(Collectors.toMap(Zz::getSrc, m -> m, (v1, v2) -> v2));

            for (Map.Entry<String, Zz> stringZzEntry : cMap.entrySet()) {
                String src = stringZzEntry.getKey();
                final Zz zz = stringZzEntry.getValue();

                List<String> keys = tableMapAll.getKeys(src);
                for (String s : keys) {
                    if (cMap.containsKey(s)) {
                        System.out.println("存在");
                    }

                }
                List<String> values = tableMapAll.getValues(src);
                for (String s : values) {
                    if (cMap.containsKey(s)) {
                        System.out.println("存在");
                    }

                }
            }


        }


    }
~~~
