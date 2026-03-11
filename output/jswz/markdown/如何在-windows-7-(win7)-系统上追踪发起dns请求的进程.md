---
title: "如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程"
source: https://mrxn.net/jswz/how-to-find-dns-query-process-on-win7.html
asset_dir: assets/如何在-windows-7-(win7)-系统上追踪发起dns请求的进程
---

# 如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程

[Mrxn](https://mrxn.net/author/1)- 发表于2024/7/6 23:12
- 5596浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

win7

ProcessOn

process-on

---

# 前言

在前面一篇[文章](https://mrxn.net/hacktools/DNSLookupView.html),我简单介绍了在 win8 及以上系统上使用 DNSLookupView 来监控系统 DNS 请求,本期就继续完成这个系列的 win7 部分,因为 xp 系统实在是太老了!

Windows 操作系统

# 正文

## 工具

> 工欲善其事, 必先利其器

使用工具有如下两个[软件](#)

- Microsoft Message Analyzer (MMA)
- Process Monitor (v2.9.6版本)

这两个软件的下载地址在文末参考里自行下载,我也会放一份在我的 [GitHub](https://mrxn.net/index.php?keyword=github "GitHub") RedTeam\_BlueTeam\_HW 仓库里.

## 第一步 首先禁用 DNS Client 服务

可以通过任务栏再打开 services 或者通过在 win7 启动窗口来输入 services.msc 回车后即可快速打开服务窗口

操作系统

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-001-14cf0e0df309.png)](https://mrxn.net/content/uploadfile/202407/thum-e3dd1720341004.png)](https://mrxn.net/content/uploadfile/202407/e3dd1720341004.png)

找到 DNS Client ,选择右键,选择 属性(properties),在属性窗口中,首先停止服务,然后将 启动类型(Startup type)修改为禁用(Disable),防止被其他进程启动.

物流软件安全

深入探索

xp

process

Client

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-002-79d2e70bdfb9.png)](https://mrxn.net/content/uploadfile/202407/thum-6b791720341004.png)](https://mrxn.net/content/uploadfile/202407/6b791720341004.png)

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-003-6d7ea669711f.png)](https://mrxn.net/content/uploadfile/202407/thum-3b6c1720341004.png)](https://mrxn.net/content/uploadfile/202407/3b6c1720341004.png)

DNS Client 的执行命令如下,这也是很多软件抓包的进程信息显示是如下  
C:\[Windows](#)\system32\svchost.exe -k NetworkService  
一直抓不到真正发起DNS请求的进程原因是在 [Windows 系统](#)中，大多数 [DNS 查询](https://mrxn.net/tag/DNS%E8%A7%A3%E6%9E%90 "DNS 查询")都是由 svchost.exe 中的 DNS 客户端服务进行的.

网络

## 第二步 使用 PM + MMA 抓包

对于 Process Monitor 在 win7 系统上需要使用老板本才可以使用.笔者这里采用的是 2.9.6 版本,而Microsoft Message Analyzer目前官网已经不能下载了,但是 GitHub 上有存档,笔者测试下载下来后在 win7 上是可以正常使用的.

Windows 操作系统

**⚠️注意⚠️**

> 下面的操作都是以管理员权限运行的软件

打开 Process Monitor 后,设置一下 filter 规则,将 Operation 设置为 UDP Send

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-004-a204dc6e5f03.png)](https://mrxn.net/content/uploadfile/202407/thum-02db1720341003.png)](https://mrxn.net/content/uploadfile/202407/02db1720341003.png)

再设置 只监听 网络 的部分,也就是下图红框中的部分,它两边的部分都取消监听

操作系统

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-005-3b2017c97b50.png)](https://mrxn.net/content/uploadfile/202407/thum-7f9e1720341003.png)](https://mrxn.net/content/uploadfile/202407/7f9e1720341003.png)

然后就可以抓到发起DNS请求的进程了,如下图所示

物流软件安全

[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-006-dcad14710cae.webp)](https://image.mrxn.net/d2ec5b2a4bea45caae9396f4e418d9c4.webp)

打开 Microsoft Message Analyzer 后 选择 New Session

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-007-20155292c387.png)](https://mrxn.net/content/uploadfile/202407/thum-9c421720341007.png)](https://mrxn.net/content/uploadfile/202407/9c421720341007.png)

然后选择 Live Trace ,并在这里选择使用场景,我们当然选择 网络了(Network),一般选择 Local Network Interfaces 即可.

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-008-f2e4d8c8b97d.png)](https://mrxn.net/content/uploadfile/202407/thum-09ec1720341006.png)](https://mrxn.net/content/uploadfile/202407/09ec1720341006.png)

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-009-60f3546fed60.png)](https://mrxn.net/content/uploadfile/202407/thum-ce151720341006.png)](https://mrxn.net/content/uploadfile/202407/ce151720341006.png)

选择好后,还可以配置使用那一张网卡(如果你有多张网卡),如下图所示,点击 Configure 后进入 Provider 即可设置网卡,且会显示网卡的详细信息,如名称,类型,IP地址等等.

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-010-c9305aa4b821.png)](https://mrxn.net/content/uploadfile/202407/thum-09ee1720341005.png)](https://mrxn.net/content/uploadfile/202407/09ee1720341005.png)

设置过滤规则,如下图所示,笔者设置为

```
DNS.QueryName contains "qq.com"
```

根据你的需求,自行修改,支持很多语法,和 Wireshark 差不多,且可通过tab 补全,提示很全.  
如果你在抓包中途需要修改过滤规则,也可以通过上面的 Edit Session 来修改场景和过滤规则等等.

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-011-53ef9bd6f4ea.png)](https://mrxn.net/content/uploadfile/202407/thum-f3f91720341005.png)](https://mrxn.net/content/uploadfile/202407/f3f91720341005.png)

当抓到符合你的过滤规则的数据后,会出现如下图所示的内容,图中三个地方均可展示信息信息,包括进程 PID 等信息

操作系统

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-012-638f32027167.png)](https://mrxn.net/content/uploadfile/202407/thum-ccb21720341008.png)](https://mrxn.net/content/uploadfile/202407/ccb21720341008.png)

其中 3 号标记的 PID 列字段,需要按下图所示设置,在列上右键选择 Add Column,然后选择 Unions 双击 PID 即可添加到列.

[[![如何在 Windows 7 (win7) 系统上追踪发起DNS请求的进程](images/img-013-3a581731f4aa.png)](https://mrxn.net/content/uploadfile/202407/thum-8b431720341008.png)](https://mrxn.net/content/uploadfile/202407/8b431720341008.png)

以上就是详细的完整内容,希望可以帮助到你!助你更快[溯源](https://mrxn.net/tag/%E6%BA%AF%E6%BA%90 "溯源")定位到恶意进程.

最后,记得再定位到进程处理完后,记得把 [DNS](https://mrxn.net/tag/DNS%E8%A7%A3%E6%9E%90 "DNS") Client 服务启用,并启动.不然很多服务没法通信.

# 参考

- <https://github.com/riverar/messageanalyzer-archive>
- <https://process-monitor.cn.uptodown.com/windows/download/20537>
- <https://github.com/Mr-xn/RedTeam_BlueTeam_HW>
- <https://stackoverflow.com/questions/10213765/identifying-pid-source-of-dns-request-windows-xp>

- 标签：
- [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
- [#windows](https://mrxn.net/tag/windows)

---

文章目录

- [1.前言](#toc-1-)
- [2.正文](#toc-2-)
- [2.1.工具](#toc-2-1-)
- [2.2.第一步 首先禁用 DNS Client 服务](#toc-2-2-)
- [2.3.第二步 使用 PM + MMA 抓包](#toc-2-3-)
- [3.参考](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
