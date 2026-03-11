---
title: "mac 无法卸载java xpc连接错误"
source: https://mrxn.net/jswz/java-update-uninstall-xpc-connection-error.html
asset_dir: assets/mac-无法卸载java-xpc连接错误
---

# mac 无法卸载java xpc连接错误

[Mrxn](https://mrxn.net/author/1)- 发表于2023/3/25 10:54
- 10812浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

卸载程序

安装

JDK

---

## 前言

出现这个错误一半是在mac的系统设置界面里的[Java](#)选项中，打开其Java控制面板后，进行更新的时候，当下载更新后，会提示你是否删除缓存之类，然后你确认是，就会报这个错误。

Java（编程语言）

[[![mac 无法卸载java xpc连接错误](images/img-001-8b09cde031f5.png)](https://mrxn.net/content/uploadfile/202303/thum-66fb1679713213.png)](https://mrxn.net/content/uploadfile/202303/66fb1679713213.png)

## 正文

这个问题有一段时间了，只是一直没有去管他，也不影响日常使用，日常使用切换[java](#)版本都是通过jenv来搞定的。这个系统的Java只影响哪些你通过双击打开jar这类操作有影响，当然你也可以通过从终端用命令行去打开jar文件。  
碰巧今天在双击使用某个jar文件时提示更新，就去更新，然后就出现了文章开头提到的粗错误，刚好今天有时间，就将其解决了。  
首先通过搜索可以找到的相关文章不多，其中在apple社区找到了两篇文章[1](https://discussionschinese.apple.com/thread/252990563)|[2](https://discussionschinese.apple.com/thread/253957688)

第1篇没有回答，第2篇文章中提到了一个简单的删除系统自带Java版本，但不彻底。下面说下如何彻底卸载Java，迂回解决这个报错 哈哈

Mac OS

```
sudo rm -rf /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin
sudo rm -rf /Library/PreferencePanes/JavaControlPanel.prefPane
sudo rm -rf ~/Library/Application\ Support/Oracle/Java
```

深入探索

传输层安全性协议

代码安全审计

Web安全课程

其中第二条中的 `PreferencePanes` 和 网上和 oracle 提到的也不一样，它们的多了一个字母s: `PreferencesPanes` ,这个根据自己的路径决定吧，毕竟版本差别不一样。

其次就是删除系统自带的那个旧版本

```
sudo rm -rf /Library/Java/JavaVirtualMachines/jdk*
```

然后重新去oracle下面新版dmg安装包重新安装即可。  
下载地址: <https://www.java.com/zh-CN/download/>  
卸载参考: <https://www.java.com/zh-CN/download/help/mac_uninstall_java.html>

其他参考  
<https://segmentfault.com/a/1190000042724793>  
<https://chiilabo.com/2021-10/java-update-uninstall-xpc-connection-error/>  
<https://cloud.tencent.com/developer/article/1680250>

Windows 操作系统

- 标签：
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.前言](#toc-1-)
- [2.正文](#toc-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
