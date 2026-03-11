---
title: "金和OA ArchivesShowSend.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowSend-sqli.html
asset_dir: assets/金和oa-archivesshowsend.aspx-sql注入漏洞
---

# 金和OA ArchivesShowSend.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/18 13:30
- 1927浏览
- [0评论](#comment)
- 25分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowSend.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesShowSend.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowSend** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  if (this.Session["UserCode"] != null)
    this.strUserCode = this.Session["UserCode"].ToString();
  this.Depts = new Role(this.strUserCode, "IOA_ArchivesModify").GetRoleDepts();
  if (this.Depts.Length > 0)
    ((HtmlControl) this.btnModify).Style.Add("display", "");
  else
    ((HtmlControl) this.btnModify).Style.Add("display", "none");
  this.strDeptList = new Role(this.strUserCode, "IOA_Distribute").GetRoleDepts();
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
GET /c6/Jhsoft.Web.Archives/ArchivesShowSend.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowSend.aspx SQL注入漏洞](images/img-001-e4ffb01c1cf3.webp)](https://image.mrxn.net/1b5163fe82e44426bfea0be68c2befcf.webp)

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
