---
title: uibot-之元素定位之选取网页目标.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
---
title: uibot-之元素定位之选取网页目标.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---

![网页目标：百度主页的二维码](https://upload-images.jianshu.io/upload_images/13965490-b93e8d8fe6938b6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 网页目标：百度主页的二维码

 `wnd`信息标明了这个网页所在的浏览器窗口，`html`信息才是网页上的界面元素的关键信息。
*   **`html`**：代表这是一个网页界面元素；

*   **`url`**：对应浏览器地址栏中显示的URL，不参与元素特征匹配。仅在“绑定外部浏览器”命令中（在“浏览器”类命令中可以找到）用到，用于选择想要绑定的浏览器活动标签页；
*   **`title`**：与url类似，对应浏览器标签页的标题，不参与元素特征匹配，也仅在“绑定外部浏览器”命令中使用；
*   **`tagName`**：html标签类型（`div、a、input`等）；

*   **`attrMap`**：对界面元素详细的html描述；

*   **`index`**：一般起辅助作用，说明在满足特征条件情况下，元素出现的顺序。UiBot的index是从数字1开始的，当index没有填写或取0时，则会选择第一个出现的元素。

**实例：获取产品月销量**

![天猫商品列表](https://upload-images.jianshu.io/upload_images/13965490-9f976a8e9e64ee04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**具体步骤：**

1.  从UiBot Creator的命令区选择“获取元素文本”命令，如下图：

![获取元素文本命令](https://upload-images.jianshu.io/upload_images/13965490-2c82539267719bb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

获取元素文本命令

2.  在“获取元素文本”命令上点击“查找目标”按钮，并选择销量数字，如Intel i5 8500页面的“98”，如下图：

![选中需要获取的文本](https://upload-images.jianshu.io/upload_images/13965490-9305316961e20970.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

选中需要获取的文本

3.  用“输出调试信息”命令查看抓取到的值（当然，也可以用于其他用途，如转换成数字、保存到Excel表格等，本文暂不赘述其他用途），如下图：

![查看抓取的内容](https://upload-images.jianshu.io/upload_images/13965490-7cab2e7d632de5b1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看抓取的内容

看起来，好像工作得很好，毫无问题的获得了Intel i5 8500的月销量：98。但是，如果我们在其他商品上再去运行这个流程（使用Chrome浏览器，只需切换页面的标签即可，UiBot始终会在激活的标签工作），就会发现出问题了。

![在其他商品上运行流程](https://upload-images.jianshu.io/upload_images/13965490-525eeb2236026640.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在其他商品上运行流程

可以看到，在等待一定时间之后，UiBot最终因为没有找到目标而抛出了异常。那么，问题到底出在什么地方？我们应该如何做，才能让UiBot顺利找到目标呢？

点击“获取元素文本”命令，查看命令的属性，并具体打开“目标”属性进行查看，如下图：

![查看目标的属性](https://upload-images.jianshu.io/upload_images/13965490-bbf55c079e03b20a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

细心的读者可能已经发现了：原来`"aaname"`这条特征已经被固定在“98”了。这显然是不合理的：我们本来就是为了获取销量，如果把销量的数值98也加到特征里面，那是毫无意义的！因为销量一旦发生变化，特征就无法匹配了，造成“漏选”的问题。怎么办呢？我们可以很自然的想到：取消`aaname`特征的勾选状态，或把`aaname`的特征采用`"*"`进行通配，即可跳过这条造成“漏选”的特征。如下图：

![修改“aaname”的特征为通配符](https://upload-images.jianshu.io/upload_images/13965490-61277eb1968453a3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

修改“aaname”的特征为通配符

请注意，这里不必纠结上面图片框里显示的98，那只是一张参考图，在实际查找目标的时候不会起到任何作用。也不必纠结`title`和`url`这两条特征，因为前文已经提到，这两条特征也不会参与到查找目标的过程中。

修改完成之后，再次运行这个流程块，看看是否能正确获取其他商品的月销量。如下图：

![修改“aaname”特征之后的运行](https://upload-images.jianshu.io/upload_images/13965490-d3fc4fd7b651a072.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

修改“aaname”特征之后的运行

奇怪的事情发生了，之前的异常确实没有出现，并且获取到了内容。但是并不是我们想要的“77”，而是“**月销量**”几个字，这是怎么回事呢？

我们观察一下页面上的内容，发现修改“aaname”之后，虽然不会发生“漏选”，但由于文字“月销量”的特征和“77”完全一致，造成了“错选”。仔细查看即可发现，“月销量”文字和“77”的`tagName、attrMap`等特征完全一样，好比是一个户口本里的同一家人，已经无法区分了。怎么办呢？可以使用`"index"`特征来定位他们的不同。上文提到，UiBot的`index`是从数字1开始的，当index没有填写或取0时，则匹配第一个。从页面上看，“月销量”这个元素在销量数字的前面，如果它是第一个，那么销量数字就应该是第二个，因此，我们猜测，当的`index`取2的时候，就可以找到销量数字了。不妨填上试一下。

![修改“index”特征的值](https://upload-images.jianshu.io/upload_images/13965490-670bb70d6ce1cf17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

修改“index”特征的值

现在验证一下。在UiBot Creator工具栏上，点击“运行”按钮，直接运行当前的流程块。可以看到，在其他商品的页面上，也可以正确的拿到了其月销量数据了。
实际操作中，多多尝试和总结经验。
