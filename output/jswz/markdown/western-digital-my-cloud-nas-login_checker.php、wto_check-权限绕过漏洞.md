---
title: "Western Digital My Cloud NAS login_checker.php、wto_check 权限绕过漏洞"
source: https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-login_checker-authbypass.html
asset_dir: embedded-base64
---

# 漏洞简介

Western Digital My Cloud NAS是美国西部数据（Western Digital）公司的一款应用广泛的网络连接云存储设备，可用于托管文件，并自动备份和同步该文件与各种云和基于Web的服务。Western Digital My Cloud NAS `login_checker.php` 接口文件未对用户会话进行严格验证，存在[身份验证绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，攻击者可通过构造恶意 Cookie 绕过身份认证机制，直接获取普通用户或管理员权限。

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> `icon_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"`

# 漏洞分析

## login\_check

直接看 `/lib/login_checker.php` 登录相关逻辑的实现

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

深入探索

数据管理

防病毒程序与恶意软件

网络

```
Cookie: username=admin; isAdmin=1
```

## wto\_check

在另一个检查管理员是否登陆超时的函数wto\_check()校验中也是存在[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")的

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

计算机安全

可在cookie里添加 `username=admin" -s 9999 -c "` 这个来设置超时时间，从而让系统认为管理员没超时，从而绕过鉴权。

相当于调用 wto 程序的 -s 参数来设置超时时间为 9999 从而绕过了系统本有鉴权检查。
