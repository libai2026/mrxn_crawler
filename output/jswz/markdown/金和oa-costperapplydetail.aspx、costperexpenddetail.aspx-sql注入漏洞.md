---
title: "金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CostPerApplyDetail-sqli.html
asset_dir: assets/金和oa-costperapplydetail.aspx、costperexpenddetail.aspx-sql注入漏洞
---

# 金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/21 13:31
- 275浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

编程语言教程

漏洞扫描器

计算机安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CostPerApplyDetail.aspx` 、`CostPerExpendDetail.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `CostPerApplyDetail.aspx` 的源码（与`CostPerExpendDetail.aspx` 相同），在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **CostPerApplyDetail** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (!((Control) this).Page.IsPostBack)
  {
    if (this.Request.QueryString["DeptID"] != null)
    {
      this.strDeptID = this.Request.QueryString["DeptID"].ToString();
      ((HtmlInputControl) this.hiddenDeptID).Value = this.strDeptID;
      this.txtDeptName.Text = this.cc.GetDeptName(this.strDeptID);
    }
    if (this.Request.QueryString["UserID"] != null)
    {
      this.strUserID = this.Request.QueryString["UserID"].ToString();
      ((HtmlInputControl) this.hiddenUserID).Value = this.strUserID;
      this.txtUserName.Text = this.cc.GetUserName(this.strUserID);
    }
  }
  this.DataBindData(1, this.page_size, (DataSet) null);
}
```

深入探索

物流软件安全

文件大小转换

技术文章订阅

**GetDeptName**

```
public string GetDeptName(string DeptID)
{
  string empty = string.Empty;
  DataTable dataTable = this.db.ExecSQLReDataTable($"select DeptName from Department where DeptID = '{DeptID}'");
  if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
    empty = dataTable.Rows[0]["DeptName"].ToString();
  return empty;
}
```

**GetUserName**

```
public string GetUserName(string UserID)
{
  string empty = string.Empty;
  DataTable dataTable = this.db.ExecSQLReDataTable($"select UserName from Users where UserID = '{UserID}'");
  if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
    empty = dataTable.Rows[0]["UserName"].ToString();
  return empty;
}
```

参数`DeptID`、`UserID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

深入探索

Docker加速服务

安全认证考试

网络安全培训

```
GET /c6/JHSoft.Web.CostControl/Cost/CostPerApplyDetail.aspx/?DeptID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞](images/img-001-1255b595344b.webp)](https://image.mrxn.net/992b205052ad45b4bbd7b693e9c3ad04.webp)

[![金和OA CostPerApplyDetail.aspx、CostPerExpendDetail.aspx SQL注入漏洞](images/img-002-4217b532d2d9.webp)](https://image.mrxn.net/50f9de4521024360b22920b1278da7b3.webp)

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
