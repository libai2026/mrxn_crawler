---
title: "金和OA ArchivesInfoAcceptAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesInfoAcceptAip-sqli.html
asset_dir: assets/金和oa-archivesinfoacceptaip.aspx-sql注入漏洞
---

# 金和OA ArchivesInfoAcceptAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/8 13:30
- 378浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

数据库

软件

网络安全会议

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesInfoAcceptAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

安全研究工具

恶意软件分析工具

安全工具开发

根据 `ArchivesInfoAcceptAip.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesInfoAcceptAip** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  this.ReadLocal();
  this.GetList();
  this.fillPage();
  this.UploadFile1.ModuleID = "ArchivesSlave";
  this.UploadFile1.ModuleMessageID = this.strArchID;
  this.UploadFile1.ReferenceFilePath = "../Control/";
  this.UploadFile1.ButtonAdd.Visible = false;
  this.UploadFile1.ButtonDel.Visible = false;
  this.UploadFile1.ButtonEditor.Visible = false;
  this.UploadFile1.ButtonLook.Visible = false;
  this.strContentFiles = JHSoft.Upload.UploadFile.GetFileID("ArchivesContent", this.strArchID);
  this.strAcceptPaperName = JHSoft.Archives.ArchivesDoc.getAcceptPaperName(this.strArchID).ToString();
}
```

参数`id`被带入`GetFileID`、`getAcceptPaperName`等方法

```
public static string GetFileID(string ModuleID, string ModuleMessageID)
{
  string QueryString = $"select fileID from files where ModuleID='{ModuleID}' and ModuleMessageID='{ModuleMessageID}'";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  StringBuilder stringBuilder = new StringBuilder();
  for (int index = 0; index < ((InternalDataCollectionBase) dataTable.Rows).Count; ++index)
    stringBuilder.Append(dataTable.Rows[index]["fileID"].ToString() + ",");
  return stringBuilder.Length > 0 ? stringBuilder.ToString().Substring(0, stringBuilder.ToString().Length - 1) : string.Empty;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

深入探索

Web安全课程

文本剥离工具

SQL注入防护

[![金和OA ArchivesInfoAcceptAip.aspx SQL注入漏洞](images/img-001-ec119abdc085.webp)](https://image.mrxn.net/154507e2bd03463dbe7e92eb56db56f6.webp)

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesInfoAcceptAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesInfoAcceptAip.aspx SQL注入漏洞](images/img-002-470722b3b6b6.webp)](https://image.mrxn.net/972ccd486dc84b06a00b0579a592aa94.webp)

成功延时 8 秒

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
