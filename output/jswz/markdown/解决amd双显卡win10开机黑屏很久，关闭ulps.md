---
title: "解决AMD双显卡win10开机黑屏很久，关闭ULPS"
source: https://mrxn.net/jswz/Disable-AMD-ULPS-to-improve-win10-openspeed.html
asset_dir: embedded-base64
---

我的本本加了个256的SSD，一直用的win10 速度速度都还可以的，但是前两天自动更新后（AMD），我就发现电脑开机特别慢啊，之前都是几秒钟就到了刷指纹的界面，手指一扫就到桌面了，农企给我自动更新后，开机就要黑屏几十秒。。。。一开始还以为电脑中毒了，系统坏了啥的。。。折腾就不说了。

芯片与处理器

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

把上面这段代码保存为后缀为reg的格式，比如ULPS\_Disable.reg 双击导入[注册表](https://mrxn.net/tag/%E6%B3%A8%E5%86%8C%E8%A1%A8 "标签：注册表")，重启即可测试效果。

声卡与显卡

下面这段代码就是开启ulps的，使用方法同上：

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0000]
"EnableULPS"=dword:00000001

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318}\0001]
"EnableULPS"=dword:00000001
```

深入探索

网络安全

博客资源与服务

数据管理

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

百度经验的很多链接失效了，我通过搜索作者的名字，找到了他的网盘，哈哈，然后找到了这个，其实没有找到之前，我也解决了，自己手动搜索[注册表](https://mrxn.net/tag/%E6%B3%A8%E5%86%8C%E8%A1%A8 "标签：注册表")修改一样的。不过有上面这两个脚本还是快多了啊！so,[分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB "标签：分享")在这里，以方便有需要的朋友。

Windows 操作系统
