---
title: "金和OA AjaxForCompanyBudgetDecompose.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForCompanyBudgetDecompose-sqli.html
asset_dir: assets/金和oa-ajaxforcompanybudgetdecompose.ashx-sql注入漏洞
---

# 金和OA AjaxForCompanyBudgetDecompose.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/25 13:05
- 284浏览
- [0评论](#comment)
- 39分钟阅读

深入探索

软件

数据库

sql

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForCompanyBudgetDecompose.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForCompanyBudgetDecompose.ashx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForCompanyBudgetDecompose** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["strType"];
  string strYear1 = context.Request["strYear"];
  if (string.op_Equality(str1, "getBudgetTime"))
    context.Response.Write(this.DataPeriodList(strYear1));
  else if (string.op_Equality(str1, "getBudgetManageInfo"))
  {
    string strTime = context.Request["strTime"];
    context.Response.Write(this.DataBudgetManageInfo(strYear1, strTime, context.Session["UserCode"].ToString()));
  }
  else if (string.op_Equality(str1, "getHistoryList"))
    context.Response.Write(this.BindHistoryList(strYear1, context.Session["UserCode"].ToString()));
  else if (string.op_Equality(str1, "saveBudget"))
  {
    string[] strArray = context.Request["strBudgetInfo"].Split(new char[1]
    {
      '@'
    });
if (string.op_Equality(strArray[0].Split(new char[1]
{
  '|'
})[5], "Company"))
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"select * from BudgetManage where BudgetType = 0 and CompanyBudget = '{context.Session["UserCode"].ToString()}'");
  if (dataTable == null || ((InternalDataCollectionBase) dataTable.Rows).Count == 0)
if (string.op_Equality(strArray[0].Split(new char[1]
{
  '|'
})[5], "Center"))
{
  DataTable dataTable = this.db.ExecSQLReDataTable($"select * from BudgetUserAndDept where BudgetType = 0 and UserID = '{context.Session["UserCode"].ToString()}'");
  if (dataTable == null || ((InternalDataCollectionBase) dataTable.Rows).Count == 0)
if (string.op_Equality(strArray[0].Split(new char[1]
{
  '|'
})[5], "Department"))
{
  bool flag = false;
  DataTable dataTable = this.db.ExecSQLReDataTable("select * from BudgetUserAndDept where BudgetType = 0");
  if (dataTable != null || ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
if (string.op_Inequality(strArray[0].Split(new char[1]
{
  '|'
})[5], "Company"))
{
  if (!this.bdDao.IsDecompose(strArray[0].Split(new char[1]
  {
    '|'
  })[5], strArray[0].Split(new char[1]{ '|' })[1], strArray[0].Split(new char[1]
else if (string.op_Equality(strDecompose[5].ToString(), "Center"))
{
  strContent = strContent.Replace("[Page]", "Department");
  DataTable dataTable = this.db.ExecSQLReDataTable($"select * from RelationshipUsers where DeptID = {strDeptId} and DeptLeader = 1");
```

深入探索

安全研究工具

安全认证考试

服务器安全服务

当 `strType=getBudgetTime` 时，**strYear**、**strDeptId**、**type**被带入`DataPeriodList`方法

```
protected string DataPeriodList(string strYear, string strDeptId, string type, string timeType)
{
  string str1 = string.Empty;
  DataTable budgetTime = this.bdDao.GetBudgetTime(strYear, strDeptId, type);
```

跟进`GetBudgetTime`方法

```
public DataTable GetBudgetTime(string strYear, string strDeptId, string strType)
{
  this.strSql = $"select distinct DecomposeTime from DecomposeList where DecomposeState = 0 and DecomposeYear = {strYear} and DecomposeType = '{strType}'";
  if (!string.IsNullOrEmpty(strDeptId))
  {
    BudgetDecomposeDao budgetDecomposeDao = this;
    budgetDecomposeDao.strSql = $"{budgetDecomposeDao.strSql} and DeptID in ({strDeptId})";
  }
  this.strSql += " order by DecomposeTime asc";
  return this.db.ExecSQLReDataTable(this.strSql);
}
```

参数**strYear**、**strDeptId**、**type**被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

整体执行流程如下，当中其他几个方法也存在同样的[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，就不赘述了

代码安全审计

[![金和OA AjaxForCompanyBudgetDecompose.ashx SQL注入漏洞](images/img-001-dea92ac793dc.webp)](https://image.mrxn.net/c211a36a54ab435e9ed222a424627cbc.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/AjaxForCompanyBudgetDecompose.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getBudgetTime&strDeptId=1&strYear=2012&type=SQLI_POC&TimeType=1
```

[![金和OA AjaxForCompanyBudgetDecompose.ashx SQL注入漏洞](images/img-002-03e806821ced.webp)](https://image.mrxn.net/c2cac9c36317471897b57e650f5b2358.webp)

成功延时 4 秒

漏洞修复方案

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
