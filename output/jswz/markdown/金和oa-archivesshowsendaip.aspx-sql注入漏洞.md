---
title: "金和OA ArchivesShowSendAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowSendAip-sqli.html
asset_dir: assets/金和oa-archivesshowsendaip.aspx-sql注入漏洞
---

# 金和OA ArchivesShowSendAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/19 13:37
- 1903浏览
- [0评论](#comment)
- 26分钟阅读

深入探索

安全研究报告

JSON处理工具

SQL注入检测工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowSendAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

SQL

安全

计算机安全

根据 `ArchivesShowSendAip.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowSendAip** 的处理逻辑

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
GET /c6/Jhsoft.Web.Archives/ArchivesShowSendAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowSendAip.aspx SQL注入漏洞](images/img-001-be31c4d719fb.webp)](https://image.mrxn.net/4d38a1d0f9c3493481a1324b86fd2986.webp)

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
