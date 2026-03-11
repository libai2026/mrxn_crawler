---
title: "用友U8+渠道管理(高级版) gettoken_new SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-api-gettoken_new-sqli.html
asset_dir: assets/用友u8+渠道管理(高级版)-gettoken_new-sql注入漏洞
---

# 用友U8+渠道管理(高级版) gettoken\_new SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/19 10:39
- 789浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

api

授权

sql

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)U8+是用友公司推出的企业管理[软件](#)平台，广泛应用于财务、供应链及人力资源等核心业务流程中。在U8+渠道管理（高级版）模块中，`gettoken_new` 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。该漏洞是由于页面在处理用户输入的参数时，未对输入内容进行充分过滤与安全校验，攻击者可构造恶意SQL语句，通过HTTP请求注入至后端数据库查询中。

SQL注入检测工具

# 影响版本

V18, V16.5, V16.1, V16.0, V15.1, V15.0, V13

# fofa语法

> title="渠道管理（高级版）"

# 漏洞分析

根据web.xml对url `/api/gettoken_new` 的映射

```
    <servlet>
        <servlet-name>GetTokenServlet</servlet-name>
        <servlet-class>
            com.gxfcsoft.framework.core.GetTokenServlet
        </servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>GetTokenServlet</servlet-name>
        <url-pattern>/api/gettoken_new</url-pattern>
    </servlet-mapping>
```

深入探索

VPN服务

Docker加速服务

SQL注入防护

直接看 `com.gxfcsoft.framework.core.GetTokenServlet` 实现逻辑

代码安全审计

```
  protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    Calendar c = Calendar.getInstance();
    String start_date = DateUtil.getDateTime(c);
    String errorInfo = "";
    String resultInfo = "";
    boolean isSuccess = false;
    String remoteAddr = req.getRemoteAddr();
    String remoteHost = req.getRemoteHost();
    String remoteUser = req.getRemoteUser();
    int remotePort = req.getRemotePort();
    String path = req.getPathInfo();
    if (path == null || path.isEmpty())
      path = req.getRequestURI().substring(req.getContextPath().length()); 
    String username = "";
    req.setCharacterEncoding("UTF-8");
    resp.setCharacterEncoding("UTF-8");
    JSONObject json = new JSONObject();
    String appid = req.getParameter("appid");
    String userid = req.getParameter("userid");
    String appkey = req.getParameter("appkey");
    String appsecret = req.getParameter("appsecret");
    json = checkParams(appid, userid, appkey, appsecret, json);
    if (json.isEmpty()) {
      appsecret = appsecret.replace(" ", "+");
      Element element = queryObject(appid, appsecret, appkey);
```

深入探索

安全工具开发

漏洞扫描服务

安全

跟进`checkParams` 方法看下

漏洞修复方案

```
  public JSONObject checkParams(String appid, String userid, String appkey, String appsecret, JSONObject json) {
    if (StringUtil.isEmpty(appid)) {
      json.put("flag", "1");
      json.put("msg", String.valueOf(appid) + "为空！");
    } 
    if (StringUtil.isEmpty(userid)) {
      json.put("flag", "1");
      json.put("msg", String.valueOf(userid) + "为空！");
    } 
    if (StringUtil.isEmpty(appkey)) {
      json.put("flag", "1");
      json.put("msg", String.valueOf(appkey) + "为空！");
    } 
    if (StringUtil.isEmpty(appsecret)) {
      json.put("flag", "1");
      json.put("msg", String.valueOf(appsecret) + "为空！");
    } 
    return json;
  }
```

判断这些参数是否为空。继续跟进`queryObject` 方法

```
  public Element queryObject(String appid, String appsecret, String appkey) {
    Connection conn = null;
    try {
      conn = ResManager.getConnection("default");
      UserState us = new UserState();
      us.setCorpName("default");
      CommonDao cDao = new CommonDao(conn, us);
      String select_sql = "select top 1 * from iauthregister where appid = '" + appid + "' and appsecret = '" + appsecret + "' and appkey = '" + appkey + "' ";
      Element element = cDao.findOne(select_sql);
      return element;
    } catch (SQLException e) {
      e.printStackTrace();
      return null;
    } finally {
      if (conn != null)
        ResManager.freeConnection("default", conn); 
    } 
  }
```

到这就很明了了，参数`appid`、`appsecret`和`appkey`未经过任何过滤或校验就被直接拼接进SQL语句中，从而导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

补丁修复也很直接，正则检测是否包含危险字符串

物流软件安全

[![用友U8+渠道管理(高级版) gettoken_new SQL注入漏洞](images/img-001-86f539e5ab1c.webp)](https://image.mrxn.net/e218fcab624f4c409d120bc03f74a486.webp)

# 漏洞复现

```
GET /api/gettoken_new?appid='SQLI_POC&appkey=1&appsecret=1&userid=1 HTTP/1.1
Host: u8.mrxn.net
```

[![用友U8+渠道管理(高级版) gettoken_new SQL注入漏洞](images/img-002-420f3266d9a9.webp)](https://image.mrxn.net/c50611891d274ac8886ac7ad5f274faa.webp)

延时 5 秒成功

文件大小转换

# 参考

- [关于U8+渠道管理(高级版)存在SQL注入漏洞的公告](https://security.yonyou.com/#/noticeInfo?id=730)
- <https://security.yonyou.com/#/patchInfo?identifier=c53323eb06a64ee18cb5d95dcbd7d5ff>

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
