---
title: "关于Google chrome浏览器无法启动更新检查的解决方法"
source: https://mrxn.net/jswz/chrome-update-error-code-4-0x80070005-system-level.html
asset_dir: assets/关于google-chrome浏览器无法启动更新检查的解决方法
---

# 关于Google chrome浏览器无法启动更新检查的解决方法

[Mrxn](https://mrxn.net/author/1)- 发表于2016/11/25 12:38
- 7603浏览
- [0评论](#comment)
- 4分钟阅读

深入探索

Google Chrome

安装

网页浏览器

---

因为自己的身体原因，几个月没有使用电脑，今天开机使用的时候想更新一下chrome浏览器，结果就出现这个错误：[[![关于Google chrome浏览器无法启动更新检查的解决方法](images/img-001-b1bce337fa86.png "点击查看原图")](https://mrxn.net/content/uploadfile/201611/02a21480049339.png)](https://mrxn.net/content/uploadfile/201611/02a21480049339.png)

检查更新时出错：无法启动更新检查（错误代码为 4: [0x80070005](https://support.google.com/chrome/answer/6315198?visit_id=1-636156446874269825-3305065930&rd=1) -- system level）。

网络浏览器

先说第一种解决方法：直接点击这串蓝色的数字，会自动跳转到Google的官方帮助站点，直接下载离线安装版，跟着操作就OK。

第二种，我们从提示出错的字面意思去理解它：无法启动更新检查，那么就有可能是检查更新服务没有启动，验证一下就好了：

```
win+R
services.msc
```

查看结果如下：

[[![关于Google chrome浏览器无法启动更新检查的解决方法](images/img-002-774ce1ba1156.png "点击查看原图")](https://mrxn.net/content/uploadfile/201611/29d21480049339.png)](https://mrxn.net/content/uploadfile/201611/29d21480049339.png)

果然是Google的更新服务被禁用了，我想可能是在使用优化[软件](#)优化的时候做的负优化 -\_-|| ，

计算机硬件

深入探索

漏洞修复方案

Windows安全工具

企业安全咨询

直接右键--属性--启动改为手动就OK了，在前往<chrome://help/> 更新就好了。

- 标签：
- [#google](https://mrxn.net/tag/google)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
