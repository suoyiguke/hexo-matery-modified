---
title: 如何获得dll中的progID.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
---
title: 如何获得dll中的progID.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
com组件可以存在exe，或者dll中，而且对vb，vc，delphi等语言提供了统一的调用，而dll只能存在于dll文件中，而且不同语言调用方式不一样，com组件开发难度相对于dll较大，多用于大型项目中。

java主要使用jacob来调用com组件。

1.注册com组件(这里使用大漠插件dm.dll）

regsvr32 dm.dll

另外regsvr32 /u dm.dll 代表卸载com组件



2.查看dll调用需要的progID

使用文本编辑工具以16进制方式打开dm.dll，搜索progID

可以看到progID就在''内，是"dm.dmsoft"


可以找到,有的dll可以通过这种方式。但是更多的dll不能
>ProgID = s 'XTXAppCOM.BJCASAC.1'
~~~
HKCR
{
	XTXAppCOM.BJCASAC.1 = s 'BJCASAC Class'
	{
		CLSID = s '{2DDCE69B-5144-425C-8BEF-B06D148928D0}'
	}
	XTXAppCOM.BJCASAC = s 'BJCASAC Class'
	{		
		CurVer = s 'XTXAppCOM.BJCASAC.1'
	}
	NoRemove CLSID
	{
		ForceRemove {2DDCE69B-5144-425C-8BEF-B06D148928D0} = s 'BJCASAC Class'
		{
			ProgID = s 'XTXAppCOM.BJCASAC.1'
			VersionIndependentProgID = s 'XTXAppCOM.BJCASAC'
			ForceRemove Programmable
			InprocServer32 = s '%MODULE%'
			{
				val ThreadingModel = s 'Apartment'
			}
			ForceRemove Control
			ForceRemove 'ToolboxBitmap32' = s '%MODULE%, 106'
			MiscStatus = s '0'
			{
			    '1' = s '%OLEMISC%'
			}
			TypeLib = s '{B8490A7B-56F2-482F-A71D-3D5B26DC61BB}'
			Version = s '1.0'
		}
	}
}
~~~
