---
title: "解决AMD双显卡win10开机黑屏很久，关闭ULPS"
source: https://mrxn.net/jswz/Disable-AMD-ULPS-to-improve-win10-openspeed.html
asset_dir: embedded-base64
---

# 解决AMD双显卡win10开机黑屏很久，关闭ULPS

[Mrxn](https://mrxn.net/author/1)- 发表于2016/12/7 13:46
- 8638浏览
- [1评论](#comment)
- 17分钟阅读

深入探索

软件

Microsoft Windows

安全工具开发

---

我的本本加了个256的[SSD](#)，一直用的win10 速度速度都还可以的，但是前两天自动更新后（AMD），我就发现电脑开机特别慢啊，之前都是几秒钟就到了刷指纹的界面，手指一扫就到[桌面](#)了，农企给我自动更新后，开机就要黑屏几十秒。。。。一开始还以为电脑中毒了，系统坏了啥的。。。折腾就不说了。

声卡与显卡

后来在搜索到了一些百度经验的文章，很多都没用。。。。其中有两篇说的就是按摩店（AMD）的双[显卡](#)，win10升级后开机慢。果然，禁用ulps后，开机立马好了，终于恢复了几秒钟！

### 注：这个方法只适用于双AND显卡的电脑哈，其他的没有测试，你也没有ulps这个东西，哈哈。

下面说一下方法哈：

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0000]
"EnableULPS"=dword:00000000

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0001]
"EnableULPS"=dword:00000000
```

把上面这段代码保存为后缀为reg的格式，比如ULPS\_Disable.reg 双击导入注册表，重启即可测试效果。

计算机驱动器和存储设备

下面这段代码就是开启ulps的，使用方法同上：

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0000]
"EnableULPS"=dword:00000001

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0001]
"EnableULPS"=dword:00000001
```

深入探索

Windows

windows

Windows Registry

这是作者原话：

```
This zip contains two files:

ULPS_Disable.reg
ULPS_Enable.reg

Basically it will just change the value of "EnableUlps" in the registry from "0" (disable) or "1" (enable) at locations:
[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\[b]0000[/b]]
[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\[b]0001[/b]]

Double click the one you want and reboot your computer.

ULPS stands for "Ultra Low Power State".

Disabling it allows your system to overclock. Specific drivers may still be required.

 -HTWingNut
```

深入探索

registry

电脑中毒

网络安全培训

百度经验的很多链接失效了，我通过搜索作者的名字，找到了他的网盘，哈哈，然后找到了这个，其实没有找到之前，我也解决了，自己手动搜索注册表修改一样的。不过有上面这两个脚本还是快多了啊！so,分享在这里，以方便有需要的朋友。

计算机硬件

- 标签：
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#windows](https://mrxn.net/tag/windows)
- [#注册表](https://mrxn.net/tag/%E6%B3%A8%E5%86%8C%E8%A1%A8)

---

文章目录

- [1.
  注：这个方法只适用于双AND显卡的电脑哈，其他的没有测试，你也没有ulps这个东西，哈哈。](#toc-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
