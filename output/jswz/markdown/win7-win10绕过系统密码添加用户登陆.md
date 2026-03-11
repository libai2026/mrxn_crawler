---
title: "win7 win10绕过系统密码添加用户登陆"
source: https://mrxn.net/jswz/windows-password-by-pass.html
asset_dir: assets/win7-win10绕过系统密码添加用户登陆
---

# win7 win10绕过系统密码添加用户登陆

[Mrxn](https://mrxn.net/author/1)- 发表于2016/2/24 18:45
- 10715浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

Nessus

JSON处理工具

防火墙软件

---

[[![win7 win10绕过系统密码添加用户登陆](images/img-001-3a7b6052a0b3.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201602/799b1456312052.jpg)](https://mrxn.net/content/uploadfile/201602/799b1456312052.jpg)

[blue] 不使用任何工具/[软件](#)来绕过win7、win10的密码从而添加新账户/修改本身账户密码来登陆系统 ，这个方法在网上也有过，今天呢博主专门测试了一下，是可以的，所以发出来，共享。方便大家在忘记密码而又没有工具的时候登录系统。下面就开始吧：[/blue]

软件

0x001

首先我们让电脑重启下，并且还得让他进入修复模式

最简单的方法就是长按电源键，然后直到他强制关机，再开机，哇哦，进入修复模式了呢！

0x002

然后你就看到了非正常关机的修复界面，蓝底白字那个，我不用win10就不截图了，自己感受，然后别点重启，点高级设置！

0x003

然后，又有三个选项，不用管，看图看得懂吧？选择第二个，那个螺丝刀和扳手的自动排查图标！

0x004

这里windows会让你选择从镜像恢复或是命令行提示符，机智的你是不是肯定会选择命令提示符呢？

然后你就想执行命令了是吧？添加账号了是吧？提升为管理员了是吧？

呵呵。。。那我还写着文章干嘛？事实证明是没用的，应为这个命令行无法为正常windows系统添加账户（说的太深，自己理解去吧）

[[![win7 win10绕过系统密码添加用户登陆](images/img-002-030f51f3f82c.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201602/d0091456312140.jpg)](https://mrxn.net/content/uploadfile/201602/d0091456312140.jpg)

深入探索

文本剥离工具

SQL注入检测工具

网络安全课程

这个时候我们用命令行这样执行：

c:

cd Windows\System32\

rename sethc.exe bak\_sethc.exe

xcopy cmd.exe sethc.exe

exit

 嗯哼，打完收工。。。。明白了吧，把粘滞键改成cmd。

然后重启电脑，看到登录界面，要我输入密码？？？按五下shift，CMD弹出来了吧？呼呼。

这个时候，你可以去添加账户了，绝对是添加给当前系统的。

net user p0tt1 p0tt1666 /add

net loucalgroup administrators p0tt1 /add

然后？然后就进去了...进去了...去了...了...

[quote] 注：代码和过程其实都差不多，博主比较懒，不想打字，复制的，原文：<http://p0tt1.com/?post/1lyzhz> [/quote]

- 标签：
- [#密码](https://mrxn.net/tag/%E5%AF%86%E7%A0%81)
- [#攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
- [#windows](https://mrxn.net/tag/windows)
- [#绕过](https://mrxn.net/tag/%E7%BB%95%E8%BF%87)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
