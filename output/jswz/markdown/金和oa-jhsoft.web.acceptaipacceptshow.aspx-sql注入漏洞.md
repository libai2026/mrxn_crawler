---
title: "金和OA JHsoft.Web.AcceptAip/AcceptShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AcceptAip-AcceptShow-sqli.html
asset_dir: assets/金和oa-jhsoft.web.acceptaipacceptshow.aspx-sql注入漏洞
---

# 金和OA JHsoft.Web.AcceptAip/AcceptShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/8 08:12
- 509浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

Nessus

编码转换工具

SQL注入检测工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AcceptShow.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 AcceptShow.aspx 的源码，在 bin 目录下查找 JHBase.Web.AcceptAip.dll 将其进行反编译后找到 `AcceptShow` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["id"] == null)
    return;
  this.strAcceptID = this.Request["id"].ToString();
  this.initPage();
  if (!((Control) this).Page.IsPostBack)
  {
    this.GetList();
    this.fillPage();
  }
  this.JHOfficeAip1.loadState = 1;
  this.JHOfficeAip1.mAFileType = "aip";
  if (string.op_Equality(this.strArchID, "0"))
  {
    this.strContentFiles = JHSoft.Upload.UploadFile.GetFileID("AcceptContent", this.strAcceptID);
    this.UploadFile1.ModuleID = "AcceptSlave";
    this.UploadFile1.ModuleMessageID = this.strAcceptID;
  }
```

参数 `id` 需要满足不为空 即可进入 `UploadFile.GetFileID` 方法中

跟进 `GetFileID` 方法

```
public static string GetFileID(string ModuleID, string ModuleMessageID)
{
  string QueryString = $"select fileID from files where ModuleID='{ModuleID}' and ModuleMessageID='{ModuleMessageID}'";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
```

参数 `ModuleMessageID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.AcceptAip/AcceptShow.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=SQLI_POC
```

[![金和OA JHsoft.Web.AcceptAip/AcceptShow.aspx SQL注入漏洞](images/img-001-054ff7658acd.webp)](https://image.mrxn.net/2b6f5e4576e543588e091c4f3d3b6e67.webp)

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

编程
