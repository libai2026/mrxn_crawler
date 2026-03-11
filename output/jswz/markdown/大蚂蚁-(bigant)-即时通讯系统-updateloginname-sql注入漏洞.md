---
title: "大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞"
source: https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html
asset_dir: assets/大蚂蚁-(bigant)-即时通讯系统-updateloginname-sql注入漏洞
---

# 大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/1 13:16
- 304浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

身份验证

sql

api

---

# 漏洞简介

杭州九麒科技大蚂蚁 (BigAnt) 即时通讯系统是一款企业级IM通信管理系统，提供多种功能支持。该系统的 \Api\Controller\UserController::updateLoginName 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可通过在 updateLoginName 功能的相关参数中插入恶意构造的 SQL 查询语句，实现对后端数据库的非法操作，可能导致敏感信息泄露、数据篡改、绕过身份验证，甚至在特定配置下实现任意命令执行或获取系统控制权限。

短信和即时消息

# 影响版本

BigAnt 5.5.x 及以上版本用户

[![大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](images/img-001-af66cd8e6523.webp)](https://image.mrxn.net/5623d2945cc347a388c16efc24905efc.webp)

经过测试，最新版本 6.0.1.20250407.1 也受影响

SQL注入检测工具

深入探索

鉴权

即时通讯

数据库

# fofa语法

> (body="/Public/static/admin/admin\_common.js" && body="/Public/lang/zh-cn.js.js") || title="即时通讯 系统登录" && body="/Public/static/ukey/Syunew3.js"

# 漏洞分析

系统是基于thinkphp 3.2架构，大部分采用数组形式的参数传递不存在sql注入

在 ThinkPHP 3.2 中：

- `->where(array条件)` 使用**数组方式**传参是安全的（框架会自动参数绑定/转义）
- `->where("字符串拼接")` 使用**字符串拼接**外部输入是**危险的**
- `->query($sql)` / `->execute($sql)` 直接执行原生 SQL，如果拼接了用户输入则存在注入风险
- `I()` 函数虽有基本过滤，但不能完全防止 [SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)（特别是在字符串拼接场景下）

但是部分控制器的部分方法如**UserController.class.php**下的**updateLoginName()**方法中

深入探索

应用程序接口

Api

SQL

```
public function updateLoginName()
{
        $userId = $this->q('user_id',1);
        $newLogin = $this->q('user_login',1);

        //查看user_login是否存在
        $loginMap = [];
        $loginMap['user_id'] = array('neq',$userId);
        $loginMap['user_login'] = $newLogin;
        $hasLogin = $this->model->field('user_id')->where($loginMap)->select();
        if (!empty($hasLogin)) {
                $this->responseFail(ERR_OP_ERR,L('_USER_UPDATE_ERROR_')) ;
        }

        //查看user_login是否未变更
        $oldLogin = $this->model->where('user_id = '.$userId)->getField('user_login');
        if ($oldLogin == $newLogin) {
                $this->responseSuccess(L('_EDIT_SUCCESS_'));
        }
```

`$userId`来自用户请求参数 `$this->q('user_id',1);`，直接拼接到 `where('user_id = '.$userId)->getField('user_login')`字符串中，攻击者可通过构造恶意 `user_id`参数注入SQL payload造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 认证码参考[大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html) 的权限分析部分
>
> 代码安全审计

```
POST /api/user/updateLoginName HTTP/1.1
Host: bigant.mrxn.net
Content-Type: application/x-www-form-urlencoded

authen=cc7e6a614831d1c6b351a5f12678ed4b94cf98b2a52b1050d6c19433fdeff37d&uid=1&user_login=1&user_id=SQLI_POC
```

[![大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](images/img-002-0378e7462b13.webp)](https://image.mrxn.net/37defb6f8c0e49a7862f1e881bd7a5b1.webp)

成功利用报错注入获取到数据库用户信息。

漏洞扫描服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#MySQL](https://mrxn.net/tag/MySQL)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
