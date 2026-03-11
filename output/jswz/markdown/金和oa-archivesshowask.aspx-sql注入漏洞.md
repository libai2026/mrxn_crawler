---
title: "金和OA ArchivesShowAsk.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowAsk-sqli.html
asset_dir: assets/金和oa-archivesshowask.aspx-sql注入漏洞
---

# 金和OA ArchivesShowAsk.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/16 13:38
- 1859浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

JSON处理工具

Nessus

防火墙软件

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowAsk.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesShowAsk.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowAsk** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  string UserID = "";
  if (this.Session["UserCode"] != null)
    UserID = this.Session["UserCode"].ToString();
  this.Depts = new Role(UserID, "IOA_ArchivesModify").GetRoleDepts();
  if (this.Depts.Length > 0)
    ((HtmlControl) this.btnModify).Style.Add("display", "");
  else
    ((HtmlControl) this.btnModify).Style.Add("display", "none");
  this.strDeptList = new Role(UserID, "IOA_Distribute").GetRoleDepts();
  this.ReadLocal();
  this.GetList();
```

深入探索

安全研究工具

服务器安全服务

Windows安全工具

参数`id`被带入`GetList`方法

```
private void GetList()
{
  DataTable archivesInfo = JHSoft.Archives.ArchivesDoc.getArchivesInfo(this.strArchID);
  if (((InternalDataCollectionBase) archivesInfo.Rows).Count > 0)
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

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesShowAsk.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowAsk.aspx SQL注入漏洞](images/img-001-4c2d89354287.webp)](https://image.mrxn.net/eb6b7ec39ea64045aa1588df050f673b.webp)

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
