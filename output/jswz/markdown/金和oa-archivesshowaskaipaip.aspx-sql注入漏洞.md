---
title: "金和OA ArchivesShowAskAipAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowAskAipAip-sqli.html
asset_dir: assets/金和oa-archivesshowaskaipaip.aspx-sql注入漏洞
---

# 金和OA ArchivesShowAskAipAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/17 13:32
- 1920浏览
- [0评论](#comment)
- 26分钟阅读

深入探索

文件大小转换

网络安全会议

漏洞修复方案

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowAskAipAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

安全认证考试

SQL注入防护

安全研究报告

根据 `ArchivesShowAskAipAip.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowAskAipAip** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
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

Nessus

Web安全书籍

恶意软件分析工具

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
GET /c6/Jhsoft.Web.Archives/ArchivesShowAskAipAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowAskAipAip.aspx SQL注入漏洞](images/img-001-7027ac278c5b.webp)](https://image.mrxn.net/34d97555b4fb4586aec839c827cfdc29.webp)

成功延时 12 秒

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
