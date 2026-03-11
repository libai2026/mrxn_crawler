---
title: "金和OA ArchivesInfoAsk.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesInfoAsk-sqli.html
asset_dir: assets/金和oa-archivesinfoask.aspx-sql注入漏洞
---

# 金和OA ArchivesInfoAsk.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/9 13:22
- 405浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

安全运维咨询

编程语言教程

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesInfoAsk.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

JSON处理工具

物流软件安全

技术文章订阅

根据 `ArchivesInfoAsk.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesInfoAsk** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  this.ReadLocal();
  this.GetList();
  if (new GroupConfig().IsUseGroup)
  {
    DataTable outerGuidArchives = GovType.getOuterGUIDArchives("IOA_Ask", this.strArchID);
```

参数`id`被带入`getOuterGUIDArchives`方法

```
public static DataTable getOuterGUIDArchives(string strTypeName, string strFileId)
{
  string QueryString = " declare @strID varchar(50) ";
  if (string.op_Equality(strTypeName, "IOA_Ask"))
    QueryString = $"{QueryString} select @strID = OutSystemID from AskDoc left join Archives on AskDoc.ArchivesID=Archives.ArchivesID where Archives.ArchivesID='{strFileId}'" + " if( @strID is null) select @strID = ''" + " select @strID as 'OutSystemID'";
  if (string.op_Equality(strTypeName, "IOA_Accept"))
    QueryString = $"{QueryString} select @strID = OutSystemID from AcceptDoc left join Archives on AcceptDoc.ArchivesID=Archives.ArchivesID where Archives.ArchivesID='{strFileId}'" + " if( @strID is null) select @strID = ''" + " select @strID as 'OutSystemID'";
  if (string.op_Equality(strTypeName, "IOA_Send"))
    QueryString = $"{QueryString} select @strID = OutSystemID from SendDoc left join Archives on SendDoc.ArchivesID=Archives.ArchivesID where Archives.ArchivesID='{strFileId}'" + " if( @strID is null) select @strID = ''" + " select @strID as 'OutSystemID'";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

深入探索

文本剥离工具

安全工具开发

Docker加速服务

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesInfoAsk.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesInfoAsk.aspx SQL注入漏洞](images/img-001-0b1344ead81c.webp)](https://image.mrxn.net/09047e323aa7497e802d5d9ae5b634ab.webp)

成功延时 4 秒

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
