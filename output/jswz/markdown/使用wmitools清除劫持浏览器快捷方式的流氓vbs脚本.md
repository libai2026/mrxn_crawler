---
title: "使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本"
source: https://mrxn.net/jswz/WMITools-del_del_vbs_link.html
asset_dir: assets/使用wmitools清除劫持浏览器快捷方式的流氓vbs脚本
---

# 使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本

[Mrxn](https://mrxn.net/author/1)- 发表于2017/9/28 13:57
- 7373浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

代码安全审计

防火墙软件

云安全解决方案

---

昨天无聊下载了个小游戏玩...emmmm,结果今天发现我的浏览器都被强奸了...所有的浏览器快捷方式都被添加恶心的推广链接....[[![使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本](images/img-001-4498e7f05ab7.png "点击查看原图")](../content/uploadfile/201709/54d31506578489.png)](../content/uploadfile/201709/54d31506578489.png)

> http://hao643.com/?r=ggggg&m=e19
>
> 网络浏览器

就是这个煞笔...开始以为是常规的注册表修改,使用pchunter注册表搜索常见的位置没有发现...那就Google搜索吧...发现了下面几个帖子,使用WMITools成功删除了此流氓...瞬间开心好多...估计也会有人不小心中招,在此记录一下,一是自己记性不好,备忘录.其次是万一博客读者遇到了看了这篇文章可以帮助到你们.也是一件好事.

深入探索

企业安全咨询

Web安全书籍

服务器安全服务

下载WMITools:<https://pan.lanzou.com/1741009/>

然后去WMITools的安装目录,默认是:

C:\Program Files (x86)\WMI Tools\

直接以管理员的身份打开WMI Event Viewer,然后删除这个事件,取消任务栏的快捷方式,修改快捷方式里被添加的链接后,重新固定到任务栏即可...[[![使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本](images/img-002-3fb1f2607838.png "点击查看原图")](../content/uploadfile/201709/aa3c1506578489.png)](../content/uploadfile/201709/aa3c1506578489.png)[[![使用WMITools清除劫持浏览器快捷方式的流氓vbs脚本](images/img-003-f65992f196e7.png "点击查看原图")](../content/uploadfile/201709/3fa41506578489.png)](../content/uploadfile/201709/3fa41506578489.png)

其他详细的解释请看下面的链接:

脚本语言

2008年的关于这个流氓方式的始末:<http://bbs.myhack58.com/read.php?tid-185642-uid-1515.html>

2012年一位前辈发现的这个方法:<http://blog.sina.com.cn/s/blog_8627ac3c010195ri.html>

[Script](#) Text里面就是vb[脚本](#),具体的事例可以看这里:<https://pastebin.com/x1da51N3>

到此完毕.下次见.Mrxn\_posted\_on\_mrxn.net\_2017\_09\_28

- 标签：
- [#脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
