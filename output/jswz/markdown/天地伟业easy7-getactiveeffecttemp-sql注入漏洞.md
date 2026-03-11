---
title: "天地伟业Easy7 getActiveEffectTemp SQL注入漏洞"
source: https://mrxn.net/jswz/easy7-obj-getActiveEffectTemp-sqli.html
asset_dir: assets/天地伟业easy7-getactiveeffecttemp-sql注入漏洞
---

# 天地伟业Easy7 getActiveEffectTemp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/6 08:37
- 274浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

表现层状态转换

软件

rest

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

SQL注入检测工具

该系统的 /Easy7/rest/obj/getActiveEffectTemp 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意请求执行任意SQL语句，可能导致敏感信息泄露或数据库被篡改。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

代码安全审计

再来看本次的漏洞接口 /Easy7/rest/obj/getActiveEffectTemp 对应的 `getActiveEffectTemp()` 方法实现逻辑

```
@Controller
@RequestMapping({"/inquestRoom"})
public class CLS_REST_InquestRoom {
    private static final Logger log = LoggerFactory.getLogger(CLS_REST_InquestRoom.class);
    @Resource(
        name = "boInquestRoom"
    )
    private CLS_BO_InquestRoom boInquestRoom;
    @RequestMapping({"/getActiveEffectTemp"})

    @RequestMapping({"/getActiveEffectTemp"})
    public void getActiveEffectTemp(HttpServletRequest req, HttpServletResponse resp, String id) throws IOException {
        resp.getWriter().print(JSONObject.fromObject(this.boObj.getActiveEffectTemp(id)));
    }
```

深入探索

VPN服务

安全研究工具

漏洞扫描服务

参数`id`被直接带入`boInquestRoom.getActiveEffectTemp`方法

```
public CLS_VO_Result getActiveEffectTemp(String id) {
    CLS_VO_Result result = new CLS_VO_Result();
    if (id != null && !"".equals(id)) {
        List<CLS_VO_OBJ> objList = this.daoObj.getActiveEffectTemp(id);
        result.setRet(0);
        result.setContent(objList);
        return result;
    } else {
        result.setRet(-7);
        log.error("getActiveEffectTemp id == null");
        return result;
    }
}
```

继续跟进 `daoInquestRoom.getActiveEffectTemp`方法

[![天地伟业Easy7 getActiveEffectTemp SQL注入漏洞](images/img-001-26e1c50026a0.webp)](https://image.mrxn.net/140ac740b59642e6a5a8372425fbe78c.webp)

最终在dao层，参数`id`是未经任何过滤或校验直接拼接在IN自查询SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /Easy7/rest/obj/getActiveEffectTemp HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=SQLI_POC
```

[![天地伟业Easy7 getActiveEffectTemp SQL注入漏洞](images/img-002-ec8e8f75eaab.webp)](https://image.mrxn.net/e767cdcca3a54c5d8d49e31cf9a34f96.webp)

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
