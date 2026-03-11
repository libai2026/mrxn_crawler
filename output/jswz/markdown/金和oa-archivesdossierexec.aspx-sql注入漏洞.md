---
title: "金和OA ArchivesDossierExec.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesDossierExec-sqli.html
asset_dir: assets/金和oa-archivesdossierexec.aspx-sql注入漏洞
---

# 金和OA ArchivesDossierExec.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/7 13:30
- 402浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

漏洞扫描器

漏洞预警服务

网络安全课程

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesDossierExec.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

技术文章订阅

Docker加速服务

漏洞修复方案

根据 `ArchivesDossierExec.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesDossierExec** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  string strDossID = this.Request["id"].ToString();
  if (string.op_Equality(this.Request["op"].ToString(), "closeDossier"))
    JHSoft.Archives.ArchivesDossier.CloseDoss(strDossID);
  if (string.op_Equality(this.Request["op"].ToString(), "openDossier"))
    JHSoft.Archives.ArchivesDossier.OpenDoss(strDossID);
  if (string.op_Equality(this.Request["op"].ToString(), "update"))
    this.Response.Write(JHSoft.Archives.ArchivesDossier.getDossFlg(strDossID));
  if (!string.op_Equality(this.Request["op"].ToString(), "delete"))
    return;
  this.Response.Write(JHSoft.Archives.ArchivesDossier.getUsedDossFlg(strDossID));
}
```

深入探索

编程语言教程

物流软件安全

安全认证考试

根据op的值进入不同的处理逻辑

代码安全审计

当`op=CloseDoss`时，参数`id`被带入`CloseDoss`方法

```
public static void CloseDoss(string strDossID)
{
  string QueryString = $"update ArchivesDossier set DossFlg=1 where DossID in ('{strDossID.Replace(",", "','")}')";
  DBOperatorFactory.GetDBOperator().ExecSQLReInt(QueryString);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

其他几个处理逻辑差不多

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-001-fcb03d225873.webp)](https://image.mrxn.net/da5f717fa75941b8a5305face0b21606.webp)

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-002-758f54d744a4.webp)](https://image.mrxn.net/5c4aa1bd228e445a82c0819850567ce0.webp)

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-003-b1cf53067374.webp)](https://image.mrxn.net/2e786b178c26457687a76c5fd2e0863f.webp)

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesDossierExec.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesDossierExec.aspx SQL注入漏洞](images/img-004-d5d714250457.webp)](https://image.mrxn.net/97b7926cfdb849a8874d4b3c9f6748fa.webp)

成功延时 5 秒

漏洞扫描服务

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
