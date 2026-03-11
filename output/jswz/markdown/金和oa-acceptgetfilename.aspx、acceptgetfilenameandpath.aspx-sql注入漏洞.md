---
title: "金和OA AcceptGetFileName.aspx、AcceptGetFileNameAndPath.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AcceptAcceptGetFileName-AcceptGetFileNameAndPath-sqli.html
asset_dir: assets/金和oa-acceptgetfilename.aspx、acceptgetfilenameandpath.aspx-sql注入漏洞
---

# 金和OA AcceptGetFileName.aspx、AcceptGetFileNameAndPath.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/9 08:15
- 649浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

数据库

软件

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AcceptGetFileName.aspx` 和 `AcceptGetFileNameAndPath.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 AcceptGetFileName.aspx 的源码，在 bin 目录下查找 JHBase.Web.accept.dll 将其进行反编译后找到 `AcceptGetFileName` 的处理逻辑

```
public class AcceptGetFileName : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    string SlaveID = this.Request["fileId"].ToString();
    string empty1 = string.Empty;
    string empty2 = string.Empty;
    string empty3 = string.Empty;
    UploadFile.GetFileInfo(SlaveID, ref empty1, ref empty2, ref empty3);
```

深入探索

编程语言教程

Web安全课程

编码转换工具

参数 `SlaveID` 带入进入 `UploadFile.GetFileInfo` 方法中

跟进 `GetFileInfo` 方法

```
public static void GetFileInfo(
  string SlaveID,
  ref string FilePath,
  ref string FileName,
  ref string FileType)
{
  string QueryString = $"select FilePath,[FileName],FileType from  Files where FileID in ({SlaveID})";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  if (((InternalDataCollectionBase) dataTable.Rows).Count <= 0)
    return;
  FileName = dataTable.Rows[0][nameof (FileName)].ToString();
  FileType = dataTable.Rows[0][nameof (FileType)].ToString();
  FilePath = dataTable.Rows[0][nameof (FilePath)].ToString();
}
```

参数 `SlaveID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

JHsoft.Web.AcceptAip 下的 AcceptGetFileName 也存在同样的问题

代码安全审计

[![金和OA AcceptGetFileName.aspx、AcceptGetFileNameAndPath.aspx SQL注入漏洞](images/img-001-8b4b79d29ee5.webp)](https://image.mrxn.net/9c6113cbff95489c88a63aeb00cce53b.webp)

AcceptGetFileNameAndPath.aspx 也是如此

深入探索

安全认证考试

网络安全会议

计算机安全

[![金和OA AcceptGetFileName.aspx、AcceptGetFileNameAndPath.aspx SQL注入漏洞](images/img-002-37ec6578ac1b.webp)](https://image.mrxn.net/6b7b08d04ea848ac81f80c2136f05fb1.webp)

# 漏洞复现

## AcceptGetFileName.aspx

```
POST /c6/Jhsoft.Web.Accept/AcceptGetFileName.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileId=SQLI_POC
```

[![金和OA AcceptGetFileName.aspx、AcceptGetFileNameAndPath.aspx SQL注入漏洞](images/img-003-38ea48959281.webp)](https://image.mrxn.net/a5d885987f7841bb83f5f19122a2cdda.webp)

成功延时 5 秒

漏洞扫描服务

## AcceptGetFileNameAndPath.aspx

```
POST /c6/Jhsoft.Web.Accept/AcceptGetFileNameAndPath.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileId=SQLI_POC
```

[![金和OA AcceptGetFileName.aspx、AcceptGetFileNameAndPath.aspx SQL注入漏洞](images/img-004-254e7289a243.webp)](https://image.mrxn.net/eef4368412d441a38e5bbdf967e3d986.webp)

同样是可以延时 5 秒

数据管理

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
- [5.1.AcceptGetFileName.aspx](#toc-5-1-)
- [5.2.AcceptGetFileNameAndPath.aspx](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
