---
title: "【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上"
source: https://mrxn.net/jswz/dg-ghope-vm-gho-no-iso.html
asset_dir: assets/【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上
---

# 【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上

[Mrxn](https://mrxn.net/author/1)- 发表于2016/1/20 19:36
- 7164浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

硬盘

磁盘

虚拟系统

---

首先说一下，博主写这篇文章是因为博主在学习过程中恰好遇到了这个问题--如何将gho格式后缀的系统文件安装在空白的虚拟机上，并且最终解决了我的问题，所以在此小计一下。这时候系统文件是gho，没有安装菜单，不支持分区怎么办？那么看下面的方法，不需要iso虚拟机测试安装gho系统的方法.

还有一种情况是物理机安装了系统发现不对劲，怀疑是安装工具修改了系统，排查重装系统又太麻烦，就可以用虚拟机测试了.

软件

准备工作：gho文件，DiskGenius，GhostExp，两个[软件](#)的下载地址：<https://userscloud.com/lfbb6g8jv10m>  <http://pan.baidu.com/s/1eRcw5xC>

大致步骤我说一下，其中一些不需需要改变的步骤我就不说了，需要注意的地方和重要的地方我会贴图，详情请看图：

自定义创建：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-001-a200d16ef0aa.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/0d391453289955.png)](https://mrxn.net/content/uploadfile/201601/0d391453289955.png)

深入探索

企业安全咨询

恶意软件分析工具

安全研究报告

不需要加载光驱，选择稍后安装系统：

操作系统

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-002-32ee39c22872.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/2bf01453289955.png)](https://mrxn.net/content/uploadfile/201601/2bf01453289955.png)

这里可选择创建的虚拟系统的版本，这里是选择XP：

物流软件安全

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-003-3275bb2fefde.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/86291453289955.png)](https://mrxn.net/content/uploadfile/201601/86291453289955.png)

虚拟系统保存目录选择，可自定义，但是一定要记得保存的路径：

软件

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-004-ab39b82d0156.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/01b81453289956.png)](https://mrxn.net/content/uploadfile/201601/01b81453289956.png)[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-005-237353b07d14.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/30eb1453289956.png)](https://mrxn.net/content/uploadfile/201601/30eb1453289956.png)

创建完虚拟机后打开DG分区工具，打开虚拟[硬盘](#)文件，就是虚拟系统的文件：

操作系统

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-006-514b52df7c45.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/f0631453289956.png)](https://mrxn.net/content/uploadfile/201601/f0631453289956.png)

看好了，别选错了，一般就是你命名以为vdmk之类的结尾的：

硬盘驱动器

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-007-7ca560211183.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/4f8b1453289956.png)](https://mrxn.net/content/uploadfile/201601/4f8b1453289956.png)

这里只是作为演示，我就知分了一个区，在实际使用中，可以根据自己的需求来分区，然后格式化：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-008-c8b4023663a2.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/55f51453289956.png)](https://mrxn.net/content/uploadfile/201601/55f51453289956.png)

然后打开虚拟机的[磁盘](#)管理，加载到物理机Z盘：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-009-198d678b4b26.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/7b2d1453289956.png)](https://mrxn.net/content/uploadfile/201601/7b2d1453289956.png)

[选择虚拟机的C盘，去掉读写保护：](https://mrxn.net/content/uploadfile/201601/04241453289956.png)

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-010-2f6d0848d8ab.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/04241453289956.png)](https://mrxn.net/content/uploadfile/201601/04241453289956.png)

打开我的电脑就出现了Z盘：

操作系统

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-011-e4bb1f7a93ea.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/19451453289956.png)](https://mrxn.net/content/uploadfile/201601/19451453289956.png)

然后用gho镜像浏览器打开gho系统镜像文件，全选，右键提取到Z盘：

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-012-be74d3b625c9.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/28021453289956.png)](https://mrxn.net/content/uploadfile/201601/28021453289956.png)

**切记**--提取复制完后别忘了虚拟机磁盘管理取消共享的Z盘：

硬盘驱动器

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-013-beaba9446680.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/9b1f1453289956.png)](https://mrxn.net/content/uploadfile/201601/9b1f1453289956.png)

然后打开虚拟机电源启动虚拟系统，看见这个启动界面就是成功了..：如下图

计算机硬件

[[![【图文教程】如何将gho格式后缀的系统文件安装在空白的虚拟机上](images/img-014-023a81eb4f90.png "点击查看原图")](https://mrxn.net/content/uploadfile/201601/c6351453289955.png)](https://mrxn.net/content/uploadfile/201601/c6351453289955.png)

以上是vm虚拟机安装测试系统的方法只用到了虚拟机和另外两个小工具，并没有用任何iso文件或者是什么PE系统....

操作系统

掌握了这个方法以后遇到下载的gho就不用担心没法测试了.同时也方便大家在虚拟机安装gho格式的系统。不懂得可以评论留言，我看见了就会尽快回复。

- 标签：
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#windows](https://mrxn.net/tag/windows)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
