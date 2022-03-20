---
title: java-内存中join-算法.md
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
这个有点像mysql join 算法

###double netsted for
~~~
import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

public class Join {

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    static
    class Couple {

        private Integer familyId;
        private String userName;
    }

    public static void main(String[] args) {
        // 用于计算循环次数
        int count = 0;

        // 老公组
        List<Couple> husbands = new ArrayList<>();
        husbands.add(new Couple(1, "梁山伯"));
        husbands.add(new Couple(2, "牛郎"));
        husbands.add(new Couple(3, "干将"));
        husbands.add(new Couple(4, "工藤新一"));
        husbands.add(new Couple(5, "罗密欧"));

        // 老婆组
        List<Couple> wives = new ArrayList<>();
        wives.add(new Couple(1, "祝英台"));
        wives.add(new Couple(2, "织女"));
        wives.add(new Couple(3, "莫邪"));
        wives.add(new Couple(4, "毛利兰"));
        wives.add(new Couple(5, "朱丽叶"));

        for (Couple husband : husbands) {
            for (Couple wife : wives) {
                // 记录循环的次数
                count++;
                if (husband.getFamilyId().equals(wife.getFamilyId())) {
                    System.out.println(husband.getUserName() + "爱" + wife.getUserName());
                    // 把已经匹配的remove
                    wives.remove(wife);
                    //本次已经找到，再循环下去没有意义
                    break;
                }
            }
        }
        System.out.println("----------------------");
        System.out.println("循环了：" + count + "次");
    }
}
~~~

在本案例中，第三版算法在男嘉宾顺序时可以得到最好的结果（5次），如果倒序则得到最差的结果（15次）。



第二种算法，使用hash

### hash join
~~~

    public static void main(String[] args) {

        // 用于计算循环次数
        int count = 0;

        // 老公组
        List<Couple> husbands = new ArrayList<>();
        husbands.add(new Couple(1, "梁山伯"));
        husbands.add(new Couple(2, "牛郎"));
        husbands.add(new Couple(3, "干将"));
        husbands.add(new Couple(4, "工藤新一"));
        husbands.add(new Couple(5, "罗密欧"));

        // 老婆组
        List<Couple> wives = new ArrayList<>();
        wives.add(new Couple(1, "祝英台"));
        wives.add(new Couple(2, "织女"));
        wives.add(new Couple(3, "莫邪"));
        wives.add(new Couple(4, "毛利兰"));
        wives.add(new Couple(5, "朱丽叶"));

        // 给女嘉宾发牌子
        Map<Integer, Couple> wivesMap = new HashMap<>();
        for (Couple wife : wives) {
            // 女嘉宾现在不在List里了，而是去了wivesMap中，前面放了一块牌子：男嘉宾的号码
            wivesMap.put(wife.getFamilyId(), wife);
            count++;
        }

        // 男嘉宾上场
        for (Couple husband : husbands) {
            // 找到举着自己号码牌的女嘉宾
            Couple wife = wivesMap.get(husband.getFamilyId());
            System.out.println(husband.getUserName() + "爱" + wife.getUserName());
            count++;
        }

        System.out.println("----------------------");
        System.out.println("循环了：" + count + "次");
    }
~~~

此时无论你如何调换男嘉宾出场顺序，都只会循环10次。

###小结


它的精髓就是利用HashMap给其中一列数据加了“索引”，每个数据的“索引”（Map的key）是不同的，让数据差异化。
了解原理后，如何掌握这简单有效的小算法呢？
记住两步：
• 先把其中一列数据由线性结构的List转为Hash散列的Map，为数据创建“索引”
• 遍历另一列数据，依据索引从Map中匹配数据
相比第三版在原有的两个List基础上操作数据，第四版需要额外引入一个Map，内存开销稍微多了一点点。算法中，有一句特别经典的话：空间换时间。第四版勉强算吧。但要清楚，实际上Couple对象并没有增多，Map只是持有原有的Couple对象的引用而已。新增的内存开销主要是Map的索引（Key）。
请大家务必掌握这个小算法，后面很多地方会用到它。
