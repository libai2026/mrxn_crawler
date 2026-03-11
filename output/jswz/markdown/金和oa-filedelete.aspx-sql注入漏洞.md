---
title: "金和OA FileDelete.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-accept-FileDelete-sqli.html
asset_dir: assets/金和oa-filedelete.aspx-sql注入漏洞
---

# 金和OA FileDelete.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/4 08:28
- 703浏览
- [0评论](#comment)
- 15分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `FileDelete.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 FileDelete.aspx 的源码，在 bin 目录下查找 JHBase.Web.accept.dll 将其进行反编译后找到 `FileDelete` 的处理逻辑

```
public class FileDelete : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    string str = this.Request["SlaveID"];
    if (str == null || str.IndexOf("/Temp/") < 0)
      return;
    UploadFile.DeleteTemp(str.ToString());
  }
```

参数 `SlaveID` 需要满足不为空且包含 `/Temp/` 字符串即可进入 `UploadFile.DeleteTemp` 方法中

跟进 `DeleteTemp` 方法

```
public static void DeleteTemp(string SlaveID)
{
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select FilePath from Files where FIleID in ('{SlaveID.Replace(",", "','")}')");
  string empty = string.Empty;
  Page page = new Page();
  for (int index = 0; index < ((InternalDataCollectionBase) dataTable.Rows).Count; ++index)
  {
    string str = dataTable.Rows[index][0].ToString().Replace("/Slaves/", "/Temp/");
    if (File.Exists(page.Server.MapPath(str.ToString())))
      File.Delete(page.Server.MapPath(str.ToString()));
  }
  ((MarshalByValueComponent) dataTable).Dispose();
}
```

参数 `SlaveID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.accept/FileDelete.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

SlaveID=SQLI_POC--/Temp/
```

[![金和OA FileDelete.aspx SQL注入漏洞](images/img-001-5b58a497c08d.webp)](https://image.mrxn.net/1561ff6e97644836a3e3ff3c64d3036f.webp)

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
