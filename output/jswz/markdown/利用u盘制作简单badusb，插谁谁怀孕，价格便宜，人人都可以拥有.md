---
title: "利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有"
source: https://mrxn.net/jswz/diy-myself-badusb.html
asset_dir: assets/利用u盘制作简单badusb，插谁谁怀孕，价格便宜，人人都可以拥有
---

# 利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有

[Mrxn](https://mrxn.net/author/1)- 发表于2016/4/1 13:34
- 26625浏览
- [28评论](#comment)
- 22分钟阅读

深入探索

Windows安全工具

在线安全工具

SQL注入检测工具

---

首先 来看一下 图(如果刷坏或者想更改Payload,需要短接39和40针，再用官方刷写工具刷新),注意红色箭头标志：

[[![利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有](images/img-001-d6c7b3dbf082.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201604/54de1459488860.jpg)](https://mrxn.net/content/uploadfile/201604/54de1459488860.jpg)

**0x00 前言**

关于Badusb可以参看这个视屏：http://v.qq.com/boke/page/l/g/w/l01425u2igw.html

不是很新的东西，其他作者已对此做过研究测试，本文仅用来记录操作过程，保存日志，说明细节。

**0x01参考资料**

> https://github.com/adamcaudill/Psychson   
> https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads   
> http://zone.wooyun.org/content/20001

**0x02环境搭建**

深入探索

编码转换工具

VPN服务

漏洞修复方案

1、硬件

```
U盘 ：东芝（TOSHIBA） 速闪系列 U盘 16GB （黑色） USB3.0 主控版本：Phison 2251-03 购买地址： http://item.jd.com/929732.html
```

2、[软件](#)

物流软件安全

Windows x64主机

（1）Java Runtime Environment ：Java环境，用于支持Duckencoder

（2）SDCC ：刷写U盘的环境，用于支持Psychson

（3）Visual Studio 2012 ：编译Psychson的开发环境

（4）Psychson ：BasUSB写入工具 （https://github.com/adamcaudill/Psychson）

（5）Burner File ：BN03V104M.BIN，必要的burner

（6）USB-Rubber-Ducky Payload ：编写Payload的参考代码 （https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads）

（7）Duckencoder ：用于编译Payload

（8）chipgenius 芯片检测工具 ：用于确定U盘型号

**0x03操作流程**

1、配置Payload

进入DuckEncoder文件夹

执行：

```
java -jar encoder.jar -i payload.txt -o inject.bin
```

说明：

```
encoder.jar：文件夹自带 
payload.txt：可参考USB-Rubber-Ducky Payload 
inject.bin：执行代码后生成的文件
```

2、生成固件

深入探索

安全研究报告

安全研究工具

文本剥离工具

执行：

```
Psychson-master\firmware\build.bat
```

生成fw.bin文件

3、将Payload写入fw.bin文件

执行：

```
EmbedPayload.exe inject.bin fw.bin
```

说明：

```
EmbedPayload.exe：编译EmbedPayload工程得来 
inject.bin：操作1生成 
fw.bin：操作2生成
```

4、将生成的固件写入U盘

（1）执行

```
DriveCom.exe /drive=E /action=SetBootMode
```

设置U盘模式

（2）执行

```
DriveCom.exe /drive=E /action=SendExecutable /burner=BN03V104M.BIN
```

操作burner

（3）执行

```
DriveCom.exe /drive=E /action=SendFirmware /burner=BN03V104M.BIN /firmware=fw.bin
```

将fw.bin刷入U盘

**0x04 小结**

刷入成功后，下次插入U盘会模拟键盘操作，自动执行Payload

**0x05 补充**

如果刷坏或者想更改Payload,需要短接39和40针，再用官方刷写工具刷新

相关工具以及国外的工具资料包请在这里下载：[[![利用U盘制作简单BadUSB，插谁谁怀孕，价格便宜，人人都可以拥有](images/img-002-d52be2001975.png "点击查看原图")](https://mrxn.net/content/uploadfile/201604/b2f81459489784.png)](https://mrxn.net/content/uploadfile/201604/b2f81459489784.png)

链接: http://pan.baidu.com/s/1jIm22bk 密码: mrxn

欢迎私聊博主个人定制哦！价格实惠，保你满意，远控女神？试卷？老师的秘密？报复？格盘？改后缀？木马？都可以！哈哈

我只负责制作，怎么用那是你的事儿！你也可以自己按照教程制作，喜欢折腾的慢慢折腾去吧！

- 标签：
- [#攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
- [#渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
- [#隐私窃取](https://mrxn.net/tag/%E9%9A%90%E7%A7%81%E7%AA%83%E5%8F%96)
- [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#badusb](https://mrxn.net/tag/badusb)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
