---
title: layer-递归调用弹出窗，而不是一下子全部弹出.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
---
title: layer-递归调用弹出窗，而不是一下子全部弹出.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
~~~

<script>


    $(function () {


        var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


        function zz() {
            let number = arr.pop();
            if (number) {
                //在这里面输入任何合法的js语句
                layer.open({
                    type: 1 //Page层类型
                    , area: ['500px', '300px']
                    , title: '你好，layer。' + number
                    , shade: 0.6 //遮罩透明度
                    , maxmin: true //允许全屏最小化
                    , anim: 1 //0-6的动画形式，-1不开启
                    , content: '<div style="padding:50px;">这是一个非常普通的页面层，传入了自定义的html</div>'
                    , end: function () {

                        zz()
                    }
                });

            }
        }


        zz();


    });

</script>
~~~
