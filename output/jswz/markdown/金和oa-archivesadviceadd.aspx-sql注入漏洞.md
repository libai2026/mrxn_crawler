---
title: "金和OA ArchivesAdviceAdd.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesAdviceAdd-sqli.html
asset_dir: assets/金和oa-archivesadviceadd.aspx-sql注入漏洞
---

# 金和OA ArchivesAdviceAdd.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/4 13:28
- 469浏览
- [2评论](#comment)
- 15分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesAdviceAdd.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesAdviceAdd.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesAdviceAdd** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Expires = -1;
  if (this.Session["UserCode"] != null)
    this.strUserCode = this.Session["UserCode"].ToString();
  if (this.Request.QueryString["filetype"] != null)
    this.fileType = this.Request.QueryString["filetype"].ToString();
  if (this.Request.QueryString["fileid"] != null)
    this.fileID = this.Request.QueryString["fileid"].ToString();
  if (this.IsPostBack)
    return;
  this.ReadLocal();
  this.OutputAdvice();
}
```

参数 `filetype`、`fileid` 被带入`OutputAdvice`方法

```
public static DataTable GetAllAdvice(string fileType, string fileID)
{
  string QueryString = $"Select FileType,FileID,AdviceUserID,AdviceDetail,AdviceTime,UserName from ArchivesAdvice a,Users b where a.AdviceUserID = b.UserID and FileType like '%{fileType}%' and FileID = '{fileID}' order by AdviceTime";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesAdviceAdd.aspx/?fileid=1&filetype=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesAdviceAdd.aspx SQL注入漏洞](images/img-001-76793bc49a74.webp)](https://image.mrxn.net/b182b2adb6ad4f81a0ba00bba74d3c8f.webp)

成功延时 5 秒

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
