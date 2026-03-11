---
title: "金和OA BookUpdate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/Jhsoft-BookUpdate-sqli.html
asset_dir: assets/金和oa-bookupdate.aspx-sql注入漏洞
---

# 金和OA BookUpdate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/21 14:13
- 564浏览
- [0评论](#comment)
- 14分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BookUpdate.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

深入探索

文件大小转换

VPN服务

授权

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BookUpdate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.AddressBook.dll` 将其进行反编译后找到 **BookUpdate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.userid = this.Request.QueryString["id"].ToString();
  DataTable dt = DataTableToXml.search(this.userid);
```

深入探索

安全运维咨询

SQL

网络安全培训

参数 `id` 被带入`DataTableToXml.search`方法

```
public static DataTable search(string id)
{
  string QueryString = $"select  UserName,DeptName,PosiName,UserTel,UserMobileTelePhone,dossvalue,UserID,gangwei=(select top 1 staname from dbo.station where staid in (select sta_id from dbo.JHHR_Register where reg_code=v.UserID )) from [vw_AddressBookPub] v left join (select * from dossiervalue where dossierfieldid=24) d on v.userid=d.regcode where DeleteFlag=0 and userid='{id}'";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

至此，就非常明了了，`id` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddressBook/BookUpdate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA BookUpdate.aspx SQL注入漏洞](images/img-001-9348d3fa9550.webp)](https://image.mrxn.net/d0b5302541324f51b270a09875b1a783.webp)

成功延时 10 秒（执行两次）

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
