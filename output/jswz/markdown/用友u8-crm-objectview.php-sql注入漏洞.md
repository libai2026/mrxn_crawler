---
title: "用友U8 CRM objectview.php SQL注入漏洞"
source: https://mrxn.net/jswz/yonyon-u8crm-pub-objectview-ID-sqli.html
asset_dir: assets/用友u8-crm-objectview.php-sql注入漏洞
---

# 用友U8 CRM objectview.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/6 08:26
- 1048浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

SQL注入检测工具

防火墙软件

云安全解决方案

---

# 漏洞简介

用友U8 CRM客户关系管理系统是一款专业的企业级CRM[软件](#)，旨在帮助企业高效管理客户关系、提升销售业绩和提供优质的客户服务。用友 U8 CRM客户关系管理系统 objectview.php 文件存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者通过漏洞执行任意SQL语句，调用xp\_cmdshell写入后门文件，执行任意代码，从而获取到服务器权限

软件

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V13

# fofa语法

> `title="用友U8CRM"`

# 漏洞分析

根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)通告

[![用友U8 CRM objectview.php SQL注入漏洞](images/img-001-4f6b7b32de12.webp)](https://image.mrxn.net/66502f10c66349b5922fb675fb5d1a52.webp)

可知漏洞原因为sql注入导致的命令注入攻击。

漏洞预警服务

深入探索

在线安全工具

Windows安全工具

网络安全课程

那直接看 `U8SOFT/turbocrm70/code/www/pub/objectview.php` 修复前后的差异

[![用友U8 CRM objectview.php SQL注入漏洞](images/img-002-644285979cb3.webp)](https://image.mrxn.net/dcd2413929de4dedb5678cc1ba91c3f7.webp)

可以看到修复版本是对 `getRealID` 方法增加了更安全的参数化处理sql语句，那直接看有那里调用了 `getRealID` 方法，找到如下调用

```
function getRealID($ID){
    $realID = $ID;
    global $gblDB;
    $sql="select account_id from tc_account where cLtcCustomerCode='$ID' and account_id <> cLtcCustomerCode";
    $rs = $gblDB->query($sql);
    if ($rs && $rs->fetchRecord())
    {
        $realID=$rs->getFieldValueByName("account_id");
    }
    $rs->close();
    return TRegisterID($realID);
}
......

$ObjType = TGetRequest("ObjType");
$ID = TRegisterID(TGetRequest("ID"));
if($ObjType == 1){
    $ID = getRealID(TGetRegID($ID));
}
```

深入探索

编码转换工具

技术文章订阅

安全认证考试

可以看到没有修复之前是当 `ObjType=1` 时， `getRealID` 方法是直接将 `$ID` 拼接进sql语句中，无任何过滤和校验，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

代码安全审计

# 漏洞复现

```
GET /pub/objectview.php?DontCheckLogin=1&ObjType=1&ID=1' HTTP/1.1
Host: u8crm.mrxn.net
```

# 参考

- `https://security.yonyou.com/#/patchInfo?identifier=dbed49af1ced41e89fcc67d35e5df6c9`

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
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
