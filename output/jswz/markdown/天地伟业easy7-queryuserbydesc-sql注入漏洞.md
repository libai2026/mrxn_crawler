---
title: "天地伟业Easy7 queryUserbyDesc SQL注入漏洞"
source: https://mrxn.net/jswz/easy7-user-queryUserbyDesc-sqli.html
asset_dir: assets/天地伟业easy7-queryuserbydesc-sql注入漏洞
---

# 天地伟业Easy7 queryUserbyDesc SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/9 08:41
- 286浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

计算机安全

rest

数据库

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

SQL注入防护

该系统的 /Easy7/rest/user/queryUserbyDesc 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意请求执行任意SQL语句，可能导致敏感信息泄露或数据库被篡改。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

代码安全审计

再来看本次的漏洞接口 /Easy7/rest/user/queryUserbyDesc 对应的 `queryUserbyDesc()` 方法实现逻辑

```
@Controller
@RequestMapping({"/user"})
public class CLS_REST_User {
    @Resource(
        name = "boUser"
    )
    private CLS_BO_User boUser;

    @RequestMapping({"/queryUserbyDesc"})
    public void queryUserbyDesc(HttpServletRequest req, HttpServletResponse resp, String userDesc) throws IOException {
        resp.getWriter().print(JSONObject.fromObject(this.boUser.queryUserbyDesc(userDesc)));
    }
```

深入探索

在线安全工具

Web安全书籍

安全工具开发

参数`id`被直接带入`boUser.queryUserbyDesc`方法

```
@Transactional
public CLS_VO_Result queryUserbyDesc(String userDesc) {
    CLS_VO_Result result = new CLS_VO_Result();
    if (userDesc != null && !"".equals(userDesc)) {
        result.setContent(this.daoUser.queryUserbyDesc(userDesc));
        result.setRet(0);
        return result;
    } else {
        result.setRet(-7);
        return result;
    }
}
```

继续跟进 `daoUser.queryUserbyDesc`方法

[![天地伟业Easy7 queryUserbyDesc SQL注入漏洞](images/img-001-7e1d797a8c64.webp)](https://image.mrxn.net/edb064c5b0594a9485ecd0abf3dec65c.webp)

最终在dao层，参数`userDesc`是未经任何过滤或校验直接拼接在IN自查询SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /Easy7/rest/user/queryUserbyDesc HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

userDesc=SQLI_POC
```

深入探索

文本剥离工具

JSON处理工具

编程语言教程

[![天地伟业Easy7 queryUserbyDesc SQL注入漏洞](images/img-002-f63ee3c5be58.webp)](https://image.mrxn.net/0b3e3f5c7c5d493f9a2a9e22d7601848.webp)

成功延时5秒

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
