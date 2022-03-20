---
title: java-jpg、png转bpm.md
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
title: java-jpg、png转bpm.md
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

    /**
     *  jpg/bmp/png）转16位bmp(RBG565)
     * @param filePath
     * @param saveFileName
     */
    public static void image2RGB565Bmp(String filePath, String saveFileName) {
        try {
            BufferedImage sourceImg = ImageIO.read(new File(filePath));
            int h = sourceImg.getHeight(), w = sourceImg.getWidth();
            int[] pixel = new int[w * h];
            PixelGrabber pixelGrabber = new PixelGrabber(sourceImg, 0, 0, w, h, pixel, 0, w);
            pixelGrabber.grabPixels();

            MemoryImageSource m = new MemoryImageSource(w, h, pixel, 0, w);
            Image image = Toolkit.getDefaultToolkit().createImage(m);
            BufferedImage buff = new BufferedImage(w, h, BufferedImage.TYPE_USHORT_565_RGB);
            buff.createGraphics().drawImage(image, 0, 0 ,null);
            ImageIO.write(buff, "bmp", new File(saveFileName));
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        image2RGB565Bmp("D:\\QQ文档\\2542847562\\Image\\Group2\\$(\\SV\\$(SVR)A{80VV5(RDE%$OVVH.jpg","E:\\a\\$@QKE6T~4_DA_3%KAL~{6W7.bmp");
    }

~~~
