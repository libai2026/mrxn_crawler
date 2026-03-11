---
title: "金和OA Jhsoft.Web.blog/XmlHttp.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-blog-XmlHttp-sqli.html
asset_dir: assets/金和oa-jhsoft.web.blogxmlhttp.aspx-sql注入漏洞
---

# 金和OA Jhsoft.Web.blog/XmlHttp.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/29 13:31
- 375浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

SQL注入防护

数据库

漏洞扫描服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.blog/XmlHttp.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `Jhsoft.Web.blog/XmlHttp.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.blog.dll` 将其进行反编译后找到 **XmlHttp** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Operation = this.Request.QueryString["Operation"].ToString();
  this.param1 = this.Request.QueryString["param1"].ToString();
  this.param2 = this.Request.QueryString["param2"].ToString();
  string operation = this.Operation;
  if (operation == null)
    return;
  if (!string.op_Equality(operation, "delPhoto"))
  {
    if (!string.op_Equality(operation, "delright"))
      return;
    this.GetDelRight();
  }
  else
    this.DelPhoto();
}
```

深入探索

编程语言教程

网络安全培训

云安全解决方案

当 `Operation=delPhoto` 时，参数`param1`被带入`DelPhoto`方法

```
public void DelPhoto()
{
  if (new JHSoft.Blog.Blog().DelPhoto(this.param1))
    this.Response.Write("ok");
  else
    this.Response.Write("No");
}
public bool DelPhoto(string PhotoID)
{
  bool flag = true;
  string QueryString = "update BlogPhotoAlbum set DelFlag=1 where photoAlbumId=" + PhotoID;
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  dbOperator.ExecSQLReInt(QueryString);
  if (dbOperator.IsError)
    flag = false;
  return flag;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.blog/XmlHttp.aspx/?Operation=delPhoto&param1=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA Jhsoft.Web.blog/XmlHttp.aspx SQL注入漏洞](images/img-001-93a68b1e2742.webp)](https://image.mrxn.net/16d845c2a88a4dc5b9a6c8f6b01f6b58.webp)

成功延时 4 秒

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
