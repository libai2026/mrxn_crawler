---
title: "金和OA BorrowShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BorrowShow-sqli.html
asset_dir: assets/金和oa-borrowshow.aspx-sql注入漏洞
---

# 金和OA BorrowShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/20 13:28
- 346浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

数据库

SQL

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BorrowShow.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BorrowShow.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **BorrowShow** 的处理逻辑

深入探索

云安全解决方案

漏洞扫描器

Docker加速服务

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.ReadLocal();
  this.initDiv();
  if (!((Control) this).Page.IsPostBack)
  {
    this.strBorrID = this.Request["borrId"].ToString();
    ((Control) this).ViewState["borrid"] = (object) this.strBorrID;
    this.BoundGrid();
    this.Reading1.ModuleMessageID = this.strBorrID;
    this.Reading1.ModuleID = "IOA_Borrow";
  }
  else
    this.strBorrID = ((Control) this).ViewState["borrid"].ToString();
  this.initText();
}
```

深入探索

安全认证考试

编程语言教程

JSON处理工具

参数`id`被带入`initText`方法

```
private void initText()
{
  DataTable borrowInfo = ArchivesBorrow.GetBorrowInfo(this.strBorrID);
```

跟进`GetBorrowInfo`方法

```
public static DataTable GetBorrowInfo(string strBorrID)
{
  string QueryString = "select a.UserID,a.DeptID,BorrDate,BorrbackDate,DocIDs,b.UserName,c.DeptName from ArchivesBorrow a inner join Users b on a.UserID=b.UserID and b.UserType <> 2 inner join Department c on a.DeptID=c.DeptID where BorrID=" + strBorrID;
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/BorrowShow.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA BorrowShow.aspx SQL注入漏洞](images/img-001-263c2641eb07.webp)](https://image.mrxn.net/5d1856068b394f39a253a738cf51838c.webp)

成功延时 4 秒

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
