---
title: "金和OA AjaxForBudgetDecompose.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForBudgetDecompose-sqli.html
asset_dir: assets/金和oa-ajaxforbudgetdecompose.ashx-sql注入漏洞
---

# 金和OA AjaxForBudgetDecompose.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/23 13:05
- 281浏览
- [0评论](#comment)
- 22分钟阅读

深入探索

漏洞修复方案

SQL注入检测工具

VPN服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForBudgetDecompose.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForBudgetDecompose.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForBudgetDecompose** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["strType"];
  string str2 = context.Request["strYear"];
  if (string.op_Equality(str1, "getBudgetTime"))
  {
    DataSet divertInformation = new CostManager().Get_Budget_PeriodDivertInformation(str2);
else
{
  string strTime = context.Request["strTime"];
  DataTable decomposeManageList = this.budgetDecomposeDao.GetBudgetDecomposeManageList(str2, strTime);
```

当 `action=getBudgetTime` 时，`strYear`被带入`Get_Budget_PeriodDivertInformation`方法

```
public DataSet Get_Budget_PeriodDivertInformation(string YearPeriod)
{
  return this.GetDS_BySQL($"{" Select Budget_PeriodManage.YearPeriod,Budget_PeriodManage.Period,Budget_PeriodDivert.Status " + " from Budget_PeriodManage " + " Left outer join Budget_PeriodDivert " + " on Budget_PeriodDivert.YearPeriod = Budget_PeriodManage.YearPeriod " + " and  Budget_PeriodDivert.Period = Budget_PeriodManage.Period "} where Budget_PeriodDivert.Status is null and Budget_PeriodManage.YearPeriod ='{YearPeriod}'" + " order by YearPeriod asc ,Period asc " + "   select Period from Budget_PeriodManage where getdate() between begindate and enddate ");
}
```

参数`strYear`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

否则**strYear**、**strTime**会被带入**GetBudgetDecomposeManageList**方法

```
public DataTable GetBudgetDecomposeManageList(string strYear, string strTime)
{
  this.strSql = $"select * from BudgetDecomposeManage b \r\n                    where b.BudgetState <> 3 and BudgetYear = {strYear} and BudgetTime = {strTime}";
  return this.db.ExecSQLReDataTable(this.strSql);
}
```

存在相同的[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Decompose/AjaxForBudgetDecompose.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getBudgetTime&strYear=SQLI_POC
```

[![金和OA AjaxForBudgetDecompose.ashx SQL注入漏洞](images/img-001-8a4f520aad1f.webp)](https://image.mrxn.net/6a3f2cc49a3445c98ef33713bc38099e.webp)

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
