---
title: "金和OA GetDictionary.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GetDictionary-sqli.html
asset_dir: assets/金和oa-getdictionary.aspx-sql注入漏洞
---

# 金和OA GetDictionary.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/13 08:25
- 677浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

恶意软件分析工具

代码安全审计

JSON处理工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetDictionary.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 GetDictionary.aspx 的源码，在 bin 目录下查找 JHBase.Web.Menu.dll 将其进行反编译后找到 GetDictionary 的处理逻辑

```
public class GetDictionary : JHSoft.Base.Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    DataTable dictionary = DictionaryContextMenu.GetDictionary(this.Request["DictionaryID"].ToString());
    if (((InternalDataCollectionBase) dictionary.Rows).Count > 0)
    {
```

跟进 `GetDictionary` 方法

```
public class DictionaryContextMenu
{
  public static DataTable GetDictionary(string ID)
  {
    return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"SELECT dictitem FROM DossierDictionary  where dictCollID='{ID}' order by dictsort");
  }
}
```

参数`DictionaryID` >> `ID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /c6/JHBase.Web.Menu/GetDictionary.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

MessageID='SQLI_POC
```

[![金和OA GetDictionary.aspx SQL注入漏洞](images/img-001-4f63ff2695b7.webp)](https://image.mrxn.net/9812a2989aec40628ed6c1abeed38682.webp)

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
