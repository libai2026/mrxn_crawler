---
title: "Badusb初玩步骤记录&疑问探讨"
source: https://mrxn.net/jswz/diy-myself-badusb2.html
asset_dir: assets/badusb初玩步骤记录&疑问探讨
---

# Badusb初玩步骤记录&疑问探讨

[Mrxn](https://mrxn.net/author/1)- 发表于2016/4/1 14:09
- 6651浏览
- [2评论](#comment)
- 25分钟阅读

深入探索

授权

传输层安全性协议

计算机安全

---

一直在各大常逛的网站看到关于Badusb的文章，顿时觉得很神奇，很高端，于是一直想拥有这么一个邪恶的东西，可是因为2303不是很好找，并且git上的编译写入过程一看就头大，所以一直搁浅了，可是并没放弃，扯远了，扯回来。

PS:英文好的同学可以直接去Git看[官方教程](https://github.com/adamcaudill/Psychson)   
PS：发现关于Badusb的详细教程文章国内寥寥无几，大牛们肯定都是在躲着玩..让后来想学的小白怎么办

俄罗斯大神发的帖子，有制作视频，查资料去看吧：https://dmyt.ru/forum/viewtopic.php?f=7&t=383

需要的环境&工具

0.2303芯片的U盘  （废话...）  
1.Visual Studio 2012（编译所需工具用，可选安装，我会编译打包好）   
2.Java环境  （执行encoder所需）   
3..NET framework 4.5（系统自带，没有请到微软官网下载）   
4.SDCC  http://sdcc.sourceforge.net   //安装至C:\Program Files\SDCC目录下   
5.Duckencoder（编译攻击代码）   
6.Burner File BN03V104M.BIN  （2303固件）           
7.Psychson  （Badusb写入工具 https://github.com/adamcaudill/Psychson/）   
8.攻击payload  （想要执行的攻击代码）   
9.主控芯片查看工具  （可选，查看U盘主控芯片信息）

深入探索

文件大小转换

物流软件安全

JSON处理工具

1.下载&编译攻击代码   
https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads   
你可以使用HelloWorld测试，也可以用Downer下载exe并运行（第二次刷入比较麻烦，建议第一次就选好想要的payload

`java -jar encoder.jar -i payload.txt -o inject.bin //使用Duckencoder目录下的encoder生成payload为bin`  

2.生成固件&将攻击代码写入固件

`Psychson-master\firmware\build.bat //生成固件

EmbedPayload.exe C:\Psychson-master\inject.bin C:\Psychson-master\firmware\bin\fw.bin //将攻击代码写入生成的固件`  

3.将生成的固件写入U盘

`DriveCom.exe /drive=G /action=SetBootMode //设置U盘模式

深入探索

编码转换工具

企业安全咨询

漏洞修复方案

DriveCom.exe /drive=G /action=SendExecutable /burner=BN03V104M.BIN //2302固件

DriveCom.exe /drive=G /action=SendFirmware /burner=C:\Psychson-master\BN03V104M.BIN /firmware=C:\Psychson-master\firmware\bi\fw.bin //写入带有攻击代码的固件到芯片中`  

就不每个都传图了，直接上写入成功的图：[[![Badusb初玩步骤记录&疑问探讨](images/img-001-0d65783137aa.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201604/97f01459491407.jpg)](https://mrxn.net/content/uploadfile/201604/97f01459491407.jpg)

文件打包下载链接:链接:http://pan.baidu.com/s/1jIm22bk 密码:mrxn

疑问讨论：（玩过的大牛，都别躲着玩了，快出来科普问题，或说说猥琐的新姿势..）   
  
1.看漏洞原理，貌似是因为此芯片可编程为其他设备，如Usb键盘，打印机什么的，然后执行代码，那么U盘被编程为了其他设备，是否可以将恶意 exe写入进去，并在插入的时候执行自己存储的exe，而不是执行vbs下载（因为要考虑到内网或没网，执行一个内置并潜伏的程序应该能pass此场景）   
  
2.貌似它只是模拟了键盘去执行命令，那么在没有powershell的环境里如何做到隐藏执行？cmd有点显眼，虽然一闪而过   
  
3.如何即让它可以模拟执行命令又能像正常U盘一样存储东西（比较插上U盘结果没出现盘让人感觉有点不对）听说量产工具可以把U盘量产为不同的用途，不知道是否可以用在此处   
  
end：不想再折腾了。。第一次刷入helloworld成功后还小激动了会，然后发现第二次刷入新的payload出现了错误，在大牛的帮助下才成功使用短接方法重新刷入payload（在没有工具的情况下，拆开U盘橡胶外壳，不要问我是不是咬开的，我徒手撕的..）   
  
感谢90某大神的耐心回答，几个小时之前都没听说过U盘还有短接这东西。。（此文也是参考自他）   
  
下一个可能要感谢“一只猿”了，你们猜为什么   
  
enjoying..（ps：去目（nv）标（shen）那丢U盘吧）

原文：http://www.jeary.org/?post=51

漏洞扫描服务

- 标签：
- [#隐私窃取](https://mrxn.net/tag/%E9%9A%90%E7%A7%81%E7%AA%83%E5%8F%96)
- [#黑客](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2)
- [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
- [#badusb](https://mrxn.net/tag/badusb)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
