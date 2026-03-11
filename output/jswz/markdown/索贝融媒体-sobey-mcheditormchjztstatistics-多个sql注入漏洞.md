---
title: "索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-statistics-countJztMonthsDetailArticle-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjztstatistics-多个sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/16 08:16
- 517浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

安全研究工具

VPN服务

Windows安全工具

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/Jzt/statistics/countJztArticle、countJztTWArticle和countJztMonthsDetailArticle接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"
>
> 代码安全审计

# 漏洞分析

## countJztArticle

根据漏洞信息看下`mch/Jzt/statistics/countJztArticle`的实现逻辑

漏洞扫描服务

```
public Response countJztArticle(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "startTime",required = false) Long startTime, @RequestParam(value = "endTime",required = false) Long endTime, @RequestParam(value = "isTw",required = false,defaultValue = "0") String isTw, @RequestParam(value = "isRenYuan",required = false,defaultValue = "0") String isRenYuan, @RequestParam(value = "userCode",required = false) String userCode) {
    List args = new ArrayList();
    StringBuffer sqlBuffer = new StringBuffer("select zcnarticle.id ");
    sqlBuffer.append(" , (select zcchannel.channelname from zcchannel inner join zccatalog on zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" where zccatalog.ID = zcnarticle.catalogID) as channelName ");
    sqlBuffer.append(" , (select zcchannel.channelid from zcchannel inner join zccatalog on zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" where zccatalog.ID = zcnarticle.catalogID) as channelid ");
    sqlBuffer.append("  from zcnarticle  ");
    sqlBuffer.append(" , ( select  distinct zcnarticle.id as articleid from zcnarticle where 1=1 ");
    if (isTw.equals("0")) {
        SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    } else {
        SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_WRITE_STATUS_LIST);
    }

    if (!isRenYuan.equals("0")) {
        sqlBuffer.append(String.format(" and zcnarticle.createUserCode= '%s' ", userCode));
    }
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-001-df4931e0c420.webp)](https://image.mrxn.net/981c68908573488d997e0caa51384d61.webp)

代码一看就很明了了，当isRenYuan不等于0时，**userCode**无任何过滤或校验，被直接拼接在SQL语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

如果没有String.format，就不存在，因为默认的append方法底层是参数化查询。

编程

## countJztTWArticle

其实和上面的countJztArticle一样的处理逻辑

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-002-8c5ef393b254.webp)](https://image.mrxn.net/d831bcdc374f40819768ce830884255d.webp)

## countJztMonthsDetailArticle

深入探索

软件

文本剥离工具

SQL

和上面的countJztArticle一样的处理逻辑

漏洞扫描服务

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-003-097b39df2025.webp)](https://image.mrxn.net/bdb321b1ea7b4d98a5cdd69bf731f2af.webp)

# 漏洞复现

## countJztArticle

```
GET /sobey-mchEditor/js/..;/mch/Jzt/statistics/countJztArticle?siteCode=&token=&userCode=admin&channelId=1&isRenYuan=1&userCode='SQLI_POC HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-004-e760d250cba4.webp)](https://image.mrxn.net/9f2a7019b458492386125264842ca63f.webp)

成功利用报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据用户

## countJztTWArticle

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-005-674e03af47c2.webp)](https://image.mrxn.net/9cf37094730040d9800d960b587e2921.webp)

同样的[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)

## countJztMonthsDetailArticle

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/ 多个SQL注入漏洞](images/img-006-7a2ede42ca07.webp)](https://image.mrxn.net/e0c8d3ed847043989fb32390c73a2eb1.webp)

也是同样的[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.countJztArticle](#toc-4-1-)
- [4.2.countJztTWArticle](#toc-4-2-)
- [4.3.countJztMonthsDetailArticle](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.countJztArticle](#toc-5-1-)
- [5.2.countJztTWArticle](#toc-5-2-)
- [5.3.countJztMonthsDetailArticle](#toc-5-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
