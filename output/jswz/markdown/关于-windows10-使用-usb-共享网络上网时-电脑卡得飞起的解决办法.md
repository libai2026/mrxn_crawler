---
title: "关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法"
source: https://mrxn.net/jswz/how-to-Improve-the-fluency-of-use-usb-sharing-network.html
asset_dir: assets/关于-windows10-使用-usb-共享网络上网时-电脑卡得飞起的解决办法
---

# 关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法

[Mrxn](https://mrxn.net/author/1)- 发表于2016/5/11 13:26
- 16519浏览
- [22评论](#comment)
- 9分钟阅读

深入探索

计算机安全

安全

安全运维咨询

---

声明：以下内容来自于V2社区，个人收藏，如有侵权，还请告知，谢谢！

使用 USB 共享手机的网络时，电脑变得很卡，尤其是系统自带的应用，如打开网络与共享中心，使用 Cortana 搜索，甚至是在任何地方用系统自带输入法输入，都很卡！拔掉 USB 线之前卡掉的操作都瞬间完成了。 然而第三方[软件](#)并不受影响，比如我发这个帖子，我等了半分钟把输入法换成了手心，然后就非常顺畅的打完了字，发出来了，要使用自带输入法，特别是使用微软拼音中文状态下，大概标题还没输完。 有需要用 USB 共享网络的应该很少，不知道有没有人遇到同样的情况。我的手机是闲置的 MI4 ，当作免费的移动无线路由器

搜索引擎

系统是 win10 X64 10.0 版本是 10586 4 核 U 8G 内存 睿速 T9 256G 开机都是秒开，为毛我一插手机 USB 线，打开 USB 网络共享，电脑就卡成渣，但是 CPU 和内存都不怎么彪，这是嘛情况啊，各位有没有遇到过、、、？求解

通过搜索，说什么在设备管理中心禁用一下再启用这个网卡，可是还是没有效果.... 各位 V 友 有没有什么办法解决呢？或者是科普一下，这是什么原因！

## 解决办法：

设备管理器中，选择 usb 共享的那个网卡（一般是名字里有 NDIS 这几个字母的）， [[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-001-9cee93ba5633.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/05641462944522.png)](https://mrxn.net/content/uploadfile/201605/05641462944522.png)

深入探索

文本剥离工具

服务器安全服务

Web安全书籍

然后右键，更新驱动程序，然后选下边那一项（从计算机设备列表中选取）  ， 

[[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-002-bbd35d4bb95a.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/4a471462944522.png)](https://mrxn.net/content/uploadfile/201605/4a471462944522.png)  
然后去掉“显示兼容设备”的对钩，[[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-003-5ad989d08405.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/10fb1462944522.png)](https://mrxn.net/content/uploadfile/201605/10fb1462944522.png)

深入探索

传输层安全性协议

漏洞预警服务

编码转换工具

然后在列表左边找到“ Microsoft ”，然后在右边拉到最下边，选择“远程 NDIS 兼容设备”这个，[[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-004-fd2f38f40ed0.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/09dd1462944522.png)](https://mrxn.net/content/uploadfile/201605/09dd1462944522.png)

之后确定即可。

 [[![关于 windows10 使用 usb 共享网络上网时 电脑卡得飞起的解决办法](images/img-005-6cad39d5167b.png "点击查看原图")](https://mrxn.net/content/uploadfile/201605/82661462944522.png)](https://mrxn.net/content/uploadfile/201605/82661462944522.png)

**作者：杨晓恒**  
  
**链接：****<http://www.zhihu.com/question/35185870/answer/93712562>**  
  
**来源：知乎**  
  
**著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。**

- 标签：
- [#wifi](https://mrxn.net/tag/wifi)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

---

文章目录

- [1.
  解决办法：](#toc-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
