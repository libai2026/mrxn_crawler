---
title: "友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞"
source: https://mrxn.net/jswz/youjiasoft-Sysconfig-GetZTList-unauthcation.html
asset_dir: assets/友加畅捷管理系统-sysconfiggetztlist-未授权访问致信息泄露漏洞
---

# 友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/27 08:30
- 875浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

身份验证

安全

认证

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理[软件](#)，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

网络安全

该系统的 `Sysconfig/GetZTList` 接口存在[未授权访问](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)漏洞，攻击者无需任何认证即可直接访问该接口，从而获取敏感信息。此漏洞可能导致企业内部数据[泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)，包括但不限于用户列表、配置信息等，对企业的运营安全和数据隐私构成严重威胁。

# 影响版本

13.7004.1053.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

深入探索

安全研究报告

编码转换工具

在线安全工具

在 SysconfigController 找到 GetZTList 方法处理逻辑如下

漏洞修复方案

[![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](images/img-001-c2f37a1ac2a1.webp)](https://image.mrxn.net/b7f08d7492b545e0b3c9f649581e3108.webp)

表明需要一个pwd参数，即可返回 `DBOperation.GetZTList` 的内容，跟进看下它的实现逻辑

[![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](images/img-002-35961406a99f.webp)](https://image.mrxn.net/6220a59dd3ed4ddb81e888da5e747198.webp)

1. **框架行为:** 在 ASP.NET (或 ASP.NET Core) MVC/Web API 框架中，当一个 Action 方法的参数是引用类型（如 `string`）且在 HTTP 请求中未提供该参数时，模型绑定器会为该参数赋其默认值。对于 `string` 类型，其默认值为 `null`。
2. **代码执行路径:** 因此，当攻击者请求 `GetZTList` 接口而不带 `pwd` 参数时，`GetZTList(string pwd)` 方法中的 `pwd` 变量值为 `null`。
3. **条件判断绕过:** 代码会执行 `if (string.op_Inequality(pwd, "-1"))`，这等同于 `if (pwd != "-1")`。由于 `pwd` 是 `null`，`null != "-1"` 的结果为 `true`。因此，程序会进入 `if` 代码块，而不是 `else` 分支。
4. **过滤逻辑缺陷:** 在 `if` 代码块内部，程序会执行 `Where` 条件进行过滤： `m => string.op_Equality(m.ZTPwd, "") || m.ZTPwd == null || string.op_Equality(m.ZTPwd, jmPwd)`
   - 由于 `pwd` 为 `null`，`jmPwd = EncDecString.EncryptPWD(null)` 的结果很可能是 `null` 或空字符串 `""` (取决于 `EncryptPWD` 方法的实现)。
   - **情况一：`jmPwd` 为 `null`。** 过滤条件变为 `m.ZTPwd == "" || m.ZTPwd == null || m.ZTPwd == null`，简化为 `m.ZTPwd == "" || m.ZTPwd == null`。
   - **情况二：`jmPwd` 为 `""`。** 过滤条件变为 `m.ZTPwd == "" || m.ZTPwd == null || m.ZTPwd == ""`，同样简化为 `m.ZTPwd == "" || m.ZTPwd == null`。
5. **最终结果:** 无论 `EncryptPWD(null)` 的具体返回值是什么，最终的过滤逻辑都会返回所有 `ZTPwd` 字段为**空字符串或 `null`** 的账套列表。这实质上是列出了系统中所有**未设置密码**的账套。

[![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](images/img-003-e685a0971727.webp)](https://image.mrxn.net/052fb996c47b4dbaab6394673c3a6ae0.webp)

1. 代码的业务逻辑是通过 `pwd` 参数来验证用户身份，并返回其有权访问的账套列表。
2. 代码中存在一个关键的条件判断：`if (string.op_Inequality(pwd, "-1"))`，这等同于 `if (pwd != "-1")`。
3. **正常逻辑分支 (`pwd` 不等于 `"-1"`)**: 当 `pwd` 不为 `"-1"` 时，程序会执行 `if` 代码块。此代码块会将传入的 `pwd` 参数进行加密（`EncDecString.EncryptPWD(pwd)`），然后与配置文件中每个账套的 `ZTPwd` 字段进行比对。只有密码为空、`null` 或匹配成功的账套才会被返回。这是预期的、受保护的业务逻辑。
4. **漏洞逻辑分支 (`pwd` 等于 `"-1"`)**: 当 `pwd` 参数的值**正好为字符串 `"-1"`** 时，程序会跳过 `if` 代码块，执行 `else if` 代码块。在此分支中，代码会遍历 `zts`（即从配置文件 `sysconfig_zts` 中加载的**所有**账套列表），并**不做任何密码校验**，直接将所有账套的详细信息添加到 `ztList` 中并返回。

再看前端 js 里有关此路由的调用如下，`pwd`参数可有可无

物流软件安全

[![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](images/img-004-c4331435dea7.webp)](https://image.mrxn.net/01a07707ca7048f8a7813cddb51b71c2.webp)

或者是 `pwd=-1`

[![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](images/img-005-aa26a78d30f7.webp)](https://image.mrxn.net/ff4bcae60f7b44b784bca69135c148f3.webp)

# 漏洞复现

```
GET /Sysconfig/GetZTList HTTP/1.1
Host: youjiasoft.mrxn.net
```

[![友加畅捷管理系统 Sysconfig/GetZTList 未授权访问致信息泄露漏洞](images/img-006-8ce1b89b5925.webp)](https://image.mrxn.net/72bc8cef116f46cbae42042007b5e23f.webp)

响应包含数据库连接信息、应用安装物理路径等敏感信息。

网络安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)
- [#asp.net](https://mrxn.net/tag/asp.net)
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
