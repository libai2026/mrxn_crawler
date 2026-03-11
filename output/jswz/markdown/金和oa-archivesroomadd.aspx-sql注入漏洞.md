---
title: "金和OA ArchivesRoomAdd.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesRoomAdd-sqli.html
asset_dir: assets/金和oa-archivesroomadd.aspx-sql注入漏洞
---

# 金和OA ArchivesRoomAdd.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/12 13:30
- 1925浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

物流软件安全

文件大小转换

漏洞修复方案

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesRoomAdd.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesRoomAdd.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesRoomAdd** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.language();
  this.id = this.Request["id"] != null ? this.Request["id"].ToString() : "0";
  DataTable dataTable = ArchivesRoom.searchArchives(this.id);
```

参数`id`被带入`searchArchives`方法

```
public static DataTable searchArchives(string strArchRID)
{
  string QueryString = $"select ArchRID,ArchRName,ArchRFather,ArchRSort from ArchivesRoom where ArchRID='{strArchRID}'";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

深入探索

Docker加速服务

传输层安全性协议

企业安全咨询

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesRoomAdd.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesRoomAdd.aspx SQL注入漏洞](images/img-001-858a118881de.webp)](https://image.mrxn.net/cc467c4466e444c9a365a0692bd89fa2.webp)

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
