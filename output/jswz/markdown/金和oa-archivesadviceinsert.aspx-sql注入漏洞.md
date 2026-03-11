---
title: "金和OA ArchivesAdviceInsert.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesAdviceInsert-sqli.html
asset_dir: assets/金和oa-archivesadviceinsert.aspx-sql注入漏洞
---

# 金和OA ArchivesAdviceInsert.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/5 13:31
- 545浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

安全研究工具

云安全解决方案

网络安全课程

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesAdviceInsert.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ArchivesAdviceInsert.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesAdviceInsert** 的处理逻辑

```
  protected void Page_Load(object sender, EventArgs e)
  {
    this.Response.Expires = -1;
    this.ReadLocal();
    if (this.Request.QueryString["filetype"] != null)
      this.fileType = this.Request.QueryString["filetype"].ToString();
    if (this.Request.QueryString["fileid"] != null)
      this.fileID = this.Request.QueryString["fileid"].ToString();
    DataTable templet = Templet.getTemplet("9", "1");
    if (templet != null && ((InternalDataCollectionBase) templet.Rows).Count > 0)
      this.fileName = "../Resource/GovTemplet/" + templet.Rows[0]["ModelName"].ToString();
    else
      this.Response.Write("<script>alert(\"没有反馈意见模板\")</script>");
    this.JhWOC2.FileURL = this.fileName;
    this.JhWOC2.FileTransURL = "../JHSoft.Web.CustomQuery/FileDownLoad.aspx?FilePath=" + this.fileName;
    this.JhWOC2.InitializationType = JhWOC.DocumentType.doc;
    DataTable allAdvice = ArchivesAdvice.GetAllAdvice(this.fileType, this.fileID);
```

深入探索

安全

VPN服务

软件

参数 `filetype`、`fileid` 被带入`GetAllAdvice`方法

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
GET /c6/Jhsoft.Web.Archives/ArchivesAdviceInsert.aspx/?fileid=1&filetype=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

文本剥离工具

安全运维咨询

Windows安全工具

[![金和OA ArchivesAdviceInsert.aspx SQL注入漏洞](images/img-001-3186fc9f673e.webp)](https://image.mrxn.net/e12e1c211b984e74ac25b6a9bfb9f08b.webp)

成功延时 5 秒

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
