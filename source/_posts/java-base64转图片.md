---
title: java-base64转图片.md
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
title: java-base64转图片.md
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
~~~~


	public static String GetImageStr(String imgFilePath) {// 将图片文件转化为字节数组字符串，并对其进行Base64编码处理
		byte[] data = null;

		// 读取图片字节数组
		try {
			InputStream in = new FileInputStream(imgFilePath);
			data = new byte[in.available()];
			in.read(data);
			in.close();
		} catch (IOException e) {
			e.printStackTrace();
		}

		// 对字节数组Base64编码
		BASE64Encoder encoder = new BASE64Encoder();
		return encoder.encode(data);// 返回Base64编码过的字节数组字符串
	}

	public static boolean GenerateImage(String imgStr, String imgFilePath) {// 对字节数组字符串进行Base64解码并生成图片
		if (imgStr == null) // 图像数据为空
			return false;
		BASE64Decoder decoder = new BASE64Decoder();
		try {
			// Base64解码
			byte[] bytes = decoder.decodeBuffer(imgStr);
			for (int i = 0; i < bytes.length; ++i) {
				if (bytes[i] < 0) {// 调整异常数据
					bytes[i] += 256;
				}
			}
			// 生成jpeg图片
			OutputStream out = new FileOutputStream(imgFilePath);
			out.write(bytes);
			out.flush();
			out.close();
			return true;
		} catch (Exception e) {
			return false;
		}
	}


	public static void main(String[] args) {
		GenerateImage("iVBORw0KGgoAAAANSUhEUgAAAEUAAAAfCAYAAACxmAC4AAAFNklEQVR42u2ZfWzeUxTHn6frWl03Vlu9FBNSW0fLyBrNknXUa6QhI5uXxBps67wktbCYSTBMTWaGPzpkszLMRJWx1WbC/qCNYTObMvNg85JSjIUR8/je5POTk19+z6/PW9tlnOSTtvftd++5555z7m0k8r/0m+SIgfvp3IrEYyK3rz44QFwnvhLremH8k8TbGfS/UHwk4mJ0XyjkKLFBfCNeFrt74Rtuh/em2bdQxFDIHjG0txVSLnaKeaJA1Ga4o0FyrvhbrEyj7yAsNw6npjPAKHFQCgrZJS42Zc+Ly7KokMPFt+JHcUQa61kv/mSjpopoMh1doxX4gn1o8318RJgch0leYMpOoG9OkpN2u/ZGiOPLYZfdmLNTVEieaBPbRGeqfqQIRfyOP3iHv8t76LNVTPKVt4iaJL97iPiEbx2doM1t4nHmdHAKa8rFYt0mzxcL0jFR5w9GGMvpEif6rOkeMZgPrhU3+saoZSLJygra705glePFB+J8cX8K47q5Lhe/iucIAMMyPcMlnGFr0tXs6NniXiKB59WvxZtvDdlxvzifs1pUJXCewzB5tzFPcCyTFZcW/IXV3i0ezIZjmyXu8JUtRykzRYfIp7xO/EH91CTHP4YFHyami8sD/Mgr4ioc5WpT5wLAmeJ0cR6LjnHMPFklfhKviVfFsZkqxFnHJp+5FeNvPmYxpabuTZS1KkmvPoA+tfy9DP9kZY54kt8vFTNMXZ0JrZY1ps1SypyDfSYbVnK1uNNXNpfI9JtoMOVVfPwHcWSS47udfcTnmK2cw6YUGr9TbOov4ZsuL7pLjBGfioWmzShyGsfYTBUyhAlZLz+U47JdvOdziM1McGLImPXiAX53ucy7JgcaLpp8i3FHYaTxV60BTrTYWGUdWbTNX+YTwt8yZfn4mpTlYbGIRcyizDnVR1l8tWk7mnDqdr1SfCheDBhzs3gdBx3znW/nG6YZ575DXOSzivqQ+TrlfCnGmbKzxEbRSHyLawhqTDehRnt8+cUZcBHi/ayRHafX1aWdRk/M13mOsQ06aSsToIj+N8Y8xA0aX4Kr9zXxaSwUbJqa73bVSM/Oprfrp2i808kk0q/z2ncbLHRUSUZrJVZwU3m/Y1xH+3qC/EBMq7zE6UcO69cYN2/D4W/ot42ueoc4lAieR25uD1canAZ0SkK7CgCpx2FzfklKSBiXvJ2A0saJ3JUQ41ptiBw+w0eUkuCorgdDdDnGMZSaCUOFZY4Ks7Q9ySoN9krHIDR/hZsUVMoX49feehnNJ0fMkI44SiOFtnKacEtJ3Om8R2ngs8OY2dc28en5OBVhJaE91rxmApwwPqFvgyaivtASF5pomITYTyblGWjZA8gY8E3RUGk+l+H5BhzsHB7cGxZvqytSakrgVLvpUb+k5zjF7gkrkxILVIW14i7g8KqGvEGQdd+FaizM6AZCxVKcOvJZICNqiVb9aZZ4y1WOlCkwBmJGOJOlUBddegkMaQpKzb5BiZyGwiW1i09HKkZlPuUvqHiJYDuXpkJFHS70Qm10aanxeye0VZsta2Ho6f56C3GIuexNGNkUp4yWBGchMaTjSZaT3sXrakgrwiEvK+4l0tSk3mu4vyrL341RNtKiL9L0uIWkEyhYXvJWT7nzVasjWJkfiKpv1AIeWR8H+NbOOdZGLA+88OfmZFakiEyvpZIQVcFitD2mwiT+qTyTT0s0LyCK9ze2hXFPmPSAlR76lULmsHqhSSmncTYg94hYznXaSUW3M+pn+yuJKE62dS8er+nuw/MFxB6F1VibwAAAAASUVORK5CYII=\n","C:\\1.jpg");
	}
~~~~
