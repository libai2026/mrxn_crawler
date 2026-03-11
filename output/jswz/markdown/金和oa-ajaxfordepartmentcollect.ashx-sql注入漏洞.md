---
title: "金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AjaxForDepartmentCollect-sqli.html
asset_dir: assets/金和oa-ajaxfordepartmentcollect.ashx-sql注入漏洞
---

# 金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/18 13:32
- 301浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

编码转换工具

物流软件安全

安全认证考试

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AjaxForDepartmentCollect.ashx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AjaxForDepartmentCollect.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **AjaxForDepartmentCollect** 的处理逻辑

[![金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞](images/img-001-18c3172c35c2.webp)](https://image.mrxn.net/b1a16e774a34420984ac2abfbc3c3168.webp)

根据`strType`的值进入不同的处理流程

代码安全审计

[![金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞](images/img-002-79e9525fab08.webp)](https://image.mrxn.net/06ba1cdb396447e6a24a58432308b4eb.webp)

当 `strType=getHistoryList` 时，`strDeptId`、`strCollectType`被带入`GetCollectHistory`方法

```
protected string GetCollectHistory(string strYear, string strDepID, string strCollectType)
{
  string str = string.Empty;
  DataTable collectList = this.bcDao.GetCollectList(strYear, strDepID, strCollectType);
```

跟进`GetCollectList`方法

```
public DataTable GetCollectList(string strYear, string strDepID, string strCollectType)
{
  if (string.op_Equality(strCollectType, "Department"))
    this.strSql = $"select c.CollectYear,c.CollectTime,c.CollectMoney,d.DeptName,c.Subjects,c.CreateDate ,c.SubRemark\r\n                        from CollectList c \r\n                        left join Department d on c.DeptID = d.DeptID\r\n                        where c.CollectState = 0 and c.CollectYear = {strYear} and c.DeptID = {strDepID} order by c.CreateDate";
  if (string.op_Equality(strCollectType, "Center"))
    this.strSql = $"select * from CollectList c\r\n                        where c.CollectState = 0 and c.CollectType = 'Department' and c.CollectYear = {strYear}and c.DeptID in (select DeptID from Department where DeptParentID = {strDepID})";
  return this.db.ExecSQLReDataTable(this.strSql);
}
```

当**strCollectType**=**Department或Center**时，`strYear`和`strDeptId`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Collect/AjaxForDepartmentCollect.ashx HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

strType=getHistoryList&strDeptId=SQLI_POC&strCollectType=Department&strYear=2012
```

[![金和OA AjaxForDepartmentCollect.ashx SQL注入漏洞](images/img-003-0d621d68785a.webp)](https://image.mrxn.net/41965d1c7af74621a52e10a22dabf43c.webp)

成功延时 4 秒

漏洞预警服务

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
