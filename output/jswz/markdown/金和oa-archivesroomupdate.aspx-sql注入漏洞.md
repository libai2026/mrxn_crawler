---
title: "金和OA ArchivesRoomUpdate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesRoomUpdate-sqli.html
asset_dir: assets/金和oa-archivesroomupdate.aspx-sql注入漏洞
---

# 金和OA ArchivesRoomUpdate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/14 13:31
- 2030浏览
- [2评论](#comment)
- 12分钟阅读

深入探索

漏洞修复方案

授权

文件大小转换

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesRoomUpdate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesRoomUpdate.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesRoomUpdate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Expires = -1;
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.language();
  ((WebControl) this.txtUser).Attributes.Add("onclick", "SelectUsers()");
  this.id = this.Request["id"] != null ? this.Request["id"].ToString() : "0";
  if (((Control) this).Page.IsPostBack)
    return;
  DataTable dataTable = ArchivesRoom.searchArchives(this.id);
```

深入探索

服务器安全服务

安全工具开发

云安全解决方案

参数`id`被带入`searchArchives`方法

```
public static DataTable searchArchives(string strArchRID)
{
  string QueryString = $"select ArchRID,ArchRName,ArchRFather,ArchRSort from ArchivesRoom where ArchRID='{strArchRID}'";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesRoomUpdate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

安全研究工具

Windows安全工具

恶意软件分析工具

[![金和OA ArchivesRoomUpdate.aspx SQL注入漏洞](images/img-001-3a148306bb39.webp)](https://image.mrxn.net/4c5274c7370b4848ba373e9c08e97022.webp)

成功延时 2 秒

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
