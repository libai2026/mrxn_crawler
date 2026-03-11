---
title: "金和OA ArchivesInfoAskAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesInfoAskAip-sqli.html
asset_dir: assets/金和oa-archivesinfoaskaip.aspx-sql注入漏洞
---

# 金和OA ArchivesInfoAskAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/10 13:25
- 1949浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

服务器安全服务

漏洞扫描器

授权

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesInfoAskAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesInfoAskAip.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesInfoAskAip** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  this.ReadLocal();
  this.GetList();
```

参数`id`被带入`GetList`方法

深入探索

Docker加速服务

安全工具开发

Web安全课程

```
private void GetList()
{
  DataTable archivesInfo = JHSoft.Archives.ArchivesDoc.getArchivesInfo(this.strArchID);
```

跟进`getArchivesInfo`方法

```
public static DataTable getArchivesInfo(string archID)
{
  Page page = new Page();
  StringBuilder stringBuilder = new StringBuilder();
  if (page.GroupConfig.IsUseGroup)
    stringBuilder.Append("select ArchivesType,ArchivesTitle,[dbo].[fn_FromOuterDeptIDGetOuterSystemName](SubDeptID,ArchivesFrom) as ArchivesFrom,ArchivesKey,ArchivesWH,a.SecretID,SecretName,");
  else
    stringBuilder.Append("select ArchivesType,ArchivesTitle,ArchivesFrom,ArchivesKey,ArchivesWH,a.SecretID,SecretName,");
  stringBuilder.Append("a.ExigenceID,ExigenceName,TypeName,ArchivesFs,ArchivesBH,DeptName,SubDate,UserName,");
  stringBuilder.Append("ArchivesZsdw,ArchivesCsdw,ArchivesDate,ArchivesMan,ArchivesFj,FileName,ArchivesSource,DossID,");
  stringBuilder.Append("ArchivesGD,Field1,Field2,Field3,Field4,Field5,Field6,Field7,Field8,Field9,Field0,SubTime,AskMoney,DocID ");
  stringBuilder.Append("FROM Archives a left join Secret s on a.SecretID=s.SecretID ");
  stringBuilder.Append($"left join Exigence e on e.ExigenceID=a.ExigenceId where ArchivesID='{archID}'");
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(stringBuilder.ToString());
}
```

深入探索

安全运维咨询

JSON处理工具

云安全解决方案

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesInfoAskAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesInfoAskAip.aspx SQL注入漏洞](images/img-001-1bc62260641f.webp)](https://image.mrxn.net/5fe912f88805403ba1c2009e459c07e5.webp)

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
