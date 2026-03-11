---
title: "金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesCatalogDocPrint-sqli.html
asset_dir: assets/金和oa-archivescatalogdocprint.aspx-sql注入漏洞
---

# 金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/6 13:30
- 500浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

漏洞修复方案

编码转换工具

文本剥离工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesCatalogDocPrint.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

云安全解决方案

Docker加速服务

网络安全会议

根据 `ArchivesCatalogDocPrint.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesCatalogDocPrint** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.language();
  string str = this.Request["DossID"].ToString();
  DataTable indexList = ArchivesCatalog.GetIndexList(str);
```

参数 `DossID` 被带入`GetAllAdvice`方法

```
public static DataTable GetIndexList(string DossID)
{
  string QueryString = $"SELECT DocNo,DocTitle,DocZH,docOwner,DocCreateDate,DocPage,DocMemo FROM ArchivesDoc where dossid='{DossID}' and DelFlag=0 order by DocNo";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesCatalogDocPrint.aspx/?fileid=1&filetype=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞](images/img-001-14098a41f17a.webp)](https://image.mrxn.net/573fef295f1f4558ada8e5ac24391945.webp)

成功延时 10 秒，执行两次

代码安全审计

[![金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞](images/img-002-2201906f3e8c.webp)](https://image.mrxn.net/6ca1bd319a884246915fe56af055cfe4.webp)

[![金和OA ArchivesCatalogDocPrint.aspx SQL注入漏洞](images/img-003-da799b2736cf.webp)](https://image.mrxn.net/948defc2e2114b20a30f98946e0cc085.webp)

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
