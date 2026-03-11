---
title: "Western Digital My Cloud NAS login_checker.php、wto_check 权限绕过漏洞"
source: https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-login_checker-authbypass.html
asset_dir: assets/western-digital-my-cloud-nas-login_checker.php、wto_check-权限绕过漏洞
---

# Western Digital My Cloud NAS login\_checker.php、wto\_check 权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/3 08:18
- 734浏览
- [0评论](#comment)
- 27分钟阅读

深入探索

SQL

Western-Digital-My-Cloud-NAS

验证

---

# 漏洞简介

Western Digital My Cloud NAS是美国西部数据（Western Digital）公司的一款应用广泛的网络连接云存储设备，可用于托管文件，并自动备份和同步该文件与各种云和基于Web的服务。Western Digital My Cloud NAS `login_checker.php` 接口文件未对用户会话进行严格验证，存在[身份验证绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)漏洞，攻击者可通过构造恶意 Cookie 绕过身份认证机制，直接获取普通用户或管理员权限。

硬盘驱动器

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> `icon_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"`

# 漏洞分析

深入探索

西部数据

鉴权

软件

## login\_check

直接看 `/lib/login_checker.php` 登录相关逻辑的实现

漏洞扫描服务

```
function login_check()
{
        $ret = 0;
        if (isset($_SESSION['username']))
        {
                if (isset($_SESSION['username']) && $_SESSION['username'] != "")
                $ret = 2; //login, normal user

                if ($_SESSION['isAdmin'] == 1)
                        $ret = 1; //login, admin
        }
        else if (isset($_COOKIE['username']))
        {
                if (isset($_COOKIE['username']) && $_COOKIE['username'] != "")
                $ret = 2; //login, normal user

                if ($_COOKIE['isAdmin'] == 1)
                        $ret = 1; //login, admin
        }
        return $ret;
}
```

- `login_check()` 函数直接使用客户端可控的 `$_COOKIE['username']` 和 `$_COOKIE['isAdmin']` 进行权限判断，但未进行任何有效性校验。
- 当用户未登录（无有效 SESSION）时，系统直接信任 Cookie 中的 `username` 和 `isAdmin` 值，导致攻击者可[绕过权限](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)伪造身份。
- 即使存在 SESSION，由于逻辑缺陷，Cookie 仍可能影响权限判断，存在权限混淆风险。

因此只需要在请求header部分添加如下cookie即可绕过鉴权

计算机驱动器和存储设备

深入探索

服务器

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨

身份验证

```
Cookie: username=admin; isAdmin=1
```

## wto\_check

在另一个检查管理员是否登陆超时的函数wto\_check()校验中也是存在漏洞的

```
/*
  return value: 1: Login, 0: No login
*/
function wto_check($username)
{
        if (empty($username))
                return 0;

        exec(sprintf("wto -n \"%s\" -i '%s' -c", escapeshellcmd($username), $_SERVER["REMOTE_ADDR"]), $login_status);
        if ($login_status[0] === "WTO CHECK OK")
                return 1;
        else
                return 0;
}

/* ret: 0: no login, 1: login, admin, 2: login, normal user */
```

`wto_check()`的PHP函数，会检查某个用户（$username）是不是已经超时,它会调用一个系统里的“wto”程序，检查某个用户名和IP对应的定时器（也就是登录状态是不是还有效）。

数据备份与恢复

`wto_check()`的PHP函数，会检查某个用户（$username）是不是已经超时,它会调用一个系统里的“wto”程序，检查某个用户名和IP对应的定时器（也就是登录状态是不是还有效）。

```
# wto --h
Usage: wto [parm]
-h        help
-n        user name
-i        ip address
-s        set timeout
-g        get timer
-c        check timeout
-r        reset timer
-a        remove all
-x        del timeout item
-z        show all
-d        del user
```

- 代码里用`exec()`函数去执行系统命令，把用户名和IP拼到命令里。
- 为了安全，开发者本来想对用户名做过滤，防止有人恶意输入特殊内容，结果用了`escapeshellcmd()`这个PHP函数。
- **但这个函数只适合过滤整个命令，不适合单独过滤某个参数！**
- 正确应该用`escapeshellarg()`，它会把参数用引号括起来，防止参数里带特殊字符或多余命令。

因此这会导致因为过滤不严，攻击者可以在用户名后面加特殊内容，比如加上`-s 99999`（意思是设置超时时间为99999）。这样系统本来只是想“查一下你是不是超时”，结果攻击者却能“顺便重置自己的超时时间”，让自己一直保持登录状态。这样攻击者就可以**绕过超时机制**，一直以管理员身份操作系统。

网络安全

可在cookie里添加 `username=admin" -s 9999 -c "` 这个来设置超时时间，从而让系统认为管理员没超时，从而绕过鉴权。

相当于调用 wto 程序的 -s 参数来设置超时时间为 9999 从而绕过了系统本有鉴权检查。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.login\_check](#toc-4-1-)
- [4.2.wto\_check](#toc-4-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
