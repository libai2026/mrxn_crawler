---
title: "金和OA AcceptGetSourceFileName.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AcceptGetSourceFileName-sqli.html
asset_dir: assets/金和oa-acceptgetsourcefilename.aspx-sql注入漏洞
---

# 金和OA AcceptGetSourceFileName.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/7 08:05
- 587浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

漏洞扫描器

Nessus

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AcceptGetSourceFileName.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 AcceptGetSourceFileName.aspx 的源码，在 bin 目录下查找 JHBase.Web.AcceptAip.dll 将其进行反编译后找到 `AcceptGetSourceFileName` 的处理逻辑

```
public class AcceptGetSourceFileName : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    this.Response.Write(Accept.getSourceName(this.Request["strFileId"].ToString(), this.Request["strAppFlag"].ToString()));
  }
```

参数 `strFileId` 和 `strAppFlag` 传入 `Accept.getSourceName` 方法中

跟进 `getSourceName` 方法

深入探索

安全工具开发

恶意软件分析工具

漏洞修复方案

```
public static string getSourceName(string strFileId, string strAppFlag)
{
  string str = $"select FileName from dbo.Files where FileID='{strFileId}'";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
  return ((InternalDataCollectionBase) dataTable.Rows).Count > 0 ? dataTable.Rows[0][0].ToString() : string.Empty;
}
```

参数 `strFileId` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.AcceptAip/AcceptGetSourceFileName.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strFileId=SQLI_POC&strAppFlag=-1
```

深入探索

传输层安全性协议

网络安全课程

漏洞预警服务

[![金和OA AcceptGetSourceFileName.aspx SQL注入漏洞](images/img-001-3035e92a94a0.webp)](https://image.mrxn.net/7bfe442ee0b64ec690cc4e69028c193b.webp)

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
