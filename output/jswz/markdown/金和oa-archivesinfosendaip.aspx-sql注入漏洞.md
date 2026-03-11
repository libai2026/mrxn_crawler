---
title: "金和OA ArchivesInfoSendAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesInfoSendAip-sqli.html
asset_dir: assets/金和oa-archivesinfosendaip.aspx-sql注入漏洞
---

# 金和OA ArchivesInfoSendAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/11 13:28
- 1952浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

防火墙软件

JSON处理工具

漏洞扫描服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesInfoSendAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesInfoSendAip.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesInfoSendAip** 的处理逻辑

深入探索

服务器安全服务

Docker加速服务

计算机安全

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

软件

安全运维咨询

安全工具开发

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesInfoSendAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesInfoSendAip.aspx SQL注入漏洞](images/img-001-40474946d839.webp)](https://image.mrxn.net/15e6eea8385844839e486f6d812eca5a.webp)

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
