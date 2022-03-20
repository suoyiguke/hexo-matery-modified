---
title: MultipartFile-转-file.md
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
title: MultipartFile-转-file.md
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
	@RequestMapping(value = "/kuaidi100Print", method = RequestMethod.POST)
	@ResponseBody
	@ApiOperation("快递100，云打印")
	public JsonResult kuaidi100Print(@RequestParam("file") MultipartFile multipartFile) throws Exception {

		CommonsMultipartFile cf1 = (CommonsMultipartFile)multipartFile;
		DiskFileItem fi = (DiskFileItem)cf1.getFileItem();
		File faceBest = fi.getStoreLocation();
		try {
			clientService.kuaidi100Print(faceBest);
		} catch (Exception e) {
			return jsonResultHelper.buildFailJsonResult(e.getMessage());
		}
		return jsonResultHelper.buildSuccessJsonResult("打印成功");
	}

~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7721fc6d0f1be746.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



~~~
	@RequestMapping(value = "/kuaidi100Print", method = RequestMethod.POST)
	@ResponseBody
	@ApiOperation("快递100，云打印")
	public JsonResult kuaidi100Print(@RequestParam("file") MultipartFile multipartFile) throws Exception {
		CommonsMultipartFile cf1 = (CommonsMultipartFile)multipartFile;
		String originalFilename = cf1.getOriginalFilename();
		File file = new File("D:\\Users\\Use'r\\Pictures\\".concat(originalFilename));
		cf1.transferTo(file);
		try {
			clientService.kuaidi100Print(file);
		} catch (Exception e) {
			return jsonResultHelper.buildFailJsonResult(e.getMessage());
		}
		return jsonResultHelper.buildSuccessJsonResult("打印成功");
	}
~~~



我不想再到程序中生成文件了，所以直接rname原来的
~~~
@RequestMapping(value = "/kuaidi100Print", method = RequestMethod.POST)
	@ResponseBody
	@ApiOperation("快递100，云打印")
	public JsonResult kuaidi100Print(@RequestParam("file") MultipartFile multipartFile) throws Exception {

		CommonsMultipartFile cf1 = (CommonsMultipartFile)multipartFile;
		DiskFileItem fi = (DiskFileItem)cf1.getFileItem();
		File faceBest = fi.getStoreLocation();
		String newName = faceBest.getPath().substring(0, faceBest.getPath().lastIndexOf("\\"))+"\\"+cf1.getOriginalFilename();
		File file = new File(newName);
		faceBest.renameTo(file);
		try {
			clientService.kuaidi100Print(file);
		} catch (Exception e) {
			return jsonResultHelper.buildFailJsonResult(e.getMessage());
		}
		return jsonResultHelper.buildSuccessJsonResult("打印成功");
	}

~~~
