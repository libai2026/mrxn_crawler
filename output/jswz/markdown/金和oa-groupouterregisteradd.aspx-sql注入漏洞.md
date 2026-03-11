---
title: "金和OA GroupOuterRegisterAdd.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GroupOuterRegisterAdd-sqli.html
asset_dir: assets/金和oa-groupouterregisteradd.aspx-sql注入漏洞
---

# 金和OA GroupOuterRegisterAdd.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/15 08:29
- 502浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

SQL

服务器

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GroupOuterRegisterAdd.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

云安全解决方案

JSON处理工具

Docker加速服务

根据 `GroupOuterRegisterAdd.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **GroupOuterRegisterAdd** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request.QueryString["ID"] != null)
    this.strID = this.Request.QueryString["ID"].ToString();
  this.strPageTitle = !string.op_Equality(this.strID, string.Empty) ? "外部系统修改" : "外部系统添加";
  if (((Control) this).Page.IsPostBack || !string.op_Inequality(this.strID, string.Empty))
    return;
  this.ShowInfo(this.strID);
}
```

GET请求会将参数`ID`带入`ShowInfo`方法

```
private void ShowInfo(string systemID)
{
  DataTable systemBySystemId = OuterSystem.GetOuterSystemBySystemID(systemID);
```

继续跟进`GetOuterSystemBySystemID`方法

```
public static DataTable GetOuterSystemBySystemID(string systemID)
{
  string QueryString = $"select * from OuterSystem where System_ID='{systemID}'";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

深入探索

漏洞扫描服务

安全研究工具

Nessus

至此，就非常明了了，参数 `ID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/GroupOuterRegisterAdd.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GroupOuterRegisterAdd.aspx SQL注入漏洞](images/img-001-a5e4cecae89e.webp)](https://image.mrxn.net/70ae5c7e9e9246d7a5bdd940d48c8b36.webp)

成功延时 5 秒

代码安全审计

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
