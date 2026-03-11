---
title: "天地伟业Easy7 queryDataByTypeEx SQL注入漏洞"
source: https://mrxn.net/jswz/easy7-workbook-queryDataByTypeEx-sqli.html
asset_dir: assets/天地伟业easy7-querydatabytypeex-sql注入漏洞
---

# 天地伟业Easy7 queryDataByTypeEx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/13 08:32
- 266浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

数据库

安全

rest

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

SQL注入防护

该系统的 /Easy7/rest/workbook/queryDataByTypeEx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意请求执行任意SQL语句，可能导致敏感信息泄露或数据库被篡改。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

代码安全审计

再来看本次的漏洞接口 /Easy7/rest/workbook/queryDataByTypeEx 对应的 `queryDataByTypeEx()` 方法实现逻辑

```
@Controller
@RequestMapping({"/workbook"})
public class CLS_REST_WorkBook {
    @Resource(
        name = "boWorkBook"
    )
    private CLS_BO_WorkBook boWorkBook;

    @RequestMapping({"/queryDataByTypeEx"})
    public void queryDataByTypeEx(HttpServletRequest req, HttpServletResponse resp, CLS_VO_WorkBookPageEx voPage) throws IOException {
        resp.getWriter().print(JSONObject.fromObject(this.boWorkBook.queryDataByTypeEx(voPage)));
    }
```

深入探索

Docker加速服务

安全研究工具

文本剥离工具

参数对象`voPage`被直接带入`boWorkBook.queryDataByTypeEx`方法

```
@Transactional(
    propagation = Propagation.REQUIRED
)
public CLS_VO_Result queryDataByTypeEx(CLS_VO_WorkBookPageEx voPage) throws UnsupportedEncodingException {
    return this.daoWorkBook.queryDataByTypeEx(voPage.getTabname());
}
```

继续跟进 `daoWorkBook.queryDataByTypeEx(voPage.getTabname())`方法

[![天地伟业Easy7 queryDataByTypeEx SQL注入漏洞](images/img-001-12e241507063.webp)](https://image.mrxn.net/5014933c669a48989690e64dfd858c45.webp)

最终在dao层，参数`tabname`是未经任何过滤或校验直接拼接在SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /Easy7/rest/workbook/queryDataByTypeEx HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

tabname=TAB_WORKBOOK_TYPE SQLI_POC
```

[![天地伟业Easy7 queryDataByTypeEx SQL注入漏洞](images/img-002-fbabc42bf97f.webp)](https://image.mrxn.net/692d14e1ec034384845b6fd202394058.webp)

成功延时5秒

漏洞扫描服务

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
