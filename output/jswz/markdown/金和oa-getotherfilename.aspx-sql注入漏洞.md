---
title: "金和OA GetOtherFileName.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GetOtherFileName-sqli.html
asset_dir: assets/金和oa-getotherfilename.aspx-sql注入漏洞
---

# 金和OA GetOtherFileName.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/13 12:27
- 526浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

授权

Web安全课程

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetOtherFileName.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

SQL注入防护

传输层安全性协议

安全工具开发

根据 GetOtherFileName.aspx 的源码，在 bin 目录下查找 JHBase.Web.Menu.dll 将其进行反编译后找到 GetOtherFileName 的处理逻辑

```
public class GetOtherFileName : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    string SlaveID = this.Request["fileId"].ToString();
    string empty1 = string.Empty;
    string empty2 = string.Empty;
    string empty3 = string.Empty;
    UploadFile.GetFileInfo(SlaveID, ref empty1, ref empty2, ref empty3);
    this.Response.Write(empty1);
  }
```

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

参数`fileId` >> `SlaveID`被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /c6/JHBase.Web.Menu/GetOtherFileName.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileId=)SQLI_POC
```

[![金和OA GetOtherFileName.aspx SQL注入漏洞](images/img-001-1d0773fd4e8a.webp)](https://image.mrxn.net/7fe71b22d85046e39bcb58de648ae5c5.webp)

成功延时 5 秒

代码安全审计

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
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
