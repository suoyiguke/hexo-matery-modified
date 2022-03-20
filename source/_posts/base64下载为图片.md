---
title: base64下载为图片.md
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
title: base64下载为图片.md
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
###base64下载为图片
~~~

    public static void main(String[] args) {
        try {

            String zz = "iVBORw0KGgoAAAANSUhEUgAAADwAAAAUCAIAAABeYcl+AAABoklEQVR42rWWvU0FQQyEXQTVECOIiIigBIpAtEMHZLRBC2SUwEqWzMgznl1ASNbp3v5+O2+8vnh7eV3x8f7J8XjzvEJ2/SIu765W/HGRpA388U/Qa+UkrvjRXG6MqUNCHx7j6eF2BcssoXn31sIDfqD0ufAMXWJLgXL36sIxEix4sqSciCUEQ6OnGyIuUl01AJ8aui1RoEzMqydosm6ht+q2AXvoprR3RSPGaDuhPdgARng+1T4RV6/hXr2Ncgstuet5fXG/AruyBenDeP/Q02gG5G76NXuYF+RG4nqGydmT26OgUUJsqXa88iZcD/1tD2mmfC97TNwJVEoXItujcXMet/xLVpZZe1oi4tLI3RBrjLSHFHWCLo1T8jYsphtHbiOrl0nE6brdckuZa1j42mMyHV+mK69xn8jRZC5zI4mriFMjF7AmMLu8ofuawonYJoZH5HTxhdcYyWwhsxDf20ZaaV+xZLGdtDz54MTxrbjwVS2gJx9PjuQuadPtSWR1mxrDZN5E6bm92NPfIq+ayUUxnVjqNwm/tb75wpHoTI/TvwDqlLlSmnt8NgAAAABJRU5ErkJggg==";
            ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(
                new BASE64Decoder().decodeBuffer(zz));
            byte[] bytes = IOUtils.toByteArray(byteArrayInputStream);
            IOUtils.write(bytes,new FileOutputStream("D:\\z1zz.jpg"));

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

~~~


###图片转base64
~~~
    /**
     * 将图片转换成Base64编码
     * @param imgFile 待处理图片
     * @return
     */
    public static String getImgStr(String imgFile) {
        // 将图片文件转化为字节数组字符串，并对其进行Base64编码处理

        InputStream in = null;
        byte[] data = null;
        // 读取图片字节数组
        try {
            in = new FileInputStream(imgFile);
            data = new byte[in.available()];
            in.read(data);
            in.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return Base64.encodeBase64String(data);
    }


~~~
