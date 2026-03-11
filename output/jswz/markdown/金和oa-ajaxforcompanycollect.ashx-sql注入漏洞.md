---
title: "金和OA AjaxForCompanyCollect.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForCompanyCollect-sqli.html
asset_dir: assets/金和oa-ajaxforcompanycollect.ashx-sql注入漏洞
---

# 金和OA AjaxForCompanyCollect.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/17 13:28
- 351浏览
- [0评论](#comment)
- 26分钟阅读

深入探索

技术文章订阅

SQL注入防护

网络安全会议

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForCompanyCollect.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

授权

云安全解决方案

Windows安全工具

根据 `AjaxForCompanyCollect.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForCompanyCollect** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["strType"];
  string str2 = context.Request["strCollectType"];
  string str3 = context.Request["strAppType"];
  string strYear = context.Request["strYear"];
  if (string.op_Equality(str1, "setGoBack"))
    return;
  if (string.op_Equality(str1, "getCollectList"))
  {
    string strTime = context.Request["strTime"];
    if (string.op_Equality(str3, "start"))
    {
      this.strSql = $"select * from BudgetCollectManage where (CollectState = 0 or CollectState = 1) and BudgetYear = {strYear} and BudgetTime = {strTime}";
      DataTable dataTable = this.db.ExecSQLReDataTable(this.strSql);
      if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
        context.Response.Write("no");
      else
        context.Response.Write(this.GetCompanyCollectList(strYear, strTime, ""));
    }
    else
    {
      string strCollectId = context.Request["strCollectId"];
      context.Response.Write(this.GetCompanyCollectList(strYear, "", strCollectId));
    }
  }
  else if (string.op_Equality(str1, "getNotCollect"))
  {
    if (string.op_Equality(str3, "start"))
    {
      string strTime = context.Request["strTime"];
      context.Response.Write(this.GetNotCollectNew(strYear, strTime));
    }
    else
    {
      string strAppId = context.Request["strCollectId"];
      context.Response.Write(this.GetNotCollectEdit(strAppId));
    }
  }
  else
  {
    if (!string.op_Equality(str1, "getCollectTime"))
      return;
    context.Response.Write(this.GetCollectTime(strYear));
  }
}
```

深入探索

安全研究报告

Docker加速服务

漏洞预警服务

根据`strType`的值进入不同的处理流程

代码安全审计

[![金和OA AjaxForCompanyCollect.ashx SQL注入漏洞](images/img-001-a8fef1b9e648.webp)](https://image.mrxn.net/98176366e0084cf6ac1289f574f6391e.webp)

当 `strType=getCollectList` `strAppType=start`时，`strYear`、`strTime`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

```
string strTime = context.Request["strTime"];
if (string.op_Equality(str3, "start"))
{
  this.strSql = $"select * from BudgetCollectManage where (CollectState = 0 or CollectState = 1) and BudgetYear = {strYear} and BudgetTime = {strTime}";
```

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Collect/Handlers/AjaxForCompanyCollect.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getCollectList&strTime=SQLI_POC&strAppType=start&strYear=2012
```

[![金和OA AjaxForCompanyCollect.ashx SQL注入漏洞](images/img-002-cb3ff3266cf8.webp)](https://image.mrxn.net/9ab52a7a397d49c1b182575c2c052318.webp)

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
