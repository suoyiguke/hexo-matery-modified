---
title: java-图片操作.md
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
title: java-图片操作.md
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
###改变格式
~~~
     BufferedImage bufferedImg = ImageIO.read(new File("D:\\大小.jpg"));
        //转为gif

        File file1 = new File("D:\\大小2.gif");
        ImageIO.write(bufferedImg, "gif", file1);

~~~

###判断格式
com.alibaba.simpleimage.util.ImageUtils
~~~
        InputStream inputStream = new FileInputStream(file1);
        InputStream input = ImageUtils.createMemoryStream(inputStream);
        System.out.println(ImageUtils.isJPEG(input));
        System.out.println(ImageUtils.isBMP(input));
        System.out.println(ImageUtils.isGIF(input));
        System.out.println(ImageUtils.isPNG(input));
        System.out.println(ImageUtils.isTIFF(input));

~~~

无依赖版本
~~~
        File imageFile = new File("d://111111.jpg");
        try (ImageInputStream imageInputStream = ImageIO.createImageInputStream(imageFile)) {
            Iterator<ImageReader> imageReadersList = ImageIO.getImageReaders(imageInputStream);

            if (!imageReadersList.hasNext()) {
                throw new RuntimeException("Cannot detect image format.");
            }

            ImageReader reader = imageReadersList.next();
            System.out.println("Image format：" + reader.getFormatName());
        }
~~~
###获得 BufferedImage 方式

###写入
ImageIO.write(BufferedImage , "jpg", new File(to));




### png 转 jpg 24位深度，添加白色背景
~~~
   public static void main(String[] args) throws IOException {

        String zz ="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";
        ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(new BASE64Decoder().decodeBuffer(zz));
        BufferedImage bufferedImg = ImageIO.read(byteArrayInputStream);


       // png 转 jpg的过程添加 白色背景。因为签章png背景是透明的。而jpg背景不能是透明。所以默认显示黑色。我们需要填充白色
        bufferedImg.createGraphics().drawImage(bufferedImg, 0, 0, Color.WHITE, null);
        FileOutputStream out = new FileOutputStream("D:\\111.jpg");//目标路径
        JPEGImageEncoder encoder = JPEGCodec.createJPEGEncoder(out);
        JPEGEncodeParam param=encoder.getDefaultJPEGEncodeParam(bufferedImg);//imgBuff 添加水印后的图片
        param.setQuality(1, true);//设置质量
        encoder.encode(bufferedImg, param);



        BufferedImage bufferedImage2 = new BufferedImage(bufferedImg.getWidth(), bufferedImg.getHeight(), BufferedImage.TYPE_3BYTE_BGR);
        for (int x = 0; x < bufferedImg.getWidth(); x++) {
            for (int y = 0; y < bufferedImg.getHeight(); y++) {
                bufferedImage2.setRGB(x, y, bufferedImg.getRGB(x, y));
            }
        }
        FileOutputStream fileOutputStream2 = new FileOutputStream("D:\\1111.jpg");//目标路径
        JPEGImageEncoder encoder2 = JPEGCodec.createJPEGEncoder(fileOutputStream2);
        JPEGEncodeParam param2=encoder2.getDefaultJPEGEncodeParam(bufferedImage2);//imgBuff 添加水印后的图片
        encoder2.encode(bufferedImage2,param2);
        fileOutputStream2.close();


        /**
         * 检查是不是 jpg
         */
//        File file = new File("D:\\111.jpg");
//        byte[] bytes = FileUtils.readFileToByteArray(file);
//        String  stampBase64 = Base64Util.encode(bytes).replaceAll("\r\n", "");
//        System.out.println(stampBase64);






    }

~~~

### 字节数组转 base64码
Base64Util.encode(outputStream1.toByteArray()).replaceAll("\r\n", "");

###base64转字节数组、转ByteArrayInputStream 、转
  byteArrayInputStream = new ByteArrayInputStream(
                new BASE64Decoder().decodeBuffer(base64));

byteArrayOutputStream.toByteArray()

###获得base64 图片/文件大小，单位字节
~~~
  System.out.println(new BASE64Decoder().decodeBuffer(zz).length);
~~~

###检查base64图片的属性
~~~
    public static void main(String[] args) throws IOException {
        ByteArrayInputStream byteArrayInputStream = null;
        ByteArrayOutputStream byteArrayOutputStream = null;
        try {

            String zz ="/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAA1AHIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD+/iiiuF/4Wf8ADkfEwfBg+OfCn/C3G8Ct8Tx8NP7d03/hOD8OV19fCjeOR4Z+0f2ufCi+JnXQDrv2T+zRq7DT/tH2oiOgDuqKrXl5Z6fbTXl/dW1jZ26GSe7vJ4ra2gjXq808zpFEg7s7qo7mpIJ4LqCG5tpori2uIo57e4gkSaCeCZBJFNDLGWjliljZXjkRmR0YMpKkGgCWiiigAooooAKKKKACivGfi5+0H8HfgPqHwo074u+NrTwNL8b/AIoaH8Fvhjd6rpmuy6N4i+Kfiew1TUPDHgufxBp+l3mheHdW8TRaNqFr4c/4SjUdFtde1eKHQtJubzW72x0+59moAKKKKACiiigDwD49/tGeEf2f7DwyNY8J/FT4jeMfHmpXeifDv4afBz4c+IfiF428a63ZW8d1dWNu2nwW/hHwfp1pbSpcal4y+J3ivwL4A0O2Jute8WaXbK0o/Af4ut8d/Fn/AAVjHxn+OfjzV/2DfCvw6/4Jx+G/HniO0+BF5F8fPjDqXwn8MftkaVrcPgLxxq9v8ONd8NaPqnjHxDElh488LfDXwd8YNNbw3DeaDoHjnWP7Rm121/ZL/go3+2Hpf7Dn7JPxJ+OJfQrnx7IulfDr4IeHfEeqWWi6N4u+OvxHvU8LfC/QtX1PULi1s9N8NW/iG9i8R+OdYubiG28O+ANA8V+JLyWOy0e4kT+ef/gnv+zlF8Wv2utD+BngP4l/GfwT+zn8MP8Agmj8Erj4k/FVdM1D4dfFP9v2b4wftXftKfEH4mfFnwP41GtWPxJ+E3wN+OHxm0bxjql1rJ0Pwr8UfHvgrTdNHgLW/DPw38R6V4n8UAH0t8b9Ks/+CqfjHxAvh3/gmv8AGHwh8BtXe3034ifHfxd+y38LPg1+2N+0LoVhbW+jWOkeCvHf7V9x8I9S+B3we1XRYLGyb4leFdU+In7Qeo+FTJo/hHwb8E7+wsvFU/7C/CzSv2jPhH8OPAfwq+EP7J37Mnw0+F/w+8LaL4N+H3gS9/au8fadeeFfB/hrT7fStH0ibTfD/wCyX4z0lZ7Cyt7eKX7J4x8Qeex+0XOs3V1NNIzvjP8As3/Er4t/Gf4FXV/8W4PhZ+yR+zzfeH/ii3ws+Gs+veFvG/xb+K3g19Qi8IaN8TvGlpqGnadpf7PfgSwNlrdx8NNGtLhviN4jgs4/GmqweENCbw3r/wArfszJa/tw/tkeI/8AgpBqmR+zT+z54H8cfs5/sE3upE22m+PYfEuqafP+1D+17pouCIk8J+P9Q8KeHvhD8H9dWVLbxB8N/Avifx3bLLoPxB0G7IB9Rfs0ftgeIvjJ+0T+1j+yr8TPhVpHwy+L/wCydbfArxFr9z4M+It58Ufh3428DftD+GvFmv8AgPX/AA34l1n4e/CvxFZavY3XgTxbofivw5q/guCPS7ywsrrStc16x1JZ7f6o+JfxW+GfwZ8LXHjf4s+PvCHw48JWtxbWUniHxp4g0zw7pkmo3zmLT9JtLnU7m3W+1nVJ8WulaPZfaNU1W8eOz0+0ubqSOJvyx/4Ju+F9Y+PI/bo/4KB2Ot6l4L1D/goF8Uk079nvxfY6XpV3qWh/sp/s6eE774Kfsz/EDT9E8S2GqaTeSeOdQHxC/aB0W11ywv8ASdT0b4n6GLvT3tZZYZPLfi3+xn+zH+xl4T8Tftgftr/tC/tbftrfE61uo/DvgpPiT420yLxx44+IHj+8XRvDX7P37Pvw1+A3hb4TrLD8WtZlsfDVn8C7F9Q+GmszSS614l8OrZ2Or67aAHmv7SPxv179pD4j+JPAPgL9qP4pfBvwTqsyyxy/G3xVF8G9T8J6NdwRQXFz8Ff2MvgJo3wp/bo+OOpTBLloX/aw8X+BfgssFzaatb+FPi9of23QdU/S3/gnP8Lf2fvgR8Bz8Gf2eb/4/eI9B8Ma/ea/4u8e/tDeCvjV4Z8YfETxv4vH2rWvGEWrfFvwJ4C0bXbfUm06NRY/CvSbbwD4YtobDTNL0nRreW2gn8MT9oT4k/s/+Mv+CUv7Ovhj9l74H/s0at+2l42+LNv8bPgt4buYPE2i/A7Qvhl+zh46+N3iHRPBXib4faV8M/Cmq+M4Nf0Pw14a1TxBJ4Pv/DVxPd6rbafbahE2n+Ij+t9ABXzR+0Z408WeD5PhXY+Gf2iP2f8A9n+4+I/j6L4X6L/wvL4c6n4/1D4mePvEmmXmp+EfAfwqWy+PfwTtrfx5Pp3h3xXqkGjz2PxAutdtLCWe10S0t9E1Br/lviz+1zpHwu/bA/ZD/ZBTwVqPiXxJ+1Z4a/aN8Zf8JTZaxa2th8NPDH7PHhfwdrN9qeu6QbK6vNTTxfrfjrQvDOjFLjTLaC5F/cSXVzJbJYz/ABL/AMFE8fGv9u7/AIJF/sreHNt74g8G/tM+Mv2/viJJaA3E/gr4Ufsy/Bz4geAtG1jXI4yx0/TvHPxV+OHhTwTodxcRquoaml+ttLjS77YAdn+3N4Z8IfBH9lz4j/HT9tz9pT48/FX4G/DK58EeL/HfgLwr8JP2V20BL+3+IHhiw8J634Z0HUfgpdeO9Pu/C3izUdD8Q2WoRfFh9e0eXTDqumam19a28Mnof9p/8E5/hB4z0rXfGP7WvhmHxt4SvW1WwT42/wDBQf4g+Lv7J1GEyRT3q+Efir8fNY8O2B3ySJPbw+H7axjOIVtYo4ooo/iX/gtv+z/8O/jr4S+HH7N9loXj/wCKn7Qn7cPxc+H3w68EeBrr4m+LtW8K/D34Q/B3V9A+Ln7SHxZ8FfCXxP420n4J+GNc0D4VeDtQ8MWvjnUNO0LUrj4i/EvwNo+oeLbWx1hIU/Ur9j39oP4JfH74d6rP8I/CV18Jtd+HmvyeA/i98AfE/hbSPAXxM+BPxE02zt57vwF8RfBOjTXGn6Xfpp89nqfh7W9EvdY8G+NPC95pXivwL4i8Q+FtU03VbgA+lPCnizwt478NaF4z8EeJdA8Y+D/E+l2et+GvFfhXWNP8QeG/EOi6hCtxYavoeuaTcXematpl9buk9nf2F1cWtzC6ywyujBj0FFFABRRRQB8a/tX/ALBX7Nn7bfiL4Aax+0v4Sv8A4l6B+zh8Q774reCPhnqus3S/CzXvH02kjR9I174jeCkX+z/HZ8K27Xj+HtM1ppNHibVdYtdT0/VNM1W+sJvAPBdjrkf/AAWh/aB1ZvC3ie18JXP/AATN/ZQ8M6Z4um8Na1beDNQ8ReF/2m/2u9b1zw7pniiSwTw/e63pGkePvC99e6PaahLf2tpqlvNJbJFuZf1JooA/ny/4KE/E79pj49/Gz4cfDTTfg7+1Dof/AASx8JfEzxL8Dv8AgoL4n8CfDvWbf4n/AB9TxFp9te6HH8NPAlh4J1H9oHVP2UvAfi7wpbfDv9oL4s/CttIh+I3gj4veK7XwTF4n8FeEdZ8bWH0r8YLnxp+3N4Y0/wDY1/Zq+HXxL+Bv7IGoWOm+DP2kv2hPEvw58Xfs+xT/AAN060i0/V/2bf2UvAvjTQvB3jrVde+JGhQJ4B8QfFuw8J6R8Lfhd8OL7X28EeIvFHxCOkaToP68UUAYvhrw3oHg3w5oHhDwpo2m+HPC3hXRdK8N+GvD2jWcOn6RoWgaHYwaZo2jaVYWyR29jpul6da21lY2dvGkNtawRQxIsaKo+Sv+GKvB+uftf3f7YfxO+IHxF+LPiTw1omm6J+z78LPGWqWbfBr9maU6Dc6F4z8Y/CzwNptnZ2EvxQ+IdvfX9v4h+KHis6942sdBvrzwh4b1fRfCt3daTN9n0UAfmR+3N8DPjbr37SH/AAT6/a4+C3gdvi+f2PfiV8cJfiP8GNK8SeEvCPjjxp8Pf2gPgrq/wo1HXfh1rfxA1vwv4BufFfgDVpdG8Qjwx4t8V+EdO8S6KdXs7fxNp2pw2MN77lqv7Qv7QWtWaaf8Mf2I/i8PFF9iC01P43/EP4DfC/4X6DcMMmbxl4g8EfE34zfElLGIBgJPAXwg8fyzzKsOy3hl+2R/YtFAH5Yap4S+H37DyfGz/gph+3R8Wbb4ifGmP4baX8O7nxJ4X8J3mj+D/hl8NJvE1re+GP2a/wBmD4YtqniDxLqOq/Ef4k3+iQ3t9rOu6/8AEP40/Eebw0LmXQdB07wp4L8Lcn+z5pcX7L3gL9pH/gqN/wAFB77Tvhp8bvjppOh6/wCN9Ev7o+Im/Zo/Z68JS3Nt8A/2Q/BTaalzN4l8YWFzr8up+N7DwZZy3XxV/aN8f69Z+HbHW4o/B0dfrdqGmabq0CWuqafZalbR3Nnepb6haQXkCXmn3UV7YXaQ3Ecka3NjewQXdnOFEttdQxXELpLGjj5w+Iv7IfwW+Lfx6+GX7Q/xJ0/xX4z8WfBywth8N/BuueO/Ft38GfDXi3T77WrzRvirF8GG1YfDm/8Ai/4ej8Razp3hv4k6p4fvvFHh6wvETRr6yubHTbmzAPnH9iz4M/Ezxx8RvHP/AAUA/aj8KXvg748/Grw1beBvg38G9aeCe/8A2Tv2U7XUo9f8MfCnUBby3FpH8YfiVrEdr8Tv2jNSsrieJfF//CM/DayurzQPhTol/fegftI/si6/4w+IelftQ/sxeNtL+B37YHhPQbfwyvi7VNKu9Y+Fvx5+H2n3c+o2/wAFf2l/B+l3Nje+LvA6Xl1fXHgzxpo11Z/En4O61qV9rvgTVZdM1PxX4O8X/dVFAHxh8Jf2urvWfEegfCj9oz4M/ED9mP45awy6fZaN4jtZ/G3wU8d6xHGzSL8IP2jfCthL8OfFUeotHJNoHhLxrL8NfjNeWQ87UvhNpDpLEn2fRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB/9k=";
            byte[] bytes = new BASE64Decoder().decodeBuffer(zz);
            byteArrayInputStream = new ByteArrayInputStream(
                bytes);

            //判断格式
            InputStream input = ImageUtils.createMemoryStream(byteArrayInputStream);
            System.out.println(ImageUtils.isJPEG(input));
            System.out.println(ImageUtils.isBMP(input));
            System.out.println(ImageUtils.isGIF(input));
            System.out.println(ImageUtils.isPNG(input));
            System.out.println(ImageUtils.isTIFF(input));

            //得到图片数据
            System.out.println(bytes);

            //得到图片宽高
            BufferedImage bufferedImg = ImageIO.read(byteArrayInputStream);
            System.out.println(bufferedImg.getWidth());
            System.out.println(bufferedImg.getHeight());



        }catch (Exception e ){
            e.printStackTrace();
        }finally {
            if(byteArrayInputStream !=null){
                byteArrayInputStream.close();
            }
            if(byteArrayOutputStream !=null){
                byteArrayOutputStream.close();
            }
        }





    }

~~~

###打印图片基本数据
~~~

    public static void printImageInfo(String base64) throws IOException {

        ByteArrayInputStream byteArrayInputStream = null;
        byte[] bytes = new BASE64Decoder().decodeBuffer(base64);
        byteArrayInputStream = new ByteArrayInputStream(
            bytes);

        //判断格式
        ImageInputStream imageInputStream = ImageIO
            .createImageInputStream(byteArrayInputStream);

        Iterator<ImageReader> imageReadersList = ImageIO.getImageReaders(imageInputStream);

        if (!imageReadersList.hasNext()) {
            throw new RuntimeException("Cannot detect image format.");
        }
        ImageReader reader = imageReadersList.next();
        System.out.println("Image format：" + reader.getFormatName());

        //得到图片数据
        System.out.println("大小 " + bytes.length);

        //得到图片宽高
        BufferedImage bufferedImg = ImageIO.read(imageInputStream);
        System.out.println("Width  " + bufferedImg.getWidth());
        System.out.println("Height  " + bufferedImg.getHeight());


    }


~~~
