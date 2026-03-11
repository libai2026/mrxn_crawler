---
title: "分析一个安卓锁机APP"
source: https://mrxn.net/jswz/crack-Android-screenlock.html
asset_dir: assets/分析一个安卓锁机app
---

# 分析一个安卓锁机APP

[Mrxn](https://mrxn.net/author/1)- 发表于2017/1/4 15:05
- 5168浏览
- [20评论](#comment)
- 17分钟阅读

深入探索

Web安全课程

计算机安全

网络安全课程

---

其实这个样本是我在论坛上别人的求助帖子里看到的，就下载下来看一下：

- 首先这个[软件](#)大小就不对，45KB！其次是看在安装界面，注意右下角的不是【安装】而是【激活】，正常的软件安装都是显示安装。再看安装时系统的提醒，此软件需要的权限：
- 清除所有数据，恢复出厂设置；
- 更改屏幕解锁密码；
- 设置密码规则；
- 监视屏幕解锁次数；
- 锁定屏幕；这几条看着怎么都不想常见的APP安装时获取的权限吧

[[![分析一个安卓锁机APP](images/img-001-2dadf374acdd.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/7e591483516123.png)](https://mrxn.net/content/uploadfile/201701/7e591483516123.png)

深入探索

漏洞预警服务

安全研究报告

Windows安全工具

我们是测试嘛！真正在安装遇见这种APP时，请一定慎重！点击激活后，就是锁屏画面咯：[[![分析一个安卓锁机APP](images/img-002-d1c8913acce9.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/e91d1483516123.png)](https://mrxn.net/content/uploadfile/201701/e91d1483516123.png)

当然，图中的密码，计算方式是逆向此APP后得出的算法而已，接下来我就分析一下；

物流软件安全

深入探索

编码转换工具

文件大小转换

安全

首先是打开我们的Android逆向工具：Android killer，载入程序：

[[![分析一个安卓锁机APP](images/img-003-aad0b8dd9307.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/thum-120f1483516123.png)](https://mrxn.net/content/uploadfile/201701/120f1483516123.png)

然后我们是 java的开发工具查看java源码，图中的小红圈图标就是，打开后可以看到程序的结构和其中的密码设置算法（非常简单，就是取随机数加上设定的值）：

[[![分析一个安卓锁机APP](images/img-004-f10a9a669fe8.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/thum-e76a1483516640.png)](https://mrxn.net/content/uploadfile/201701/e76a1483516640.png)

其中关键的密码算法就是这段：

```
super.onCreate();
    this.pass = (()(Math.random() * 100000000));
    long l = this.pass + 100;
    Long localLong = new Long(l);
    this.passw = localLong;
    DU localDU1 = new DU("flower");
    this.des = localDU1;
```

其中的passw就是锁屏上的所谓序列号，解锁密码就是这个序列号加上 100，到这还没完，因为输入这个后，重启开机还得输入程序改变设置的pin码，在程序里面可以很清除的看到：

[[![分析一个安卓锁机APP](images/img-005-9e6057267cb2.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/thum-81271483516641.png)](https://mrxn.net/content/uploadfile/201701/81271483516641.png)

```
public class MyAdmin extends DeviceAdminReceiver
{
  @Override
  public CharSequence onDisableRequested(Context paramContext, Intent paramIntent)
  {
    String str = Integer.toString(2580);
    getManager(paramContext).lockNow();
    getManager(paramContext).resetPassword(str, 0);
    return super.onDisableRequested(paramContext, paramIntent);
  }
```

DeviceAdminReceiver就是安卓的设备管理器，通过这个设置的pin码，刚刚前面讲了，程序在安装时就获取了这个权限，所以在后面的卸载中也需要用到设备管理器才可以卸载的。接下来说一下怎么卸载：

首先我们在重启后需要输入刚刚从源码里分析得到儿pin码：2580，输入后就解锁进入桌面了：[[![分析一个安卓锁机APP](images/img-006-63399dc47c2d.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/7ebb1483517158.png)](https://mrxn.net/content/uploadfile/201701/7ebb1483517158.png)[[![分析一个安卓锁机APP](images/img-007-aba4e02539cb.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/7ba61483517158.png)](https://mrxn.net/content/uploadfile/201701/7ba61483517158.png)

### 注意：卸载的时候需要取消激活设备管理器，这时候还要在输入一次pin值，完了以后再确认一下是否卸载，去设置-应用，看看有没有该应用，有可能隐藏为系统应用。

[[![分析一个安卓锁机APP](images/img-008-78500379cc36.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/be0e1483517158.png)](https://mrxn.net/content/uploadfile/201701/be0e1483517158.png)

[[![分析一个安卓锁机APP](images/img-009-a453972d6781.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/44451483517158.png)](https://mrxn.net/content/uploadfile/201701/44451483517158.png)[[![分析一个安卓锁机APP](images/img-010-bdc9154a99a8.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/b51e1483517158.png)](https://mrxn.net/content/uploadfile/201701/b51e1483517158.png)

最后，就是这个程序的传播者，他说他是这个程序的开发者，简直可笑。。。曝光他：

[[![分析一个安卓锁机APP](images/img-011-d1b21a2f938f.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/thum-40241483517159.jpg)](https://mrxn.net/content/uploadfile/201701/40241483517159.jpg)[[![分析一个安卓锁机APP](images/img-012-024d39a84f52.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/thum-8a3a1483517159.jpg)](https://mrxn.net/content/uploadfile/201701/8a3a1483517159.jpg)

曝光他的QQ，手机号就行了，至于名字，地址等等就不暴露了，毕竟还是个中学生。。。希望他能够走向正途吧！

我们下回见！ Mrxn 04/1/2017

- 标签：
- [#木马](https://mrxn.net/tag/%E6%9C%A8%E9%A9%AC)
- [#逆向](https://mrxn.net/tag/%E9%80%86%E5%90%91)

---

文章目录

- [1.
  注意：卸载的时候需要取消激活设备管理器，这时候还要在输入一次pin值，完了以后再确认一下是否卸载，去设置-应用，看看有没有该应用，有可能隐藏为系统应用。](#toc-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
