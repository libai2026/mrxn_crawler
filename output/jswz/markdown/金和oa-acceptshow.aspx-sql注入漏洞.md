---
title: "金和OA AcceptShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AcceptShow-sqli.html
asset_dir: assets/金和oa-acceptshow.aspx-sql注入漏洞
---

# 金和OA AcceptShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/5 08:11
- 634浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

漏洞扫描器

技术文章订阅

Nessus

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AcceptShow.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 AcceptShow.aspx 的源码，在 bin 目录下查找 JHBase.Web.accept.dll 将其进行反编译后找到 `AcceptShow` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.strAppId = this.Request["appid"].ToString();
  if (this.Request["id"] == null)
    return;
  this.strAcceptID = this.Request["id"].ToString();
  this.strVersion = Paper.GetGovVersion(this.strAppId, this.strAcceptID);
```

深入探索

网络安全培训

云安全解决方案

服务器安全服务

参数 `id` 需要满足不为空 即可进入 `Paper.GetGovVersion` 方法中

跟进 `GetGovVersion` 方法

```
public static string GetGovVersion(string strAppID, string strAppOID)
{
  string QueryString = $"select Version from JHOA_Approve_Instance where Instance_ID = (select Instance_ID from jhoa_approve where App_ID = '{strAppID}' and AppO_ID = '{strAppOID}')";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  return dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0 ? dataTable.Rows[0]["Version"].ToString() : "";
}
```

参数 `strAppID` 和 `strAppOID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.accept/AcceptShow.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

appid=SQLI_POC--/Temp/&id=-1
```

[![金和OA AcceptShow.aspx SQL注入漏洞](images/img-001-d70cbe93bdd1.webp)](https://image.mrxn.net/4b2dd2d62bc14d65a886a5db77c3dc89.webp)

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
