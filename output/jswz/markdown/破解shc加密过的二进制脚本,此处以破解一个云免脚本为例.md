---
title: "破解shc加密过的二进制脚本,此处以破解一个云免脚本为例"
source: https://mrxn.net/jswz/unshc-the-shc-decrypter.html
asset_dir: assets/破解shc加密过的二进制脚本,此处以破解一个云免脚本为例
---

# 破解shc加密过的二进制脚本,此处以破解一个云免脚本为例

[Mrxn](https://mrxn.net/author/1)- 发表于2017/1/23 20:23
- 8664浏览
- [0评论](#comment)
- 5分钟阅读

深入探索

数据库

SQL

漏洞扫描服务

---

首先简单的介绍一下shc:

计算机安全

shc是一个专业的加密shell[脚本](#)的工具.它的作用是把shell脚本转换为一个可执行的二进制文件，这个办法很好的解决了脚本中含有IP、密码等不希望公开的问题.

今天逛一个博客看见了他的一篇文章说的关于破解云免脚本的,评论里面很多人说破解不了骚逼汪的云免脚本,我就是试试而已.哈哈

Google一下就找到了在youtube上的一个视频: [UnSHc - decrypt shc \*.sh.x bash script](https://www.youtube.com/watch?v=tmHVhMuG-Vg)

然后在作者的博客和github找到了:Unshc脚本.一键破解,很方便,在此记录一下:

首先未破解时是二进制打开是这样:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-001-1b8a978dba9e.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/d42c1485174326.jpg)](https://mrxn.net/content/uploadfile/201701/d42c1485174326.jpg)

然后克隆Unshc脚本到本地:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-002-6dce7d259453.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/927a1485174326.jpg)](https://mrxn.net/content/uploadfile/201701/927a1485174326.jpg)

然后赋予脚本的执行权限后就可以看到相应使用方法:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-003-e0be2d5c0951.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/323f1485174326.jpg)](https://mrxn.net/content/uploadfile/201701/323f1485174326.jpg)

直接破解:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-004-efe6b5bb1989.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/02561485174325.png)](https://mrxn.net/content/uploadfile/201701/02561485174325.png)

破解后的:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-005-bd33e2f0ef60.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/89841485174326.jpg)](https://mrxn.net/content/uploadfile/201701/89841485174326.jpg)

Unshc 作者github和博客:

脚本语言

<https://github.com/yanncam/UnSHc>

<https://www.asafety.fr/unshc-the-shc-decrypter/>

利用好搜索.事半功倍! 下回见!

- 标签：
- [#shell](https://mrxn.net/tag/shell)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#Linux](https://mrxn.net/tag/Linux)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
