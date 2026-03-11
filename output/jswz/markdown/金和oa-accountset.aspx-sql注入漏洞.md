---
title: "金和OA AccountSet.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AccountSet-sqli.html
asset_dir: assets/金和oa-accountset.aspx-sql注入漏洞
---

# 金和OA AccountSet.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/29 13:05
- 241浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

技术文章订阅

物流软件安全

漏洞预警服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AccountSet.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AccountSet.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AccountSet** 的处理逻辑

深入探索

Web安全书籍

编码转换工具

数据库

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack || string.IsNullOrEmpty(this.Request.QueryString["OperType"]) || string.IsNullOrEmpty(this.Request.QueryString["ID"]) || !string.op_Equality(this.Request.QueryString["OperType"], "Edit"))
    return;
  DataTable accInfo = this.Acc.GetAccInfo(this.Request.QueryString["ID"]);
```

要执行 `GetAccInfo` 方法，必须同时满足以下所有条件：

代码安全审计

1. 不是页面回发（`IsPostBack` 为 `false`）。
2. URL参数 `OperType` 的值必须为 "Edit"。
3. URL参数 `ID` 不能为空。

跟进`GetAccInfo`方法

```
public DataTable GetAccInfo(string id)
{
  return this.db.ExecSQLReDataTable("select * from EAI_Accounts where id=" + id);
}
```

参数`ID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/subClass/AccountSet.aspx/?ID=SQLI_POC&OperType=Edit HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AccountSet.aspx SQL注入漏洞](images/img-001-e0d3195aca8b.webp)](https://image.mrxn.net/f526c9347c614e419f047c4bd4929ba1.webp)

成功延时 4 秒

漏洞扫描服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
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
