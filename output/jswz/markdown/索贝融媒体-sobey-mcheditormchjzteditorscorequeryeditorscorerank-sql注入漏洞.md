---
title: "索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-jztEditorScore-queryEditorScoreRank-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjzteditorscorequeryeditorscorerank-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/18 08:30
- 552浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

Windows安全工具

传输层安全性协议

恶意软件分析工具

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/jztEditorScore/queryEditorScoreRank`的实现逻辑

```
@RequestMapping(
    value = {"/queryEditorScoreRank"},
    method = {RequestMethod.GET}
)
public Response queryEditorScoreRank(@RequestParam(value = "createStartTime",required = false) String createStartTime, @RequestParam(value = "endStartTime",required = false) String endStartTime, @RequestParam(value = "pageSize",required = false,defaultValue = "10") Integer pageSize, @RequestParam(value = "pageIndex",required = false,defaultValue = "0") Integer pageIndex, @RequestParam(value = "userName",required = false) String userName, @RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "targetUserType",required = false) String targetUserType, HttpServletRequest request) {
    QueryBuilder qb = new QueryBuilder(" select sum(zcncommoneditorscore.score) editeScoreTotal, count(distinct a.id) num, zcncommoneditorscore.targetUserCode , zcncommoneditorscore.targetUserName , zcncommoneditorscore.prop1 organizationName from zcnarticle a");
    if (!StringUtils.isEmpty(targetUserType)) {
        qb.append(String.format(JztEditorScoreServiceImpl.innerJoinTargetTypeScoreSQL, targetUserType));
    } else {
        qb.append(JztEditorScoreServiceImpl.innerJoinScoreSQL);
    }
```

深入探索

VPN服务

文本剥离工具

SQL

参数`targetUserType`使用`String.format`格式化后，无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/jztEditorScore/queryEditorScoreRank?siteCode=&targetUserType='SQLI_POC&token=&userCode=admin HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank SQL注入漏洞](images/img-001-9c4270a02225.webp)](https://image.mrxn.net/0051f454a6684a4a96b89e86cd9205d2.webp)

成功通过报错注入在响应回显数据库用户信息

代码安全审计

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
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
