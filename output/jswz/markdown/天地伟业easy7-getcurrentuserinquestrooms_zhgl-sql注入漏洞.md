---
title: "天地伟业Easy7 getCurrentUserInquestRooms_ZHGL SQL注入漏洞"
source: https://mrxn.net/jswz/easy7-inquestRoom-getCurrentUserInquestRooms_ZHGL-sqli.html
asset_dir: assets/天地伟业easy7-getcurrentuserinquestrooms_zhgl-sql注入漏洞
---

# 天地伟业Easy7 getCurrentUserInquestRooms\_ZHGL SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/4 08:29
- 305浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

计算机安全

软件

表现层状态转换

---

# 漏洞简介

天地伟业Easy7是一款用于视频监控管理的[软件](#)系统。

SQL注入检测工具

该系统的 /Easy7/rest/inquestRoom/getCurrentUserInquestRooms\_ZHGL 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意请求执行任意SQL语句，可能导致敏感信息泄露或数据库被篡改。

# 影响版本

# fofa语法

> body="/Easy7/apps/WebService/LogIn.jsp" || body="Easy7/VideoLib.EXE" || body="/Easy7/index.html" || (body="<img src=\"./images/ico/Easy7\_logo\_transparent.png") && title="平台"

# 漏洞分析

深入探索

授权

编程语言教程

Nessus

首先，该系统基于Spring 3.0，比较古老且WEB-INF/web.xml里没有配置任何filter进行权限校验，因此绝大部分接口都是可以直接访问的。

代码安全审计

再来看本次的漏洞接口 /Easy7/rest/inquestRoom/getCurrentUserInquestRooms\_ZHGL 对应的 `getCurrentUserInquestRooms_ZHGL()` 方法实现逻辑

```
@Controller
@RequestMapping({"/inquestRoom"})
public class CLS_REST_InquestRoom {
    private static final Logger log = LoggerFactory.getLogger(CLS_REST_InquestRoom.class);
    @Resource(
        name = "boInquestRoom"
    )
    private CLS_BO_InquestRoom boInquestRoom;
    @RequestMapping({"/getCurrentUserInquestRooms_ZHGL"})
    public void getCurrentUserInquestRooms_ZHGL(HttpServletRequest request, HttpServletResponse response, String currentCourtFjm) throws Exception {
        response.getWriter().print(JSONObject.fromObject(this.boInquestRoom.getCurrentUserInquestRooms_ZHGL(currentCourtFjm)));
    }
```

深入探索

文件大小转换

安全认证考试

编码转换工具

参数`currentCourtFjm`被直接带入`boInquestRoom.getCurrentUserInquestRooms_ZHGL`方法

```
public CLS_VO_Result getCurrentUserInquestRooms_ZHGL(String currentCourtFjm) {
        CLS_VO_Result result = new CLS_VO_Result();
        result.setContent(this.daoInquestRoom.getCurrentUserInquestRooms_ZHGL(currentCourtFjm));
        result.setRet(0);
        return result;
    }
```

继续跟进 `daoInquestRoom.getCurrentUserInquestRooms_ZHGL(currentCourtFjm)`方法

[![天地伟业Easy7 getCurrentUserInquestRooms_ZHGL SQL注入漏洞](images/img-001-ee9ea8924d3f.webp)](https://image.mrxn.net/2331eb7d71864907a4a4010f67ffa574.webp)

最终在dao层，参数`currentCourtFjm`是未经任何过滤或校验就被直接拼接进`"AND ROOM.S_SX_CODE = '" + currentCourtFjm + "'"`SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /Easy7/rest/inquestRoom/getCurrentUserInquestRooms_ZHGL HTTP/1.1
Host: easy7.mrxn.net
Content-Type: application/x-www-form-urlencoded

currentCourtFjm=SQLI_POC
```

[![天地伟业Easy7 getCurrentUserInquestRooms_ZHGL SQL注入漏洞](images/img-002-5ee67d00f7cf.webp)](https://image.mrxn.net/de52a0e915c74c4bb1047e76d5576169.webp)

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
