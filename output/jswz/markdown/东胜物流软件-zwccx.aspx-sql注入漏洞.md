---
title: "东胜物流软件 ZWCCX.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-ZWCCX-sqli.html
asset_dir: assets/东胜物流软件-zwccx.aspx-sql注入漏洞
---

# 东胜物流软件 ZWCCX.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/3 08:28
- 283浏览
- [0评论](#comment)
- 23分钟阅读

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 Areas/Mobile/Views/WMS/ZWCCX.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

软件

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据 Areas/Mobile/Views/WMS/ZWCCX.aspx 的代码引用`<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="ZWCCX.aspx.cs" Inherits="DSWeb.Areas.Mobile.Views.WMS.ZWCCX" %>`，在dll中找到`DSWeb.Areas.Mobile.Views.WMS.ZWCCX`的逻辑实现

```
protected void Page_Load(object sender, EventArgs e)
{
  this.SetupHTML();
  string str = this.Request.QueryString["truckno"];
  str.Replace(",", "").Replace("'", "");
  ((HtmlInputControl) this.hdkeyword).Value = str;
}

private void SetupHTML()
{
  string str1 = this.Request.QueryString["truckno"];
  str1.Replace(",", "").Replace("'", "");
  if (string.op_Inequality(str1, ""))
  {
    string str2 = $"select distinct wo.DODATE TiHuoRiQi,\r\n                                               wod.STORAGENAME CangKu,\r\n                                               ic.ADDR DiZhi,\r\n                                               ic.TEL  DianHua\r\n                                        from  wms_out_detail wod\r\n                                        left join wms_out wo on wod.OUTBSNO = wo.BSNO \r\n                                        left join info_client ic on wod.STORAGENAME = ic.SHORTNAME\r\n                                        where wod.TRUCKNO = '{str1}' and wo.DODATE>=(GETDATE()-3) order by wo.DODATE desc";
    Database database = DatabaseFactory.CreateDatabase();
```

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)形成原因如下

SQL注入防护

1. **过滤失效**：代码尝试使用 `str1.Replace(",", "").Replace("'", "")` 过滤危险字符，但 `String.Replace()` 方法返回新字符串，必须将返回值赋值才有效。当前代码未赋值，导致过滤**完全无效**。

```
// 错误写法（当前代码）
str1.Replace(",", "").Replace("'", "");  // 无效！

// 正确写法应该是
str1 = str1.Replace(",", "").Replace("'", "");
```

1. **字符串拼接** **SQL**：使用字符串插值 `$"{str1}"` 直接将用户输入拼接到 SQL 语句中，未使用参数化查询。
2. **直接执行文本** **SQL**：通过 `ExecuteReader((CommandType) 1, commandText)` 执行，`CommandType` 为 1 即 `CommandType.Text`，直接执行拼接的 SQL 文本。

`truckno`参数的值被直接拼接在str2 SQL语句里，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /Areas/Mobile/Views/WMS/ZWCCX.aspx?truckno=1' HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 ZWCCX.aspx SQL注入漏洞](images/img-001-0f5624137ff2.webp)](https://image.mrxn.net/81a9af97c27a481daf0a9633451b8728.webp)

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
